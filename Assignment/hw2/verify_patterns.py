#!/usr/bin/env python3
"""Brute-check: H2 labelings = at most two runs of 1s vs closed-form growth."""
from __future__ import annotations

import math
from itertools import product


def at_most_two_runs_of_ones(y: tuple[int, ...]) -> bool:
    ones = [i for i, b in enumerate(y) if b == 1]
    if not ones:
        return True
    runs = 1
    for t in range(1, len(ones)):
        if ones[t] != ones[t - 1] + 1:
            runs += 1
        if runs > 2:
            return False
    return True


def gamma_h2_formula(n: int) -> int:
    return sum(math.comb(n, k) for k in range(0, 5))


def main() -> None:
    for n in range(1, 12):
        brute = sum(1 for y in product([0, 1], repeat=n) if at_most_two_runs_of_ones(y))
        formula = gamma_h2_formula(n)
        assert brute == formula, (n, brute, formula)
        print(f"n={n:2d}: Gamma(H2) = {brute:4d} = sum_{{k<=4}} C(n,k)")
    print("All checks passed.")


if __name__ == "__main__":
    main()
