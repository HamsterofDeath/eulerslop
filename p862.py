#!/usr/bin/env python3
"""Project Euler 862: sum counts of larger digit permutations."""

from math import factorial


def larger_permutation_sum(digit_count: int) -> int:
    factorials = [factorial(value) for value in range(digit_count + 1)]
    counts = [0] * 10
    result = 0

    def enumerate_counts(digit: int, remaining: int) -> None:
        nonlocal result
        if digit == 9:
            counts[digit] = remaining

            denominator = 1
            for count in counts:
                denominator *= factorials[count]
            all_permutations = factorials[digit_count] // denominator
            valid_permutations = (
                all_permutations * (digit_count - counts[0]) // digit_count
            )

            # Within one digit multiset, each unordered pair of valid
            # permutations contributes once, from its smaller member.
            result += valid_permutations * (valid_permutations - 1) // 2
            return

        for count in range(remaining + 1):
            counts[digit] = count
            enumerate_counts(digit + 1, remaining - count)

    enumerate_counts(0, digit_count)
    return result


def solve() -> int:
    assert larger_permutation_sum(3) == 1_701
    return larger_permutation_sum(12)


if __name__ == "__main__":
    print(solve())
