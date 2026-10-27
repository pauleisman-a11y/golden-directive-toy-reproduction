"""Run the Clean Up-style toy benchmark.

Usage: python3 benchmark_cleanup.py
Writes results_cleanup.csv and RESULTS_CLEANUP.md in this directory.
No runs excluded, no seeds dropped. See cleanup_demo.py for rules.
"""

from __future__ import annotations

import csv
import statistics
from pathlib import Path

from cleanup_demo import POLICIES_CLEANUP, run_cleanup_episode

HERE = Path(__file__).resolve().parent
SEEDS = [42, 43, 44, 45, 46]


def main() -> None:
    rows = []
    per_seed = {}
    for policy in POLICIES_CLEANUP:
        for seed in SEEDS:
            result = run_cleanup_episode(policy, seed)
            for agent in result["agents"]:
                rows.append(
                    {
                        "policy": policy,
                        "seed": seed,
                        "agent": agent["agent"],
                        "A_harvest": agent["A"],
                        "E_stock_final_stock": agent["E_stock"],
                        "E_clean_final_cleanliness": agent["E_clean"],
                        "E_social_mean_others": round(agent["E_social"], 2),
                        "Y_stock": round(agent["Y_stock"], 2),
                        "Y_clean": round(agent["Y_clean"], 2),
                        "Y_social": round(agent["Y_social"], 2),
                    }
                )
            agents = result["agents"]
            per_seed[(policy, seed)] = {
                "mean_A": sum(a["A"] for a in agents) / len(agents),
                "mean_Y_stock": sum(a["Y_stock"] for a in agents) / len(agents),
                "mean_Y_clean": sum(a["Y_clean"] for a in agents) / len(agents),
                "mean_Y_social": sum(a["Y_social"] for a in agents) / len(agents),
                "final_stock": result["final_stock"],
                "final_cleanliness": result["final_cleanliness"],
                "total_harvest": result["total_harvest"],
            }

    with open(HERE / "results_cleanup.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# Clean Up-style toy benchmark results",
        "",
        "Warning: E_clean is cleanliness points (0-100), not apples.",
        "Y_clean mixes those scales. See cleanup_demo.py.",
        "",
        "Full data: `results_cleanup.csv`. No runs excluded.",
        "",
        "## Summary across seeds (mean +/- sample std, n=5 seeds)",
        "",
        "| Policy | Mean A | Mean Y_stock | Mean Y_clean | Mean final stock | Mean final cleanliness |",
        "|---|---|---|---|---|---|",
    ]
    for policy in POLICIES_CLEANUP:
        vals = [per_seed[(policy, s)] for s in SEEDS]

        def mean_std(key: str) -> str:
            xs = [v[key] for v in vals]
            return f"{statistics.mean(xs):.2f} +/- {statistics.stdev(xs):.2f}"

        lines.append(
            f"| {policy} | {mean_std('mean_A')} | {mean_std('mean_Y_stock')} "
            f"| {mean_std('mean_Y_clean')} | {mean_std('final_stock')} "
            f"| {mean_std('final_cleanliness')} |"
        )
    lines += [
        "",
        "## Full per-seed table (mean across the 4 agents in that run)",
        "",
        "| Policy | Seed | Mean A | Mean Y_stock | Mean Y_clean | Final stock | Final cleanliness | Total harvest |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for policy in POLICIES_CLEANUP:
        for seed in SEEDS:
            v = per_seed[(policy, seed)]
            lines.append(
                f"| {policy} | {seed} | {v['mean_A']:.2f} | {v['mean_Y_stock']:.2f} "
                f"| {v['mean_Y_clean']:.2f} | {v['final_stock']} | {v['final_cleanliness']} "
                f"| {v['total_harvest']} |"
            )
    lines += [
        "",
        "This toy, like the Harvest toy, is not evidence that training",
        "on Y works. See README, 'What would change my mind'.",
    ]
    (HERE / "RESULTS_CLEANUP.md").write_text("\n".join(lines) + "\n")
    print(f"Wrote {HERE / 'results_cleanup.csv'} and {HERE / 'RESULTS_CLEANUP.md'}")


if __name__ == "__main__":
    main()
