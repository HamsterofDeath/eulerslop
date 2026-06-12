#!/usr/bin/env python3


def S(p, m):
    total = 0
    for d in range(1, p // 2 + 1):
        max_multiplier = p // d
        count = max_multiplier - 1
        sum_multipliers = max_multiplier * (max_multiplier + 1) // 2 - 1

        # Fixed points occur for k = d*t and s = k-d.  They are the d
        # consecutive values m-s+1 through m-s+d.
        total += d * (
            (2 * m + 3 * d + 1) * count - 2 * d * sum_multipliers
        ) // 2
    return total


def solve():
    assert S(10, 10) == 225
    assert S(1000, 1000) == 208_724_467
    return S(10**6, 10**6)


if __name__ == "__main__":
    print(solve())
