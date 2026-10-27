#!/usr/bin/env python3
"""Golden Directive — minimal demo training environment.

MINIMAL DEMO, NOT MAINTAINED AS A PRODUCT. Not a proof, not the
project's toy harness results, not a framework. A quick-start meter:
it shows what Y says, full-frame vs cropped-frame, under two fixed
policies. No learning agent is included; the training signal is Y
per step, and a learner plugged in here would optimize reported Y.

Spec (stated in full in README.md):
  Y = 2 * (A * E) / (A + E) — "you cannot survive what you destroy."
  A = net contribution-health score, floored at 0, from a resource
      ledger: actual units restored by tending minus actual units
      taken by eating (eating debited at 0.5 per unit, so one
      restore roughly offsets two taken — the ledger weights are
      part of this demo's spec, not measurements).
  E = health of everything not-A: total food stock / max stock * 100.
  If either A or E hits 0, Y hits 0.
  Cropped frame: E_crop counts ONLY food tiles in the home quadrant
      (x < 4 and y < 4) — one tile here — scaled to its own max.
      Damage outside that frame never enters E_crop.

Environment (deterministic, no randomness):
  8x8 grid, food tiles at (1,1) home, (1,6), (6,1), (6,6).
  Each tile: stock starts 5, max 10.
  Regrowth: +1 per step to each UNOCCUPIED food tile (cap 10).
      A tile the agent stands on does not regrow that step.
  Agent moves 1 step per step, x-first, toward its target tile.
  TEND restores up to 3 units (actual restore credited).
  EAT takes 1 unit (actual units debited at 0.5 each).
  Episode: 150 steps. Policies: tender, raider (see below).

Usage: python3 golden_demo.py
Output: per-policy means and finals, full vs cropped, plus the ledger.
"""

# --- Demo parameters (frozen; change them and the stated outputs change) ---
GRID = 8
FOOD_TILES = [(1, 1), (1, 6), (6, 1), (6, 6)]  # first tile is home
HOME = (1, 1)
TILE_MAX = 10
START_STOCK = 5
TEND_AMOUNT = 3
EAT_AMOUNT = 1
EAT_DEBIT = 0.5
REGROWTH = 1
A_START = 50.0
A_CAP = 100.0
EPISODE_STEPS = 150


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def step_toward(pos, target):
    """One Manhattan step toward target, x-first. Deterministic."""
    x, y = pos
    tx, ty = target
    if x != tx:
        return (x + (1 if tx > x else -1), y)
    if y != ty:
        return (x, y + (1 if ty > y else -1))
    return pos


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class Env:
    def __init__(self):
        self.stock = {t: START_STOCK for t in FOOD_TILES}
        self.pos = HOME
        self.ledger = A_START  # A before floor/cap; A = clamp(ledger, 0, 100)
        self.tends = 0
        self.eaten = 0

    @property
    def a(self):
        return clamp(self.ledger, 0.0, A_CAP)

    @property
    def e_full(self):
        return sum(self.stock.values()) / (len(FOOD_TILES) * TILE_MAX) * 100.0

    @property
    def e_crop(self):
        """Home quadrant only: tiles with x < 4 and y < 4, scaled to max."""
        home_tiles = [t for t in FOOD_TILES if t[0] < 4 and t[1] < 4]
        return sum(self.stock[t] for t in home_tiles) / (len(home_tiles) * TILE_MAX) * 100.0

    @staticmethod
    def y(a, e):
        if a <= 0 or e <= 0:
            return 0.0
        return 2.0 * a * e / (a + e)

    def regrow(self):
        for t in FOOD_TILES:
            if t != self.pos and self.stock[t] < TILE_MAX:
                self.stock[t] = min(TILE_MAX, self.stock[t] + REGROWTH)

    def act_tend(self):
        restored = min(TEND_AMOUNT, TILE_MAX - self.stock[self.pos])
        self.stock[self.pos] += restored
        self.ledger += restored
        self.tends += 1

    def act_eat(self):
        taken = min(EAT_AMOUNT, self.stock[self.pos])
        self.stock[self.pos] -= taken
        self.ledger -= EAT_DEBIT * taken
        self.eaten += taken


def run_policy(policy):
    """One 150-step episode. Returns per-step rows + totals."""
    env = Env()
    rows = []
    for _ in range(EPISODE_STEPS):
        # --- policy: pick target, then act or move ---
        if policy == "tender":
            # Lowest-stock tile (ties: fixed tile order). On a tile:
            # tend unless full, then eat 1 (subsistence).
            target = min(FOOD_TILES, key=lambda t: (env.stock[t], FOOD_TILES.index(t)))
            if env.pos == target:
                if env.stock[target] < TILE_MAX:
                    env.act_tend()
                else:
                    env.act_eat()
            else:
                env.pos = step_toward(env.pos, target)
        elif policy == "raider":
            # At home: tend unless full. At a far tile: eat until empty.
            # Else move toward home (if it needs tending) or the nearest
            # stocked far tile (ties: fixed tile order).
            if env.pos == HOME:
                if env.stock[HOME] < TILE_MAX:
                    env.act_tend()
                else:
                    far = [t for t in FOOD_TILES if t != HOME and env.stock[t] > 0]
                    if far:
                        target = min(far, key=lambda t: (dist(HOME, t), FOOD_TILES.index(t)))
                        env.pos = step_toward(env.pos, target)
            elif env.pos in FOOD_TILES:
                if env.stock[env.pos] > 0:
                    env.act_eat()
                else:
                    env.pos = step_toward(env.pos, HOME)
            else:
                if env.stock[HOME] < TILE_MAX:
                    env.pos = step_toward(env.pos, HOME)
                else:
                    far = [t for t in FOOD_TILES if t != HOME and env.stock[t] > 0]
                    if far:
                        target = min(far, key=lambda t: (dist(env.pos, t), FOOD_TILES.index(t)))
                        env.pos = step_toward(env.pos, target)
        else:
            raise ValueError(f"unknown policy: {policy}")
        env.regrow()
        a, ef, ec = env.a, env.e_full, env.e_crop
        rows.append((a, ef, ec, Env.y(a, ef), Env.y(a, ec)))
    return rows, env


def summarize(policy):
    rows, env = run_policy(policy)
    n = len(rows)
    mean = lambda i: sum(r[i] for r in rows) / n
    a, ef, ec, yf, yc = rows[-1]
    print(f"policy: {policy}")
    print(f"  steps: {n}")
    print(f"  tends: {env.tends}  eaten units: {env.eaten}")
    print(f"  mean A: {mean(0):.1f}")
    print(f"  mean E_full: {mean(1):.1f}  mean E_crop: {mean(2):.1f}  crop gap (E): {mean(2) - mean(1):+.1f}")
    print(f"  mean Y_full: {mean(3):.1f}  mean Y_crop: {mean(4):.1f}  crop gap (Y): {mean(4) - mean(3):+.1f}")
    print(f"  final stock total: {sum(env.stock.values())}/40  final A: {a:.1f}")
    print(f"  final E_full: {ef:.1f}  final E_crop: {ec:.1f}")
    print(f"  final Y_full: {yf:.1f}  final Y_crop: {yc:.1f}")
    return rows, env


def main():
    print("Golden Directive — minimal demo (not maintained as a product)")
    print("Y = 2*(A*E)/(A+E); A = ledger (tends restore, eats debit 0.5/unit);")
    print("E_full = total stock / 40 * 100; E_crop = home-quadrant stock only.")
    print()
    summarize("tender")
    print()
    summarize("raider")


if __name__ == "__main__":
    main()
