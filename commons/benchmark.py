"""Run the demo benchmark and write full, unfiltered results.

Usage (no dependencies, Python 3.10+):
    python3 benchmark.py

Outputs, in this directory:
    results.csv  -- one row per agent per seed per policy (full data)
    RESULTS.md   -- mean +/- std across seeds, plus the full per-seed
                    table. No runs are excluded, no seeds are dropped,
                    and no per-seed split is collapsed into a summary
                    alone. If a cropped view is ever shown elsewhere,
                    this file is the full version it must link to.

Policies and seeds are fixed here so a rerun reproduces the table.
"""

from __future__ import annotations

import csv
import statistics
from pathlib import Path

from golden_directive import POLICIES, run_episode

HERE = Path(__file__).resolve().parent
SEEDS = [42, 43, 44, 45, 46]


def main() -> None:
    rows = []
    per_seed = {}  # (policy, seed) -> dict of means
    for policy in POLICIES:
        for seed in SEEDS:
            result = run_episode(policy, seed)
            for agent in result["agents"]:
                rows.append(
                    {
                        "policy": policy,
                        "seed": seed,
                        "agent": agent["agent"],
                        "A_harvest": agent["A"],
                        "E_resource_final_stock": agent["E_resource"],
                        "E_social_mean_others": round(agent["E_social"], 2),
                        "Y_resource": round(agent["Y_resource"], 2),
                        "Y_social": round(agent["Y_social"], 2),
                    }
                )
            agents = result["agents"]
            per_seed[(policy, seed)] = {
                "mean_A": sum(a["A"] for a in agents) / len(agents),
                "mean_Y_resource": sum(a["Y_resource"] for a in agents) / len(agents),
                "mean_Y_social": sum(a["Y_social"] for a in agents) / len(agents),
                "final_stock": result["final_stock"],
                "total_harvest": result["total_harvest"],
            }

    with open(HERE / "results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    lines = []
    lines.append("# Demo benchmark results")
    lines.append("")
    lines.append("Warning: E in this demo is a bounded proxy (apples remaining,")
    lines.append("mean other agents' harvest), not true E. See README.")
    lines.append("")
    lines.append("Full data: `results.csv` (one row per agent per seed per policy).")
    lines.append("No runs excluded. No seeds dropped.")
    lines.append("")
    lines.append("## Summary across seeds (mean +/- sample std, n=5 seeds)")
    lines.append("")
    lines.append("| Policy | Mean A | Mean Y_resource | Mean Y_social | Mean final stock |")
    lines.append("|---|---|---|---|---|")
    for policy in POLICIES:
        vals = [per_seed[(policy, s)] for s in SEEDS]

        def mean_std(key: str) -> str:
            xs = [v[key] for v in vals]
            return f"{statistics.mean(xs):.2f} +/- {statistics.stdev(xs):.2f}"

        lines.append(
            f"| {policy} | {mean_std('mean_A')} | {mean_std('mean_Y_resource')} "
            f"| {mean_std('mean_Y_social')} | {mean_std('final_stock')} |"
        )
    lines.append("")
    lines.append("## Full per-seed table (mean across the 4 agents in that run)")
    lines.append("")
    lines.append("| Policy | Seed | Mean A | Mean Y_resource | Mean Y_social | Final stock | Total harvest |")
    lines.append("|---|---|---|---|---|---|---|")
    for policy in POLICIES:
        for seed in SEEDS:
            v = per_seed[(policy, seed)]
            lines.append(
                f"| {policy} | {seed} | {v['mean_A']:.2f} | {v['mean_Y_resource']:.2f} "
                f"| {v['mean_Y_social']:.2f} | {v['final_stock']} | {v['total_harvest']} |"
            )
    lines.append("")
    lines.append("## How to read this honestly")
    lines.append("")
    lines.append("- Y_resource rewards a policy only if it both harvests and leaves stock.")
    lines.append("- Y_social rewards a policy only if it both harvests and others harvest.")
    lines.append("- A toy with fixed rules is not evidence that training on Y works.")
    lines.append("  That claim would need a real multi-agent benchmark (see README).")
    (HERE / "RESULTS.md").write_text("\n".join(lines) + "\n")
    print(f"Wrote {HERE / 'results.csv'} and {HERE / 'RESULTS.md'}")


if __name__ == "__main__":
    main()
