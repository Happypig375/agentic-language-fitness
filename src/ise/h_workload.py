"""Model-free H1/H2 sources and independent Expanded-operation oracles."""
from __future__ import annotations
import datetime as dt, json, re
from pathlib import Path
from typing import Any, Mapping
from . import h0
from .workstream_e3a import snapshot

_LANGS = ("csharp", "fsharp")
_DEF = "protocols/workstream-h0/definition.json"
_ROLE = {"csharp": ("OrderFlow.csproj", "OrderFlowEngine.cs", "Program.cs"),
         "fsharp": ("OrderFlow.fsproj", "OrderFlowEngine.fs", "Program.fs")}
_INT = re.compile(r"-?(?:0|[1-9][0-9]*)\Z")
_DATE = re.compile(r"([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2}):([0-9]{2})(?:\.([0-9]{1,7}))?(Z|[+-][0-9]{2}:[0-9]{2})\Z")

def _def(root: Path): return h0._definition(root, _DEF)

def source_for(root: Path, level: str, language: str, gold: bool = False) -> dict[str, str]:
    root = Path(root)
    if level not in ("core", "expanded") or language not in _LANGS: raise ValueError("unsupported workload level or language")
    if level == "core":
        definition = _def(root)
        if not gold: return h0.source_for(root, definition, language)
        manifest = h0._manifest(root, definition)
        return dict(snapshot(root, manifest, language, 8))
    base = root / "benchmarks/workstream-h" / ("gold" if gold else "repos") / language / ("summary" if gold else "expanded")
    if not base.is_dir(): raise ValueError("expanded source bundle is missing")
    entries = list(base.iterdir())
    if any(p.is_symlink() for p in entries): raise ValueError("source bundle contains symlink")
    for p in entries:
        if p.is_dir() and p.name.casefold() not in {"bin", "obj"}:
            raise ValueError("unexpected source directory")
    files = [p for p in entries if p.is_file()]
    by_lower = {p.name.casefold(): p for p in files}
    required = {name.casefold() for name in _ROLE[language]}
    if not required.issubset(by_lower) or len(files) > 8:
        raise ValueError("expanded source file set mismatch")
    allowed_suffixes = {".cs", ".fs", ".csproj", ".fsproj"}
    if any(p.suffix.casefold() not in allowed_suffixes or not p.name.isascii() or "\x00" in p.name for p in files):
        raise ValueError("invalid source filename")
    result = {}
    total = 0
    for p in sorted(files):
        text = p.read_bytes().decode("utf-8").replace("\r\n", "\n")
        if "\r" in text or "\x00" in text:
            raise ValueError("invalid source text")
        total += len(text.encode("utf-8"))
        result[p.name] = text
    if total > 65536: raise ValueError("source bundle exceeds byte limit")
    return result

def public_payload(root: Path, level: str) -> dict[str, Any]:
    if level not in ("core","expanded"): raise ValueError("unsupported workload level")
    root = Path(root); payload = dict(h0.contract_payload(root, _def(root)))
    if level == "expanded":
        payload["expanded_contract"] = (root/"benchmarks/workstream-h/contract.md").read_text(encoding="utf-8")
        payload["expanded_public_examples"] = json.loads((root/"benchmarks/workstream-h/public-examples.json").read_text(encoding="utf-8"))["examples"]
    return payload

def ordered_filenames(source: Mapping[str,str], language: str, reverse: bool=False) -> list[str]:
    if language not in _LANGS: raise ValueError("unsupported language")
    names = list(source); roles = _ROLE[language]; by = {n.lower():n for n in names}
    req = [by[x.lower()] for x in roles if x.lower() in by]
    if len(req) == 3:
        known = {x.lower() for x in req}; extra = sorted((x for x in names if x.lower() not in known))
        result = [req[0], *extra, req[1], req[2]]
    else: result = sorted(names)
    return list(reversed(result)) if reverse else result

def _key(s: str): 
    b=s.encode("utf-16-le","surrogatepass"); return tuple(b[i]|b[i+1]<<8 for i in range(0,len(b),2))

