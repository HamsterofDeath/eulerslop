#!/usr/bin/env python3
"""Project Euler 854: product of maximal Pisano-period moduli."""


LIMIT = 1_000_000
MODULUS = 1_234_567_891


def product_of_maxima(limit: int, modulus: int) -> int:
    """Return the product of M(p), 1 <= p <= limit, modulo modulus.

    Every n whose Pisano period divides p divides
    gcd(F_p, F_(p+1) - 1).  Fibonacci identities reduce that gcd to

        1 or 2                         if p is odd,
        F_k                            if p = 2k and k is even,
        L_k                            if p = 2k and k is odd.

    Apart from the trivial unavailable periods, these gcds themselves have
    period p.  The only non-unit contribution at odd p is M(3) = 2.
    """
    result = 2 if limit >= 3 else 1

    fibonacci, next_fibonacci = 0, 1
    lucas, next_lucas = 2, 1
    for index in range(1, limit // 2 + 1):
        fibonacci, next_fibonacci = (
            next_fibonacci,
            (fibonacci + next_fibonacci) % modulus,
        )
        lucas, next_lucas = next_lucas, (lucas + next_lucas) % modulus

        maximum = fibonacci if index % 2 == 0 else lucas
        result = result * maximum % modulus

    return result


def solve() -> int:
    assert product_of_maxima(10, MODULUS) == 264
    return product_of_maxima(LIMIT, MODULUS)


if __name__ == "__main__":
    print(solve())
