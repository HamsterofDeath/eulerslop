#!/usr/bin/env python3
"""Project Euler 710: One Million Members."""


MOD = 1_000_000


def _twopal_count(n):
    """Return t(n) exactly; intended for the small values in the statement."""
    half = n // 2
    no_two = [0] * (half + 1)
    prefix = [0] * (half + 1)
    no_two[0] = 1
    prefix[0] = 1

    for total in range(1, half + 1):
        no_two[total] = prefix[total - 1]
        if total >= 2:
            no_two[total] -= no_two[total - 2]
        prefix[total] = prefix[total - 1] + no_two[total]

    result = 2**half - prefix[half]
    if n % 2 == 0 and n >= 2:
        result += no_two[(n - 2) // 2]
    return result


def solve():
    no_two = [1]
    prefix = [1]
    pow2 = 1
    half = 0

    while True:
        odd_n = 2 * half + 1
        if odd_n > 42 and (pow2 - prefix[half]) % MOD == 0:
            return odd_n

        even_n = 2 * half
        if even_n > 42 and (pow2 - prefix[half] + no_two[half - 1]) % MOD == 0:
            return even_n

        half += 1
        pow2 = (2 * pow2) % MOD
        value = prefix[half - 1]
        if half >= 2:
            value -= no_two[half - 2]
        no_two.append(value % MOD)
        prefix.append((prefix[-1] + no_two[-1]) % MOD)


if __name__ == "__main__":
    print(solve())
