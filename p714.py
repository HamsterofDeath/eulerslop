#!/usr/bin/env python3
"""Project Euler 714: Duodigits."""

from pathlib import Path

from _cpp_runner import run_cpp


def _format_scientific(value, significant_digits=13):
    digits = str(value)
    exponent = len(digits) - 1

    if len(digits) <= significant_digits:
        mantissa = digits.ljust(significant_digits, "0")
    else:
        rounded = int(digits[:significant_digits])
        if int(digits[significant_digits]) >= 5:
            rounded += 1
        mantissa = str(rounded)
        if len(mantissa) > significant_digits:
            exponent += 1
            mantissa = mantissa[:significant_digits]

    return f"{mantissa[0]}.{mantissa[1:]}e{exponent}"


def _raw_sum(limit):
    return int(run_cpp(Path(__file__).with_suffix(".cpp"), (limit,)).strip())


def solve():
    return _format_scientific(_raw_sum(50_000))


if __name__ == "__main__":
    print(solve())
