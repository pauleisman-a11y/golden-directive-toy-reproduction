"""Clean Up-style toy: a public good, separate from the Harvest toy.

Rules, stated here (arbitrary, toy-only):
  - 4 agents, 20 rounds. River cleanliness C starts at 60 (0-100).
    Apple stock S starts at 40 (cap 100).
  - Cleaner: if C < 80, clean (C += 6, 8, or 10, seeded) and harvest 0;
    otherwise harvest 2 +/- 1.
  - Freeloader: never clean, harvest 3 +/- 1.
  - Moderate: clean on even rounds, harvest 2 +/- 1 on odd rounds.
  - Each harvest action reduces C by 2 (floor 0), each apple taken
    reduces S. After each round, S grows by int(C / 20) (0-5 apples).
  - A = apples harvested by that agent.
  - E_stock = final apple stock, in apples.
  - E_clean = final cleanliness, in cleanliness points (0-100).
    Y_clean therefore mixes apples with cleanliness points. That
    scale choice is disclosed here; Y_clean is not in pure apples.
  - Y_stock and Y_clean are reported separately, never blended.
  - Y is observe-only: it never changes an agent's action.
"""

from __future__ import annotations

import random

from golden_directive import harmonic_mean

POLICIES_CLEANUP = {
    "all_cleaners": ["cleaner"] * 4,
    "all_freeloaders": ["freeloader"] * 4,
    "mixed": ["cleaner", "cleaner", "freeloader", "freeloader"],
    "all_moderate": ["moderate"] * 4,
}

ROUNDS = 20
INITIAL_CLEANLINESS = 60
INITIAL_STOCK = 40


def run_cleanup_episode(policy: str, seed: int) -> dict:
    if policy not in POLICIES_CLEANUP:
        raise ValueError(f"unknown cleanup policy: {policy}")
    types = POLICIES_CLEANUP[policy]
    rng = random.Random(seed)
    cleanliness = INITIAL_CLEANLINESS
    stock = INITIAL_STOCK
    harvests = [0] * len(types)

    for round_no in range(ROUNDS):
        for i, kind in enumerate(types):
            action_clean = False
            if kind == "cleaner":
                action_clean = cleanliness < 80
            elif kind == "moderate":
                action_clean = round_no % 2 == 0
            if action_clean:
                cleanliness = min(100, cleanliness + rng.choice((6, 8, 10)))
                continue
            base = 3 if kind == "freeloader" else 2
            take = max(0, base + rng.choice((-1, 0, 1)))
            take = min(take, stock)
            harvests[i] += take
            stock -= take
            cleanliness = max(0, cleanliness - 2)
        stock = min(100, stock + int(cleanliness / 20))

    agents = []
    for i, a in enumerate(harvests):
        others = [h for j, h in enumerate(harvests) if j != i]
        e_social = sum(others) / len(others) if others else 0.0
        agents.append(
            {
                "agent": i,
                "A": a,
                "E_stock": stock,
                "E_clean": cleanliness,
                "E_social": e_social,
                "Y_stock": harmonic_mean(a, stock),
                "Y_clean": harmonic_mean(a, cleanliness),
                "Y_social": harmonic_mean(a, e_social),
            }
        )
    return {
        "policy": policy,
        "seed": seed,
        "final_stock": stock,
        "final_cleanliness": cleanliness,
        "total_harvest": sum(harvests),
        "agents": agents,
    }
