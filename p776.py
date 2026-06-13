#!/usr/bin/env python3
"""Project Euler 776: summing n divided by its digit sum."""

from decimal import Decimal, ROUND_HALF_UP, getcontext


TARGET = 1_234_567_890_123_456_789


def value(limit: int) -> Decimal:
    digits = [int(ch) for ch in str(limit)]
    max_sum = 9 * len(digits)
    counts = [[0] * (max_sum + 1) for _ in range(2)]
    sums = [[0] * (max_sum + 1) for _ in range(2)]
    counts[1][0] = 1

    for digit_limit in digits:
        next_counts = [[0] * (max_sum + 1) for _ in range(2)]
        next_sums = [[0] * (max_sum + 1) for _ in range(2)]
        for tight in range(2):
            limit_digit = digit_limit if tight else 9
            for digit_sum in range(max_sum + 1):
                count = counts[tight][digit_sum]
                total = sums[tight][digit_sum]
                if count == 0 and total == 0:
                    continue
                for digit in range(limit_digit + 1):
                    next_tight = int(tight and digit == limit_digit)
                    new_sum = digit_sum + digit
                    next_counts[next_tight][new_sum] += count
                    next_sums[next_tight][new_sum] += total * 10 + count * digit
        counts, sums = next_counts, next_sums

    result = Decimal(0)
    for digit_sum in range(1, max_sum + 1):
        result += Decimal(sums[0][digit_sum] + sums[1][digit_sum]) / Decimal(digit_sum)
    return result


def scientific(number: Decimal) -> str:
    exponent = number.adjusted()
    mantissa = number.scaleb(-exponent)
    rounded = mantissa.quantize(Decimal("0.000000000001"), rounding=ROUND_HALF_UP)
    if rounded == Decimal("10.000000000000"):
        rounded = Decimal("1.000000000000")
        exponent += 1
    return f"{rounded}e{exponent}"


def solve() -> str:
    getcontext().prec = 80
    assert value(10) == Decimal(19)
    assert scientific(value(123)) == "1.187764610390e3"
    assert scientific(value(12345)) == "4.855801996238e6"
    return scientific(value(TARGET))


if __name__ == "__main__":
    print(solve())
