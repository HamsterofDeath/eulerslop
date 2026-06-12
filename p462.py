#!/usr/bin/env python3
from math import factorial, lgamma, log, log10


def _shape(limit):
    rows = []
    p2 = 1
    while p2 <= limit:
        count = 0
        p3 = 1
        while p2 * p3 <= limit:
            count += 1
            p3 *= 3
        rows.append(count)
        p2 *= 2
    return rows


def _hooks(rows):
    heights = [sum(1 for r in rows if r > j) for j in range(max(rows))]
    for i, row in enumerate(rows):
        for j in range(row):
            yield (row - j) + (heights[j] - i) - 1


def _exact(limit):
    rows = _shape(limit)
    numerator = factorial(sum(rows))
    denominator = 1
    for h in _hooks(rows):
        denominator *= h
    return numerator // denominator


def F_scientific(limit):
    rows = _shape(limit)
    value = lgamma(sum(rows) + 1) / log(10) - sum(log10(h) for h in _hooks(rows))
    exponent = int(value)
    mantissa = 10 ** (value - exponent)
    text = f"{mantissa:.10f}"
    if text == "10.0000000000":
        text = "1.0000000000"
        exponent += 1
    return f"{text}e{exponent}"


def solve():
    assert _exact(6) == 5
    assert _exact(8) == 9
    assert _exact(20) == 450
    assert F_scientific(1000) == "8.8521816557e21"
    return F_scientific(10 ** 18)


if __name__ == "__main__":
    print(solve())
