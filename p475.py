#!/usr/bin/env python3
from collections import defaultdict


MOD = 1_000_000_007


def _binom_table(limit, choose_limit):
    table = [[0] * (choose_limit + 1) for _ in range(limit + 1)]
    for n in range(limit + 1):
        table[n][0] = 1
        for k in range(1, min(n, choose_limit) + 1):
            if k == n:
                table[n][k] = 1
            else:
                table[n][k] = (table[n - 1][k - 1] + table[n - 1][k]) % MOD
    return table


def f(musicians):
    assert musicians % 12 == 0
    n = musicians // 12
    rows = 3 * n       # first-day quartets
    columns = 4 * n    # labelled second-day trios

    choose = _binom_table(columns, 4)
    # State: columns currently used 0, 1, and 2 times.  Used 3 times are full.
    dp = {(columns, 0, 0): 1}

    for _ in range(rows):
        next_dp = defaultdict(int)
        for (zero, one, two), value in dp.items():
            for from_zero in range(5):
                if from_zero > zero:
                    continue
                for from_one in range(5 - from_zero):
                    from_two = 4 - from_zero - from_one
                    if from_one > one or from_two > two:
                        continue

                    ways = (
                        choose[zero][from_zero]
                        * choose[one][from_one]
                        * choose[two][from_two]
                    ) % MOD
                    key = (
                        zero - from_zero,
                        one - from_one + from_zero,
                        two - from_two + from_one,
                    )
                    next_dp[key] = (next_dp[key] + value * ways) % MOD
        dp = next_dp

    labelled_trio_count = dp[(0, 0, 0)]

    # Each quartet's four labelled musicians can be assigned to the selected
    # trio labels in 4! ways.  The trios themselves are not labelled.
    trio_factorial = 1
    for i in range(2, columns + 1):
        trio_factorial = trio_factorial * i % MOD

    return (
        labelled_trio_count
        * pow(24, rows, MOD)
        * pow(trio_factorial, MOD - 2, MOD)
    ) % MOD


def solve():
    assert f(12) == 576
    assert f(24) == 509089824
    return f(600)


if __name__ == "__main__":
    print(solve())