def _prop(o: Mapping[str,Any], name: str, default=None):
    for k,v in o.items():
        if isinstance(k,str) and k.lower()==name.lower(): return v
    return default

def _instant(x: Any):
    if not isinstance(x,str): return None
    m=_DATE.fullmatch(x)
    if not m: return None
    y,mo,d,h,mi,se,frac,z=m.groups(); oh=om=0
    if z!="Z":
        oh,om=int(z[1:3]),int(z[4:6])
        if oh>14 or om>59 or (oh==14 and om): return None
    try: base=dt.datetime(int(y),int(mo),int(d),int(h),int(mi),int(se),tzinfo=dt.timezone.utc)
    except ValueError: return None
    epoch=dt.datetime(1,1,1,tzinfo=dt.timezone.utc)
    ticks=((base-epoch).days*86400+base.hour*3600+base.minute*60+base.second)*10000000+int((frac or "").ljust(7,"0") or 0)
    sign=1 if z=="Z" or z[0]=="+" else -1
    ticks -= sign*(oh*60+om)*60*10000000
    return ticks if 0 <= ticks <= 3155378975999999999 else None

def _integer(x: Any):
    if type(x) is not int or not _INT.fullmatch(str(x)): return None
    return x if -2147483648<=x<=2147483647 else None

def _record(side: str, x: Any):
    if not isinstance(x,dict): return f"invalid {side} record"
    i=_prop(x,"id")
    if not isinstance(i,str): return f"invalid {side} id"
    p=_integer(_prop(x,"priority"))
    if p is None: return f"invalid {side} priority"
    t=_instant(_prop(x,"createdAt"))
    return f"invalid {side} createdAt" if t is None else (i,p,t)

def _reconcile(r):
    sides={}
    for side in ("left","right"):
        a=_prop(r,side)
        if a is None: a=[]
        if not isinstance(a,list): return {"error":f"{side} must be an array"}
        parsed=[]
        for x in a:
            q=_record(side,x)
            if isinstance(q,str): return {"error":q}
            parsed.append(q)
        sides[side]=parsed
    # The contract validates every record on both sides before checking either
    # side for duplicate IDs. Keep those phases separate so a malformed right
    # record takes precedence over duplicate left IDs.
    for side in ("left","right"):
        vals={}
        for q in sides[side]:
            if q[0] in vals: return {"error":f"duplicate {side} id"}
            vals[q[0]]=q
        sides[side]=vals
    out=[]
    for i in sorted(set(sides["left"])|set(sides["right"]), key=_key):
        l,r=sides["left"].get(i),sides["right"].get(i)
        origin="left" if r is None else "right" if l is None else ("right" if (r[1],r[2]) >= (l[1],l[2]) else "left")
        out.append({"id":i,"origin":origin})
    return {"items":out}

def _dependency(r):
    ids=_prop(r,"ids")
    if ids is None: ids=[]
    if not isinstance(ids,list) or any(not isinstance(x,str) for x in ids): return {"error":"invalid ids"}
    if len(set(ids))!=len(ids): return {"error":"duplicate id"}
    edges=_prop(r,"edges")
    if edges is None: edges=[]
    if not isinstance(edges,list): return {"error":"invalid edges"}
    pairs=[]
    for e in edges:
        a,b=(_prop(e,"before"),_prop(e,"after")) if isinstance(e,dict) else (None,None)
        if not isinstance(a,str) or not isinstance(b,str): return {"error":"invalid edge"}
        pairs.append((a,b))
    if len(set(pairs)) != len(pairs): return {"error":"duplicate edge"}
    known=set(ids)
    if any(a not in known or b not in known for a,b in pairs): return {"error":"unknown dependency"}
    if any(a==b for a,b in pairs): return {"error":"self dependency"}
    out={i:set() for i in ids}; deg={i:0 for i in ids}
    for a,b in pairs: out[a].add(b); deg[b]+=1
    result=[]
    while True:
        ready=sorted((i for i in ids if deg[i]==0 and i not in result),key=_key)
        if not ready: break
        x=ready[0]; result.append(x)
        for y in out[x]: deg[y]-=1
    return {"ids":result} if len(result)==len(ids) else {"error":"dependency cycle"}

