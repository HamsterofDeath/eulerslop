#!/usr/bin/env python3
"""Project Euler 725: digit sum numbers."""


MOD = 10**16
LIMIT = 2020
MAX_SUM = 18


def sum_for_limit(limit: int, modulus: int | None = None) -> int:
    total = 0
    for chosen_digit in range(1, 10):
        counts = [[0, 0] for _ in range(MAX_SUM + 1)]
        sums = [[0, 0] for _ in range(MAX_SUM + 1)]

        for length in range(1, limit + 1):
            next_counts = [[0, 0] for _ in range(MAX_SUM + 1)]
            next_sums = [[0, 0] for _ in range(MAX_SUM + 1)]
            first_position = length == 1
            digits = range(1, 10) if first_position else range(10)

            source_counts = [[1, 0]] if first_position else counts
            source_sums = [[0, 0]] if first_position else sums
            source_range = range(1) if first_position else range(MAX_SUM + 1)

            for current_sum in source_range:
                for seen in range(2):
                    count = source_counts[current_sum][seen]
                    digit_sum = source_sums[current_sum][seen]
                    if count == 0 and digit_sum == 0:
                        continue
                    for digit in digits:
                        new_sum = current_sum + digit
                        if new_sum > MAX_SUM:
                            break
                        new_seen = seen or digit == chosen_digit
                        next_counts[new_sum][new_seen] += count
                        next_sums[new_sum][new_seen] += digit_sum * 10 + count * digit
                        if modulus is not None:
                            next_counts[new_sum][new_seen] %= modulus
                            next_sums[new_sum][new_seen] %= modulus

            counts, sums = next_counts, next_sums
            total += sums[2 * chosen_digit][1]
            if modulus is not None:
                total %= modulus
    return total


def solve() -> int:
    assert sum_for_limit(3) == 63270
    assert sum_for_limit(7) == 85499991450
    return sum_for_limit(LIMIT, MOD)


if __name__ == "__main__":
    print(solve())
