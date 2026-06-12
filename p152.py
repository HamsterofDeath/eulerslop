#!/usr/bin/env python3
from collections import Counter
from math import lcm


GROUP_13 = (13, 39, 52)


def _smooth_candidates():
    out = []
    for n in range(2, 81):
        x = n
        for p in (2, 3, 5, 7):
            while x % p == 0:
                x //= p
        if x == 1:
            out.append(n)
    return out


CANDIDATES = _smooth_candidates()


def _subset_sums(values):
    sums = [0]
    for value in values:
        sums += [s + value for s in sums]
    return sums


def _count_with_group(use_group):
    # For primes p > 7, terms with denominators divisible by p must cancel
    # modulo p^2.  The only non-empty possibility is selecting 13, 39, and 52
    # together; all other such denominators are impossible.
    denominators = CANDIDATES + (list(GROUP_13) if use_group else [])
    scale = 1
    for n in denominators:
        scale = lcm(scale, n * n)

    target = scale // 2
    if use_group:
        target -= sum(scale // (n * n) for n in GROUP_13)

    values = [scale // (n * n) for n in CANDIDATES]
    left = _subset_sums(values[:20])
    right = Counter(_subset_sums(values[20:]))
    return sum(right.get(target - value, 0) for value in left)


def solve():
    return _count_with_group(False) + _count_with_group(True)


if __name__ == "__main__":
    print(solve())
