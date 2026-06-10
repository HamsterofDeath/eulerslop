#!/usr/bin/env python3
from math import comb, factorial
from fractions import Fraction

def solve():
    # 100 discs, 25 of them prime-numbered. We want exactly 22 primes
    # displaced, i.e. exactly 3 primes in their natural positions.
    # Choose which 3 primes are fixed: C(25, 3).
    # The remaining 97 discs are permuted so that none of the other
    # 22 primes lands on its own position (non-primes unrestricted).
    # By inclusion-exclusion that count is
    #   sum_{j=0}^{22} (-1)^j C(22, j) (97 - j)!
    fixed_choices = comb(25, 3)
    rest = sum((-1) ** j * comb(22, j) * factorial(97 - j) for j in range(23))
    probability = Fraction(fixed_choices * rest, factorial(100))

    # Round to 12 decimal places using exact integer arithmetic.
    scaled = probability * 10 ** 12
    rounded = (scaled.numerator * 2 + scaled.denominator) // (2 * scaled.denominator)
    return f"0.{rounded:012d}"

if __name__ == "__main__":
    print(solve())
