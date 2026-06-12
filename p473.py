#!/usr/bin/env python3
from collections import defaultdict
from math import log, sqrt


def phi_power_pairs(limit):
    pairs = {0: (1, 0), 1: (0, 1)}

    for exponent in range(1, limit + 1):
        a, b = pairs[exponent]
        pairs[exponent + 1] = (b, a + b)

    pairs[-1] = (-1, 1)
    for exponent in range(-1, -limit - 1, -1):
        a_next, b_next = pairs[exponent + 1]
        a, b = pairs[exponent]
        pairs[exponent - 1] = (a_next - a, b_next - b)

    return pairs


def half_sums(items):
    out = []

    def visit(index, previous_used, a_sum, b_sum, first, last):
        if index == len(items):
            out.append((b_sum, a_sum, first, last))
            return

        visit(index + 1, False, a_sum, b_sum, first, last)
        if not previous_used:
            a, b = items[index]
            visit(
                index + 1,
                True,
                a_sum + a,
                b_sum + b,
                index if first < 0 else first,
                index,
            )

    visit(0, False, 0, 0, -1, -1)
    return out


def palindromic_sum(limit):
    phi = (1 + sqrt(5)) / 2
    max_k = int(log(limit, phi)) + 6
    powers = phi_power_pairs(max_k + 2)

    terms = []
    for k in range(1, max_k + 1):
        # A palindrome with a phigital point in the middle pairs exponents
        # k and -k-1. k = 0 would use consecutive exponents 0 and -1.
        a = powers[k][0] + powers[-k - 1][0]
        b = powers[k][1] + powers[-k - 1][1]
        if a + b * phi <= limit:
            terms.append((a, b))

    split = len(terms) // 2
    left = half_sums(terms[:split])
    right = half_sums(terms[split:])

    right_by_b = defaultdict(list)
    for b_sum, a_sum, first, last in right:
        right_by_b[b_sum].append((a_sum, first, last))

    values = {1}
    for b_sum, a_sum, first, last in left:
        for right_a, right_first, _ in right_by_b.get(-b_sum, ()):
            if last == split - 1 and right_first == 0:
                continue
            value = a_sum + right_a
            if 0 < value <= limit:
                values.add(value)

    return sum(values)


def solve():
    assert palindromic_sum(1000) == 4345
    return palindromic_sum(10**10)


if __name__ == "__main__":
    print(solve())