def oracle_additions(request: Any) -> dict[str,Any]:
    if request is None: return {"error":"Request was null"}
    if not isinstance(request,dict): raise ValueError("unsupported request")
    op=_prop(request,"operation")
    if not isinstance(op,str): raise ValueError("unsupported operation")
    if op.lower()=="reconcile": return _reconcile(request)
    if op.lower()=="dependencyorder": return _dependency(request)
    raise ValueError("unsupported operation")

def cases_for(root: Path, level: str, include_summary: bool=True) -> list[dict[str,Any]]:
    root=Path(root); m=json.loads((root/"benchmarks/successor/manifest.json").read_text(encoding="utf-8"))
    cases=list(m.get("baseline_cases",[])); ids={f"{i:03d}-" for i in range(1,8)}
    if include_summary: ids.add("008-")
    for task in m["tasks"]:
        if any(task["id"].startswith(p) for p in ids): cases.extend({"name":c["name"],"input":c["input"],"expected":c["expected"]} for c in task.get("cases",[]))
    if level=="expanded":
        ex=json.loads((root/"benchmarks/workstream-h/public-examples.json").read_text(encoding="utf-8"))["examples"]
        cases.extend({"name":x["name"],"input":x["request"],"expected":x["response"]} for x in ex)
        neutral = [
          ("private reconcile left nonarray", {"operation":"reconcile","left":1}, {"error":"left must be an array"}),
          ("private reconcile right nonarray", {"operation":"reconcile","left":[],"right":{}}, {"error":"right must be an array"}),
          ("private reconcile invalid record", {"operation":"reconcile","left":[None]}, {"error":"invalid left record"}),
          ("private reconcile invalid id", {"operation":"reconcile","left":[{"priority":1,"createdAt":"2024-01-01T00:00:00Z"}]}, {"error":"invalid left id"}),
          ("private reconcile string priority", {"operation":"reconcile","left":[{"id":"x","priority":"1","createdAt":"2024-01-01T00:00:00Z"}]}, {"error":"invalid left priority"}),
          ("private reconcile bool priority", {"operation":"reconcile","left":[{"id":"x","priority":True,"createdAt":"2024-01-01T00:00:00Z"}]}, {"error":"invalid left priority"}),
          ("private reconcile float priority", {"operation":"reconcile","left":[{"id":"x","priority":1.0,"createdAt":"2024-01-01T00:00:00Z"}]}, {"error":"invalid left priority"}),
          ("private reconcile priority overflow", {"operation":"reconcile","left":[{"id":"x","priority":2147483648,"createdAt":"2024-01-01T00:00:00Z"}]}, {"error":"invalid left priority"}),
          ("private reconcile invalid date", {"operation":"reconcile","left":[{"id":"x","priority":1,"createdAt":"2024-02-30T00:00:00Z"}]}, {"error":"invalid left createdAt"}),
          ("private reconcile date spelling", {"operation":"reconcile","left":[{"id":"x","priority":1,"createdAt":"2024-01-01t00:00:00z"}]}, {"error":"invalid left createdAt"}),
          ("private reconcile offset overflow", {"operation":"reconcile","left":[{"id":"x","priority":1,"createdAt":"2024-01-01T00:00:00+14:01"}]}, {"error":"invalid left createdAt"}),
          ("private reconcile duplicate after later invalid", {"operation":"reconcile","left":[{"id":"x","priority":1,"createdAt":"2024-01-01T00:00:00Z"},{"id":"x","priority":1}]}, {"error":"invalid left createdAt"}),
          ("private reconcile right invalid after left duplicate", {"operation":"reconcile","left":[{"id":"x","priority":1,"createdAt":"2024-01-01T00:00:00Z"},{"id":"x","priority":1,"createdAt":"2024-01-01T00:00:00Z"}],"right":[None]}, {"error":"invalid right record"}),
          ("private dependency ids nonarray", {"operation":"dependencyOrder","ids":1}, {"error":"invalid ids"}),
          ("private dependency ids null element", {"operation":"dependencyOrder","ids":[None]}, {"error":"invalid ids"}),
          ("private dependency edges nonarray", {"operation":"dependencyOrder","ids":[],"edges":1}, {"error":"invalid edges"}),
          ("private dependency missing edge field", {"operation":"dependencyOrder","ids":["a"],"edges":[{"before":"a"}]}, {"error":"invalid edge"}),
          ("private dependency edge duplicate after malformed", {"operation":"dependencyOrder","ids":["a","b"],"edges":[{"before":"a","after":"b"},{"before":"a"}]}, {"error":"invalid edge"}),
          ("private dependency unknown", {"operation":"dependencyOrder","ids":["a"],"edges":[{"before":"a","after":"b"}]}, {"error":"unknown dependency"}),
          ("private dependency self", {"operation":"dependencyOrder","ids":["a"],"edges":[{"before":"a","after":"a"}]}, {"error":"self dependency"}),
          ("private dependency cycle", {"operation":"dependencyOrder","ids":["a","b"],"edges":[{"before":"a","after":"b"},{"before":"b","after":"a"}]}, {"error":"dependency cycle"}),
          ("private dependency ready ordinal", {"operation":"dependencyOrder","ids":["b","a","c"],"edges":[{"before":"a","after":"c"}]}, {"ids":["a","b","c"]}),
          ("private unicode case ids", {"operation":"dependencyOrder","ids":["A","a","Å"],"edges":[]}, {"ids":["A","a","Å"]}),
        ]
        cases.extend({"name":n,"input":i,"expected":e} for n,i,e in neutral)
        if include_summary:
            summary = [
              ("target summary boundary equal not overdue", {"operation":"summary","asOf":"2026-02-10T00:00:00Z","orders":[{"status":"pending","dueAt":"2026-02-10T00:00:00Z"}]}, {"pending":1,"processing":0,"completed":0,"cancelled":0,"overdue":0}),
              ("target summary null array elements", {"operation":"summary","orders":[None,None]}, {"pending":0,"processing":0,"completed":0,"cancelled":0,"overdue":0}),
              ("target summary mixed case and unknown", {"operation":"summary","asOf":"2026-02-10T00:00:00Z","orders":[{"status":"PeNdInG","dueAt":"2026-02-09T00:00:00Z"},{"status":"unknown","dueAt":"2026-02-01T00:00:00Z"}]}, {"pending":1,"processing":0,"completed":0,"cancelled":0,"overdue":1}),
              ("target summary null asOf", {"operation":"summary","asOf":None,"orders":[{"status":"pending","dueAt":"2020-01-01T00:00:00Z"}]}, {"pending":1,"processing":0,"completed":0,"cancelled":0,"overdue":0}),
            ]
            cases.extend({"name":n,"input":i,"expected":e} for n,i,e in summary)
        cases += [
          {"name":"private Int32 extremes","input":{"operation":"reconcile","left":[{"id":"x","priority":-2147483648,"createdAt":"0001-01-01T00:00:00Z"}],"right":[{"id":"x","priority":2147483647,"createdAt":"9999-12-31T23:59:59.9999999Z"}]},"expected":{"items":[{"id":"x","origin":"right"}]}},
          {"name":"private dependency cycle","input":{"operation":"dependencyOrder","ids":["a","b"],"edges":[{"before":"a","after":"b"},{"before":"b","after":"a"}]},"expected":{"error":"dependency cycle"}},
          {"name":"private subsecond tie","input":{"operation":"reconcile","left":[{"id":"x","priority":1,"createdAt":"2024-01-01T00:00:00.0000001Z"}],"right":[{"id":"x","priority":1,"createdAt":"2024-01-01T00:00:00Z"}]},"expected":{"items":[{"id":"x","origin":"left"}]}}
        ]
    return cases
