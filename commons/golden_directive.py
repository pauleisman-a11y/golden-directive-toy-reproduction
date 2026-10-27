"""Golden Directive demo metric: Y = 2*A*E / (A + E).

This is a standalone, dependency-free demo. It does NOT train agents.
Policies below are fixed rules, so Y is observe-only here: it is
computed after a run and never changes what an agent harvests.

Disclosure (Paul Eisman's Golden Directive proposal):
  Y is the harmonic mean of A and E.
  A = an agent's contribution-health. In this demo, A is that agent's
      apples harvested in the episode.
  E = health of everything not that agent. True E is not knowable, so
      this demo uses two disclosed, bounded proxies, reported separately
      and never silently blended:
        E_resource = apples remaining in the shared patch at episode end
        E_social  = mean apples harvested by the other agents
  Both proxies are in apples, so they are on the same scale as A in
  this toy. That scale choice is arbitrary and is stated here, not hidden.

Rules, tested in test_golden_directive.py:
  - If A == 0 or E == 0, Y == 0 (collapse property).
  - If A == E, Y == A.
  - Otherwise Y lies strictly between A and E, pulled toward the
    smaller of the two (e.g. A=30, E=70 gives Y=42, not 30).
  - Negative A or E raises ValueError. There is no silent clip or shift.
"""

from __future__ import annotations

import random


def harmonic_mean(a: float, e: float) -> float:
    """Return 2*a*e/(a+e), with 0 if either input is 0.

    Negative inputs raise ValueError: the harmonic mean is not a
    meaningful welfare score for negative inputs, and silently
    clipping them would hide that.
    """
    if a < 0 or e < 0:
        raise ValueError("A and E must be non-negative")
    if a == 0 or e == 0:
        return 0.0
    return 2 * a * e / (a + e)


# Fixed harvesting rules. Base take per agent per round, before a
# seeded +/-1 variation. These are toy rules, not learned policies.
POLICIES = {
    "greedy": [5, 5, 5, 5],
    "moderate": [3, 3, 3, 3],
    "restrained": [2, 2, 2, 2],
    "mixed": [5, 5, 2, 2],  # 2 greedy agents, 2 restrained agents
}

INITIAL_STOCK = 100
ROUNDS = 20
REGROWTH_THRESHOLD = 20  # below this, the patch does not regrow
REGROWTH_RATE = 0.10


def run_episode(policy: str, seed: int) -> dict:
    """Run one toy commons episode and return per-agent A/E/Y values.

    Regrowth rule (arbitrary, stated here): after each round, if the
    remaining stock is at least REGROWTH_THRESHOLD, it grows by
    REGROWTH_RATE of the remaining stock, capped at INITIAL_STOCK.
    Below the threshold it does not regrow. This is a toy, not a
    model of any real resource.
    """
    if policy not in POLICIES:
        raise ValueError(f"unknown policy: {policy}")
    bases = POLICIES[policy]
    rng = random.Random(seed)
    stock = INITIAL_STOCK
    harvests = [0] * len(bases)

    for _round in range(ROUNDS):
        for i, base in enumerate(bases):
            if stock <= 0:
                break
            take = max(0, base + rng.choice((-1, 0, 1)))
            take = min(take, stock)
            harvests[i] += take
            stock -= take
        if stock >= REGROWTH_THRESHOLD:
            stock = min(INITIAL_STOCK, stock + int(REGROWTH_RATE * stock))

    agents = []
    for i, a in enumerate(harvests):
        others = [h for j, h in enumerate(harvests) if j != i]
        e_social = sum(others) / len(others) if others else 0.0
        agents.append(
            {
                "agent": i,
                "A": a,
                "E_resource": stock,
                "E_social": e_social,
                "Y_resource": harmonic_mean(a, stock),
                "Y_social": harmonic_mean(a, e_social),
            }
        )
    return {
        "policy": policy,
        "seed": seed,
        "final_stock": stock,
        "total_harvest": sum(harvests),
        "agents": agents,
    }
