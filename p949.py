#!/usr/bin/env python3
"""Project Euler Problem 949: Left vs Right II.

Regard L and R as the game values +1 and -1.  For every longer word,
its Left options are its proper suffixes and its Right options are its
proper prefixes.  Recursively compute the two stops

    upper = max(right stop of every Left option)
    lower = min(left stop of every Right option).

If upper < lower, the word is the simplest dyadic number strictly
between them; otherwise it is hot and retains both stops.  All values
are scaled by 2**n, so the computation uses integers.

For an odd sum of these word games, Right wins with Left to move when
the sum of the upper stops is negative.  Equality is also a Right win
exactly when every component is cold.  Histograms and short
convolutions count the ordered tuples without enumerating them.
"""

from bisect import bisect_left


MODULUS = 1_001_001_011


def ceil_div_pow2(value: int, shift: int) -> int:
    """Return ceil(value / 2**shift) exactly."""
    if value >= 0:
        return (value + (1 << shift) - 1) >> shift
    return -((-value) >> shift)


def simplest_between(lower: int, upper: int, exponent: int) -> int:
    """Find the simplest scaled dyadic strictly between two bounds.

    The returned integer represents a dyadic with denominator at most
    2**exponent, on the common 2**exponent scale.  Simplicity first
    minimizes the denominator and then the absolute numerator.
    """
    for denominator_exponent in range(exponent + 1):
        scale_shift = exponent - denominator_exponent
        numerator_min = (lower >> scale_shift) + 1
        numerator_max = ceil_div_pow2(upper, scale_shift) - 1
        if numerator_min > numerator_max:
            continue

        if numerator_min > 0:
            numerator = numerator_min
        elif numerator_max < 0:
            numerator = numerator_max
        else:
            numerator = 0

        # A nonzero even numerator would have a simpler denominator.
        if (
            denominator_exponent
            and numerator
            and numerator % 2 == 0
        ):
            if numerator + 1 <= numerator_max:
                numerator += 1
            else:
                numerator -= 1
        return numerator << scale_shift

    raise AssertionError("a dyadic separator must exist")


def word_upper_stops(n: int) -> tuple[list[int], list[bool]]:
    """Return each length-n word's upper stop and cold/hot flag."""
    exponent = n
    unit = 1 << exponent
    node_count = (1 << (n + 1)) - 1
    upper_stop = [0] * node_count
    lower_stop = [0] * node_count

    # Words of a fixed length occupy one contiguous level.  Bit 1 is L.
    upper_stop[1] = lower_stop[1] = -unit
    upper_stop[2] = lower_stop[2] = unit
    cold = [False] * (1 << n)

    for length in range(2, n + 1):
        level_start = (1 << length) - 1
        for bits in range(1 << length):
            left_stop = -(1 << 60)
            for suffix_length in range(1, length):
                suffix = bits & ((1 << suffix_length) - 1)
                option = (1 << suffix_length) - 1 + suffix
                left_stop = max(left_stop, lower_stop[option])

            right_stop = 1 << 60
            for prefix_length in range(1, length):
                prefix = bits >> (length - prefix_length)
                option = (1 << prefix_length) - 1 + prefix
                right_stop = min(right_stop, upper_stop[option])

            index = level_start + bits
            if left_stop < right_stop:
                value = simplest_between(
                    left_stop, right_stop, exponent
                )
                upper_stop[index] = lower_stop[index] = value
                if length == n:
                    cold[bits] = True
            else:
                upper_stop[index] = left_stop
                lower_stop[index] = right_stop

    final_start = (1 << n) - 1
    return upper_stop[final_start:], cold


def histogram(values: list[int], modulus: int) -> dict[int, int]:
    counts: dict[int, int] = {}
    for value in values:
        counts[value] = (counts.get(value, 0) + 1) % modulus
    return counts


def convolve(
    first: dict[int, int],
    second: dict[int, int],
    modulus: int,
) -> dict[int, int]:
    if len(first) > len(second):
        first, second = second, first
    result: dict[int, int] = {}
    for left_sum, left_count in first.items():
        for right_sum, right_count in second.items():
            total = left_sum + right_sum
            result[total] = (
                result.get(total, 0) + left_count * right_count
            ) % modulus
    return result


def histogram_power(
    counts: dict[int, int],
    exponent: int,
    modulus: int,
) -> dict[int, int]:
    result = {0: 1}
    for _ in range(exponent):
        result = convolve(result, counts, modulus)
    return result


def count_negative_sums(
    first: dict[int, int],
    second: dict[int, int],
    modulus: int,
) -> int:
    ordered_second = sorted(second.items())
    second_sums = [value for value, _ in ordered_second]
    prefix_counts = [0]
    for _, count in ordered_second:
        prefix_counts.append((prefix_counts[-1] + count) % modulus)

    answer = 0
    for value, count in first.items():
        split = bisect_left(second_sums, -value)
        answer = (
            answer + count * prefix_counts[split]
        ) % modulus
    return answer


def count_zero_sums(
    first: dict[int, int],
    second: dict[int, int],
    modulus: int,
) -> int:
    if len(first) > len(second):
        first, second = second, first
    return sum(
        count * second.get(-value, 0)
        for value, count in first.items()
    ) % modulus


def count_right_wins(n: int, k: int, modulus: int = MODULUS) -> int:
    if n < 1 or k < 1 or k % 2 == 0:
        raise ValueError("n and k must be positive, with k odd")

    upper_stops, cold = word_upper_stops(n)
    all_words = histogram(upper_stops, modulus)
    cold_words = histogram(
        [
            value
            for value, is_cold in zip(upper_stops, cold)
            if is_cold
        ],
        modulus,
    )

    left_size = k // 2
    right_size = k - left_size
    all_left = histogram_power(all_words, left_size, modulus)
    all_right = histogram_power(all_words, right_size, modulus)
    negative = count_negative_sums(all_left, all_right, modulus)

    cold_left = histogram_power(cold_words, left_size, modulus)
    cold_right = histogram_power(cold_words, right_size, modulus)
    cold_zero = count_zero_sums(cold_left, cold_right, modulus)
    return (negative + cold_zero) % modulus


def solve() -> int:
    assert count_right_wins(2, 3, 2**64) == 14
    assert count_right_wins(4, 3, 2**64) == 496
    assert count_right_wins(8, 5, 2**64) == 26_359_197_010
    return count_right_wins(20, 7)


if __name__ == "__main__":
    print(solve())
