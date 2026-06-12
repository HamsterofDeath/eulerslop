#!/usr/bin/env python3

from fractions import Fraction
from math import comb


def bernoulli_numbers(limit):
    work = [Fraction(0) for _ in range(limit + 1)]
    result = []
    for m in range(limit + 1):
        work[m] = Fraction(1, m + 1)
        for j in range(m, 0, -1):
            work[j - 1] = j * (work[j - 1] - work[j])
        result.append(work[0])
    if limit >= 1:
        result[1] = Fraction(-1, 2)
    return result


class PAdicHarmonic:
    def __init__(self, prime, precision):
        self.prime = prime
        self.precision = precision
        self.modulus = prime**precision
        self.bernoulli = bernoulli_numbers(precision)
        self.memo = {0: (0, 0)}

        self.inverse = [0] * prime
        for a in range(1, prime):
            self.inverse[a] = pow(a, -1, self.modulus)

        self.unit_sums = [
            sum(pow(self.inverse[a], t + 1, self.modulus) for a in range(1, prime)) % self.modulus
            for t in range(precision)
        ]

        self.modular_power_sum_coeffs = []
        for exponent in range(precision):
            coeffs = []
            usable = True
            for k in range(exponent + 1):
                coeff = Fraction(comb(exponent + 1, k), exponent + 1) * self.bernoulli[k]
                if coeff.denominator % prime == 0:
                    usable = False
                    break
                coeffs.append(coeff.numerator * pow(coeff.denominator, -1, self.modulus) % self.modulus)
            self.modular_power_sum_coeffs.append(coeffs if usable else None)

    def power_sum(self, n, exponent):
        if n <= 0:
            return 0

        coeffs = self.modular_power_sum_coeffs[exponent]
        if coeffs is not None:
            total = 0
            for k, coeff in enumerate(coeffs):
                total = (total + coeff * pow(n, exponent + 1 - k, self.modulus)) % self.modulus
            return total

        total = Fraction(0)
        for k in range(exponent + 1):
            total += (
                Fraction(comb(exponent + 1, k), exponent + 1)
                * self.bernoulli[k]
                * n ** (exponent + 1 - k)
            )
        assert total.denominator == 1
        return total.numerator % self.modulus

    def unit_part_sum(self, n):
        p = self.prime
        q, r = divmod(n, p)
        total = 0
        for t in range(self.precision):
            total = (
                total
                + pow(-p, t, self.modulus) * self.power_sum(q, t) * self.unit_sums[t]
            ) % self.modulus

        for a in range(1, r + 1):
            total = (total + pow(p * q + a, -1, self.modulus)) % self.modulus
        return total

    def scaled_harmonic(self, n):
        if n in self.memo:
            return self.memo[n]

        level = 0
        t = n
        while t >= self.prime:
            t //= self.prime
            level += 1

        if level == 0:
            result = (self.unit_part_sum(n), 0)
        else:
            q = n // self.prime
            previous, previous_level = self.scaled_harmonic(q)
            value = (
                pow(self.prime, level, self.modulus) * self.unit_part_sum(n)
                + pow(self.prime, level - 1 - previous_level, self.modulus) * previous
            ) % self.modulus
            result = (value, level)

        self.memo[n] = result
        return result

    def denominator_not_divisible(self, n):
        value, level = self.scaled_harmonic(n)
        return value % (self.prime**level) == 0

    def largest_integral_denominator_index(self, search_limit):
        candidates = list(range(1, self.prime))
        best = max(candidates)
        power = self.prime

        while candidates and power <= search_limit * self.prime:
            next_candidates = []
            for prefix in candidates:
                base = prefix * self.prime
                for digit in range(self.prime):
                    n = base + digit
                    if power <= n < power * self.prime and self.denominator_not_divisible(n):
                        next_candidates.append(n)
            if next_candidates:
                best = max(best, max(next_candidates))
            candidates = next_candidates
            power *= self.prime
        return best


def solve():
    assert PAdicHarmonic(3, 12).denominator_not_divisible(68)
    assert not PAdicHarmonic(3, 12).denominator_not_divisible(69)
    assert PAdicHarmonic(7, 12).denominator_not_divisible(719102)
    assert not PAdicHarmonic(7, 12).denominator_not_divisible(719103)
    return str(PAdicHarmonic(137, 10).largest_integral_denominator_index(10**16))


if __name__ == "__main__":
    print(solve())
