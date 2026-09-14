"""Read-only P09 released-CSV audit; original code, no author program execution.

Usage: python artifact_csv_check.py /path/to/experiment_instance_costs_sweagent.csv
The source is pinned below. Missing rows/costs are never imputed as zero.
This verifies membership/counts/accounting columns, not paper bootstrap results.
"""

import csv
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path
import sys

SOURCE = ("https://raw.githubusercontent.com/JetBrains-Research/the-complexity-trap/"
          "bf15b5fb7d279679035a007ac9a81084d6b9a89a/"
          "auxiliary-data/experiment_instance_costs_sweagent.csv")


def finite_number(value):
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def audit(path):
    groups = defaultdict(list)
    with path.open(encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            groups[row["experiment"]].append(row)
    output = []
    for name, rows in sorted(groups.items()):
        ids = {r["instance_id"] for r in rows}
        cost = [finite_number(r["cost"]) for r in rows]
        summary = [finite_number(r["summary_cost"]) for r in rows]
        totals = [a+b if a is not None and b is not None else None
                  for a, b in zip(cost, summary)]
        record = {"experiment": name, "rows": len(rows), "unique_ids": len(ids),
                  "duplicate_ids": len(rows)-len(ids),
                  "passes": sum(int(r["outcome"]) for r in rows)}
        for label, values in [("cost", cost), ("summary_cost", summary), ("combined_cost", totals)]:
            known = [v for v in values if v is not None]
            record[label] = {"known_rows": len(known),
                             "mean_on_known": sum(known)/len(known) if known else None}
        output.append(record)
    # Descriptive, same-ID check for the 50-instance hybrid against released main baselines.
    hybrid_name = next(name for name in groups if 'summary_N_43_' in name)
    hybrid = {r['instance_id']: r for r in groups[hybrid_name]}
    matched = []
    for name, rows in sorted(groups.items()):
        if 'Coder_480B_A35B' not in name:
            continue
        baseline = {r['instance_id']: r for r in rows}
        common = sorted(hybrid.keys() & baseline.keys())
        matched.append({'baseline': name, 'common_ids': len(common),
                        'hybrid_passes': sum(int(hybrid[k]['outcome']) for k in common),
                        'baseline_passes': sum(int(baseline[k]['outcome']) for k in common),
                        'hybrid_only_passes': sum(int(hybrid[k]['outcome']) == 1 and int(baseline[k]['outcome']) == 0 for k in common),
                        'baseline_only_passes': sum(int(hybrid[k]['outcome']) == 0 and int(baseline[k]['outcome']) == 1 for k in common)})
    return {"source_url": SOURCE, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "scope": "Released CSV rows only; no missing-row imputation or paired inference.",
            "groups": output, "hybrid_N43_common_id_comparisons": matched}


if __name__ == "__main__":
    print(json.dumps(audit(Path(sys.argv[1])), indent=2, allow_nan=False))
