#!/usr/bin/env python3
"""Project Euler 877: a Pell-type recurrence for XOR-products."""


LIMIT = 10**18


def xor_product(left: int, right: int) -> int:
    """Multiply two binary polynomials over GF(2)."""
    result = 0
    while right:
        if right & 1:
            result ^= left
        left <<= 1
        right >>= 1
    return result


def equation_value(a: int, b: int) -> int:
    return (
        xor_product(a, a)
        ^ (xor_product(a, b) << 1)
        ^ xor_product(b, b)
    )


def xor_of_solutions(limit: int) -> int:
    """Return X(limit).

    Regarding the binary integers as polynomials and writing t for 2,

        Q(a, b) = a^2 + t*a*b + b^2

    is unchanged by (a, b) -> (b, a+t*b).  Starting from (0, 3), this
    gives the sequence of all ordered solutions.

    To see completeness, take a solution 0 <= a <= b with b > 3.
    Cancellation of its highest-degree term forces
    deg(a) = deg(b)-1.  Thus u = b+t*a cancels its leading term, and
    Q(u, a) = Q(a, b).  A second highest-degree comparison gives u < a.
    Repeating this descent reaches the sole small solution (0, 3).
    """
    a, b = 0, 3
    result = 0
    while b <= limit:
        result ^= b
        a, b = b, a ^ (b << 1)
    return result


def solve() -> int:
    assert xor_product(7, 3) == 9
    assert equation_value(3, 6) == 5
    assert xor_of_solutions(10) == 5
    return xor_of_solutions(LIMIT)


if __name__ == "__main__":
    print(solve())
