# S102 — Document evolution, translated edits and compatibility policy

**Complete report text, appendices and static-figure reading, 2026-10-03.** Geoffrey Litt, Peter van Hardenberg and Orion Henry, [*Project Cambria: Translate your data with lenses*](https://www.inkandswitch.com/cambria/), Ink & Switch, **October 2020**. This is a primary research/practitioner report, not a peer-reviewed controlled maintenance study. Existing native parent **`BXMUAADU`**, note **`VQFZKCEC`** and linked attachment **`N3WEUULR`** precede this reading; four collection memberships, including `PKLXQNEE`, are preserved.

## Source and coverage

The retrieved HTML is **100,836 bytes**, SHA-256 **`e12356e1721cef2c0c2f1aec8dda7679432aa730a94f43783e284571488c7f4d`**, MD5 **`aa362d3a6de86cc4ed736522a3b5bead`**. The lead/title/authorship and **all 861 extracted article lines, 64,618 characters**, including Findings, all open questions and **Appendices I–III**, are read. This is the report as served on 3 October 2026, not a certified byte-identical October 2020 snapshot.

All **nine static images** are inspected: six SVG diagrams, two JPEGs and the TypeScript diagnostic PNG. These include two decorative images. All code inputs and the compatibility table are read; dynamically computed output panes are not rerun. Four silent embedded clips are acquired, with **six timestamped frames per clip** inspected. This is 24 sampled frames, not continuous playback, a latency measurement or a reproduced collaboration session.

Bounded public-source inspection adds **15 complete files (2,392 lines)**, one test-file range, one lockfile range and six dependency-version comparisons. No library, compiler, test suite, issue tracker, page demo, model or networked collaboration application is executed. Acquisition/rendering and static reading are separate from reproduction.

## Mechanism: versions describe edits as well as data

Cambria isolates declared schema transformations from application code. A lens specification can transform JSON documents, JSON Patch edits and JSON Schema definitions; a build workflow also generates TypeScript types. The developer supplies field correspondence and conversion policy. A graph connects schemas with forward/reverse transformations, and a shortest available path composes translations between versions. Old clients need access to the lens descriptions and must understand their operators.

The examples establish concrete capabilities:

| Change | Declared policy and implication |
| --- | --- |
| Rename a field | Rewrite the field and supported patch paths while updating its schema. A type diagnostic can locate a stale property access, but cannot establish the correctness of every associated behavioral change. |
| Boolean completion → three-valued status | Supply **both** value maps. Two new statuses map to the same old Boolean; an old client cannot expose their distinction. This is a useful many-to-one policy, not automatic recovery of intent. |
| Optional scalar assignee → array of assignees | The old client observes the first array element; a scalar write targets that position. More than one assignee remains only partially visible in the old UI. Deletion requires a separate policy. |
| Add a tags array | Supply a schema/default so older documents yield an empty array. Generated static and runtime schemas reduce duplicated declarations, under the supported transformation and input assumptions. |
| Nesting/hoisting and element mapping | Explicit operators move structure and apply inner transformations. Transforming an identifier into an external account or invoice still requires application logic and data lookup. |

The core library translates **patches**; whole-document translation converts a document into patches, transforms them, then applies them to a target/base document. An optional supplied target can retain fields omitted by a particular view. Without such retained state, defaulting a removed field is not recovery of its old value. This differs from InVerDa's explicit auxiliary relational complements and from retaining the full original operation log in Cambria-Automerge.

The positive workflow account comes from the authors using an evolving issue tracker over several months. They found the shared source for translations, TypeScript types and runtime schemas reassuring and development smoother. Preserve that experience. The tracker was also too unstable to be their sole system of record while Cambria's own storage format changed. Neither statement is a controlled participant-time or defect-rate comparison.

## A valid schema is weaker than preserved meaning

Appendix I describes two edit-lens obligations: valid source edits translate into valid target edits, and applying the corresponding edits preserves a chosen relation between views. The report does not supply a complete formal proof for Cambria. It explicitly says that its general `convert` operator can violate the technical lens definition because authors may supply unrelated directional maps.

Findings identifies three desired properties: related views, avoiding changes to unseen information, and preserving the local meaning of an operation. The scalar/list example exposes a conflict. Clearing the whole list honors the old client's empty result but removes hidden assignees; removing only the first element reveals another assignee, surprising the old client; preserving a null at the head requires nullable list elements.

Appendix III **expressly reports a defective current implementation**: clearing the scalar removes the list head while leaving the old view empty even though the newer view retains more entries. Further edits can overwrite or remove unseen data. This is author-reported adverse evidence, not a failure generated by this inspection. The illustrative later line unexpectedly introduces “Sue” after a Bob/Charlie list; that literal name inconsistency is not treated as a separately observed trace.

The appendix compares six policy families: give the scalar complete control, use a nullable head register, clear the list only on null, pop the head, expose distinct clear/remove operations, or make the policy configurable. They are alternatives with different intent/visibility costs, not six implemented solutions. The report's nonnullable-scalar limitation is tied to an array that may become empty under its distributed model; it should not be generalized into a theorem that all possible scalar/collection conversions are impossible.

This matters to Nu's claims about explicit state and types: a visible value, a type-correct value and a value preserving the intended user action are separate. A fallback/default or a cleared type diagnostic cannot choose the intended deletion, ownership or temporal policy by itself.

## Persistent collaboration adds identity and history obligations

Appendix II separates the patch library from its **Automerge/Hypermerge integration**. Core Cambria supplies no independent storage or conflict-resolution protocol.

The integration records original changes tagged with their **writer schema**, storing lens descriptions when a document first uses a new schema. To construct a reader's view, it translates each change to the desired schema and applies the resulting log. Earlier eager translation on write struggled with later-added schemas, concurrent schema registration and unnecessary work; preserving original writes permits later interpretation with newly known lenses.

The concrete translation path is:

`Automerge operation and object identity → JSON Patch path → lensed path/value → reader-schema Automerge operation`

Object IDs and list-element IDs cannot be replaced by path strings without state. The adapter reconstructs the writer view at the relevant history position and maintains reader state while translating successive operations. A single requested schema may therefore require reconstruction of several schemas. In the inspected code, `getInstanceAt` replays the recorded history prefix before the selected actor/sequence entry; this code path is not a proof of correct correspondence under every possible concurrent arrival order.

The report describes ordinary Automerge convergence, but leaves **the interaction between lens guarantees and differing CRDT scalar/list conflict rules open**. A shared log is useful infrastructure; the published account does not establish that arbitrary translated operations preserve both cross-schema consistency and user intent under all concurrent schedules.

The adapter's README/code add specific integration premises:

- It is an alternate **Automerge 0.14 backend**, with the package fixing **0.14.1**, designed for an experimental Hypermerge branch. The authors report difficulty integrating the then-newer 1.0 representation because generated changes disturb encoding, hashes/dependencies and operation IDs.
- Deterministic defaults are represented by a **phantom bootstrap change** under a fixed actor, hidden from external clocks/dependencies. Peers need identical default generation for this mechanism.
- Generated object IDs depend on the originating change/operation; generated list IDs use per-actor counters. The README acknowledges repeated element IDs across different sequences and relies on their remaining separate.
- Translation reconstructs and incrementally applies intermediate states; a code comment identifies repeated application work. Neither the report nor this read measures its total runtime, memory or storage overhead.

Lens syntax itself must also evolve. The report names portable execution, recursive/named lenses, missing external data, cross-document changes, additional operators and shared lens repositories as open work. An old client receiving lens data is not automatically able to execute a future unknown primitive.

## What the source verifies

Core pin **`da8961440cac7eba1c3113488f5bcbc26046620f`** is dated **5 March 2021**, with package **0.1.2**. Adapter pin **`75f3b67558055687bd8dfd28edad6fe03bc82fed`** is dated **27 August 2020**, with package **0.0.3**. Both repository trees are completely inventoried at **83** and **30** entries, without truncation; this does not mean every file is read.

The following findings are static, source-located evidence:

1. Core `patch.ts` expands object-setting patches, applies the lens operations, derives the reader schema and adds defaults. Its `rename` path explicitly handles add/replace while leaving other JSON Patch verbs as TODOs. Thus the advertised JSON Patch interface should not be read as a verified implementation of every standard operation.
2. `wrap` converts a top-level null write into removal of element zero; `head` converts removal of element zero into a null scalar write and ignores non-head writes. The selected tests assert these local outputs. A separate array-edit test supplies an explicit replacement with the new head; passing such a conversion assertion would not establish the general two-view invariant. No tests are run here.
3. The schema interpreter rejects wrapping a nonnullable scalar and gives the array nonnull items. Its reverse `head` schema is nullable. This rules out treating the nullable-head-register alternative as the implemented default.
4. `convert` performs explicit directional table lookup and throws for a missing key. Swapping its maps is not validation of their semantic correspondence. The illustrated mapping's `default` entry is not implemented as a general fallback in this source.
5. The graph registers reverse edges and uses Dijkstra traversal. An existing edge is returned without checking equal lens definitions; at the inspected head, an existing destination schema is also not rederived/checked. These routines do not certify path-independent transformations around arbitrary graph cycles.
6. Whole-document conversion applies transformed patches to generated defaults plus an optional target document, using a shallow base merge. Retention through that base is distinct from a general lossless round trip without retained information.

The adapter lockfile resolves **Cambria 0.1.1 at `332b06ba2f1f272a59432963cb1b3e0e31437d82`**, not the inspected later head. Six relevant files are compared: reverse/default/schema files are byte-identical; document conversion differs in comments/imports; graph registration and nested `in`/`map` patch suppression have substantive changes. The scalar/head/null policy is unchanged in the compared patch text. Do not silently substitute the later core into the older adapter or claim either pin reproduces the published video.

## Evidence disposition and next action

S102 supplies a useful predecessor for maintaining multiple document schemas, generating related type/validation artifacts, and translating retained edits for differently versioned applications. Its positive demonstrations and subjective developer experience are primary evidence at those scopes. The acknowledged deletion inconsistency, prototype instability and unanswered CRDT/lens interaction are equally material evidence.

The report **explicitly has no formal performance measurement**. Broader SQL/document-database and service-integration proposals are potential applications, not deployments tested by this work. In particular, its claim of not knowing a PostgreSQL multiple-schema/lens implementation does not establish absence: the already reconstructed S103/S236 lineage supplies a relational predecessor with different assumptions. The report also cannot establish net human/agent maintenance savings, a Nu/F# advantage, external-effect rollback or arbitrary running-program migration.

The next consequential source is **S87 Denicek**, already registered/acquired but partially read. It combines document data and computations, so it can clarify how program/dependency evolution changes this representation-level contract. It shares authors/problem lineage with completed S73/S86 and must not be counted as independent validation of that motivation. Modern .NET/game and type/context/multi-turn frontiers remain separate; all experiments and construction remain held.

SC154's exact-title search requests **limit20/offset0** and returns **zero records**. This is an exact-title discovery limit for a web report, not evidence of scientific absence. W460 retrieves the report and its direct media; W461 follows its public core/adapter links and pinned source. No citation graph, incoming-statement review or new Consensus page is claimed.

## Auditable source identities

All bodies, clips, extracted text and rendered frames remain in ignored local reading storage. These hashes identify retrieved inputs; they do not certify executed behavior.

| Core file at the 2021 pin | Bytes / lines / coverage | SHA-256 |
| --- | --- | --- |
| [README.md](https://raw.githubusercontent.com/inkandswitch/cambria/da8961440cac7eba1c3113488f5bcbc26046620f/README.md) | 3286 / 78 / complete | `fb9f7dcfa5039b3f3af603f592686c1085ab6bacd7c24eba861774c2fcf0519d` |
| [package.json](https://raw.githubusercontent.com/inkandswitch/cambria/da8961440cac7eba1c3113488f5bcbc26046620f/package.json) | 1277 / 43 / complete | `2c96312d2bc0564a6b3a227ba5b2d1fe6d4b8f0844d384e1ff2a5a0941e05aa3` |
| [src/lens-graph.ts](https://raw.githubusercontent.com/inkandswitch/cambria/da8961440cac7eba1c3113488f5bcbc26046620f/src/lens-graph.ts) | 2351 / 82 / complete | `fdfd008b8c7c5f177fa985b9d8bb3796a6e7197023175706dbb7e18639b068a5` |
| [src/reverse.ts](https://raw.githubusercontent.com/inkandswitch/cambria/da8961440cac7eba1c3113488f5bcbc26046620f/src/reverse.ts) | 1412 / 76 / complete | `27e71218e7edb02576139ff95a5273ebf66cb992071714743631827a0346b5ca` |
| [src/patch.ts](https://raw.githubusercontent.com/inkandswitch/cambria/da8961440cac7eba1c3113488f5bcbc26046620f/src/patch.ts) | 7938 / 245 / complete | `a87774a206b073d875825ee217843df9a963db483952808305dd72257e8f0bd9` |
| [src/defaults.ts](https://raw.githubusercontent.com/inkandswitch/cambria/da8961440cac7eba1c3113488f5bcbc26046620f/src/defaults.ts) | 4477 / 124 / complete | `13fc5628c476bd4f2e867b1c2fc8e5c549168daaa3f716361e4ddc5eb8da5fbf` |
| [src/doc.ts](https://raw.githubusercontent.com/inkandswitch/cambria/da8961440cac7eba1c3113488f5bcbc26046620f/src/doc.ts) | 2908 / 71 / complete | `2d171216982a24c1e83b22d6c938682d3a9fa0bc75e149102bfbe27ff4f81515` |
| [src/json-schema.ts](https://raw.githubusercontent.com/inkandswitch/cambria/da8961440cac7eba1c3113488f5bcbc26046620f/src/json-schema.ts) | 14612 / 510 / complete | `758d3d377abef502428369da478ead93fa0821bbfc138309948f09e843e30eb6` |
| [src/lens-loader.ts](https://raw.githubusercontent.com/inkandswitch/cambria/da8961440cac7eba1c3113488f5bcbc26046620f/src/lens-loader.ts) | 1071 / 37 / complete | `8b39da45b72915ca629e42e99272ded047aca68199e3af9d1625132d2e82d10e` |
| [src/lens-ops.ts](https://raw.githubusercontent.com/inkandswitch/cambria/da8961440cac7eba1c3113488f5bcbc26046620f/src/lens-ops.ts) | 1613 / 85 / complete | `3a658f3f32eb53c7d26e56034fa368d0b0d79a9f63b2cc2a4af8aceddedccaef` |
| [src/index.ts](https://raw.githubusercontent.com/inkandswitch/cambria/da8961440cac7eba1c3113488f5bcbc26046620f/src/index.ts) | 752 / 25 / complete | `c1c2cae84977e0dad0a41a30df53f517f30f6301234d77bade68ec8e77793b16` |
| [test/patch.ts](https://raw.githubusercontent.com/inkandswitch/cambria/da8961440cac7eba1c3113488f5bcbc26046620f/test/patch.ts) | 26021 / 1042 / 434–718 only | `71c6d229352582ee299b2d1fd1be194abe03746d68b47a55317e08015834a770` |

| Adapter file at the 2020 pin | Bytes / lines / coverage | SHA-256 |
| --- | --- | --- |
| [README.md](https://raw.githubusercontent.com/inkandswitch/cambria-automerge/75f3b67558055687bd8dfd28edad6fe03bc82fed/README.md) | 3362 / 79 / complete | `764cda94d3ad44cdfe3fd0174f66445edb51e9c632fcefb24f296dc2349ad472` |
| [package.json](https://raw.githubusercontent.com/inkandswitch/cambria-automerge/75f3b67558055687bd8dfd28edad6fe03bc82fed/package.json) | 1045 / 37 / complete | `64445c564585f104239f8aee002e7f436b281e3b98c92f6d819ae6630717ed9b` |
| [src/cambriamerge.ts](https://raw.githubusercontent.com/inkandswitch/cambria-automerge/75f3b67558055687bd8dfd28edad6fe03bc82fed/src/cambriamerge.ts) | 27825 / 858 / complete | `7cc0e734afbc8797f8bc52727c31e087501893fe24b73dc542a48c20e835f681` |
| [src/index.ts](https://raw.githubusercontent.com/inkandswitch/cambria-automerge/75f3b67558055687bd8dfd28edad6fe03bc82fed/src/index.ts) | 763 / 42 / complete | `27feb05908b97f7cd0cb2838e865ec44967bd88b1dbc273c11a0690abef785bd` |
| [yarn.lock](https://raw.githubusercontent.com/inkandswitch/cambria-automerge/75f3b67558055687bd8dfd28edad6fe03bc82fed/yarn.lock) | 102498 / 2335 / 352–361 only | `6ce629e2421f3ca6da488d2b9910ef2041ddae3c7ffbb4ea11a74e83cbef2778` |

| Core file at the lock-resolved 0.1.1 pin | Comparison coverage | SHA-256 |
| --- | --- | --- |
| [src/lens-graph.ts](https://raw.githubusercontent.com/inkandswitch/cambria/332b06ba2f1f272a59432963cb1b3e0e31437d82/src/lens-graph.ts) | Complete textual diff inspected against read file | `acbd28235f83608d472ad1b29c563d79f1f96c86c4bbb1ff8d1adbec0ce375ed` |
| [src/reverse.ts](https://raw.githubusercontent.com/inkandswitch/cambria/332b06ba2f1f272a59432963cb1b3e0e31437d82/src/reverse.ts) | Byte-identical to read file | `27e71218e7edb02576139ff95a5273ebf66cb992071714743631827a0346b5ca` |
| [src/patch.ts](https://raw.githubusercontent.com/inkandswitch/cambria/332b06ba2f1f272a59432963cb1b3e0e31437d82/src/patch.ts) | Complete textual diff inspected against read file | `9c4048cc1cfed35cb469372be7f5e3ce83a8b0a51ab804855d0ed9eb7beb295d` |
| [src/defaults.ts](https://raw.githubusercontent.com/inkandswitch/cambria/332b06ba2f1f272a59432963cb1b3e0e31437d82/src/defaults.ts) | Byte-identical to read file | `13fc5628c476bd4f2e867b1c2fc8e5c549168daaa3f716361e4ddc5eb8da5fbf` |
| [src/doc.ts](https://raw.githubusercontent.com/inkandswitch/cambria/332b06ba2f1f272a59432963cb1b3e0e31437d82/src/doc.ts) | Complete textual diff inspected against read file | `7a9f38f10979cc7aedf9a9d73893f7cab00ac0cd818239f90adf374ae7b9db92` |
| [src/json-schema.ts](https://raw.githubusercontent.com/inkandswitch/cambria/332b06ba2f1f272a59432963cb1b3e0e31437d82/src/json-schema.ts) | Byte-identical to read file | `758d3d377abef502428369da478ead93fa0821bbfc138309948f09e843e30eb6` |

| Report media | Bytes / visual coverage | SHA-256 |
| --- | --- | --- |
| [stripe-migration-stack.svg](https://www.inkandswitch.com/cambria/static/stripe-migration-stack.svg) | 2789 / static image complete | `c28644999f9086f2a3a8252c7c0fc6f796f5bca703ff3ff90acf274b3e5381e1` |
| [phacopida.jpg](https://www.inkandswitch.com/cambria/static/phacopida.jpg) | 88522 / static image complete | `e6779fe762cfdef30f1f3a353f851cbba184622176fd3107bb830f848ad4557d` |
| [lens-graph.svg](https://www.inkandswitch.com/cambria/static/lens-graph.svg) | 2001 / static image complete | `64912be4532df82d7204db1a8e770c6ea0f53a67629a471ed013dfcecca7be62` |
| [two-issue-trackers.jpg](https://www.inkandswitch.com/cambria/static/two-issue-trackers.jpg) | 94696 / static image complete | `a75fa9e452c3f93486da6a998b5a351617219de20294b47aedb951cad9fa428f` |
| [boolean-enum-2.mov](https://www.inkandswitch.com/cambria/static/boolean-enum-2.mov) | 1492439 / 8.816667 s; six sampled frames | `eb2e24a2e7112de98adedde369561ce465020228d9b34428e0b47e2426ea03d6` |
| [boolean-enum-1.mov](https://www.inkandswitch.com/cambria/static/boolean-enum-1.mov) | 884673 / 6.316667 s; six sampled frames | `d9fc7d321507d969291f789ada687a9524d3053ee528edb93570088b7d0b53d9` |
| [cambria-assignees-1.mov](https://www.inkandswitch.com/cambria/static/cambria-assignees-1.mov) | 2063061 / 12.883333 s; six sampled frames | `01e2308fa63c6c1dc1b1d45d4fd54137e0768320966c209390736d312c54f20b` |
| [cambria-assignees-2.mov](https://www.inkandswitch.com/cambria/static/cambria-assignees-2.mov) | 1343292 / 8.350000 s; six sampled frames | `dbb420614b1f8f154e7514b206f15db12c10f8f8d01b576b6acde2286a349384` |
| [lens-artifacts.svg](https://www.inkandswitch.com/cambria/static/lens-artifacts.svg) | 65058 / static image complete | `49edb3b03db1a62d705abbd56611b2747dd01d8bf64df1cd509cf8c182e5fc33` |
| [type-error.png](https://www.inkandswitch.com/cambria/static/type-error.png) | 14307 / static image complete | `9096989a0e9caa195548e2649a951449ae1269880eb0edc6865f1424d1caca75` |
| [darwin-tree-of-life.svg](https://www.inkandswitch.com/cambria/static/darwin-tree-of-life.svg) | 38681 / static image complete | `e1c4e29c9b7cfe761f1976a988e5ea620ef77dec57dc7a05155f9b66ed1fbdce` |
| [lensed-op-log.svg](https://www.inkandswitch.com/cambria/static/lensed-op-log.svg) | 5994 / static image complete | `688c888c1dcd06d9137db80120dd40a8a0e93630aaccba16836b8efff52d78f7` |
| [automerge-json-patch.svg](https://www.inkandswitch.com/cambria/static/automerge-json-patch.svg) | 3504 / static image complete | `e89213cef43613d7ffc3dd7457ec19b66f0918b80914b63e082e5f2659904ea9` |

Video samples are at 2%, 18%, 36%, 54%, 72% and 96% of each probed duration (rounded to milliseconds). No audio streams occur in the four clips. The frames show selected checkbox/status, single-assignee and first-of-multiple-assignees behavior; they do not cover every transition, the acknowledged repeated-deletion case or a concurrency/latency trial.
