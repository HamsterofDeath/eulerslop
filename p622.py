#!/usr/bin/env python3
"""Project Euler 622: perfect shuffle periods as multiplicative orders."""


TARGET_ORDER = 60


def factorize(n):
    factors = []
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            exponent = 0
            while n % divisor == 0:
                n //= divisor
                exponent += 1
            factors.append((divisor, exponent))
        divisor += 1 if divisor == 2 else 2

    if n > 1:
        factors.append((n, 1))
    return factors


def divisors_from_factorization(factors):
    divisors = [1]
    for prime, exponent in factors:
        previous = divisors
        divisors = []
        power = 1
        for _ in range(exponent + 1):
            divisors.extend(value * power for value in previous)
            power *= prime
    return divisors


def has_exact_order(modulus, order, proper_order_divisors):
    if modulus == 1 or pow(2, order, modulus) != 1:
        return False
    return all(pow(2, divisor, modulus) != 1 for divisor in proper_order_divisors)


def solve(order=TARGET_ORDER):
    mersenne = (1 << order) - 1
    modulus_factors = factorize(mersenne)
    order_divisors = divisors_from_factorization(factorize(order))
    proper_order_divisors = [divisor for divisor in order_divisors if divisor < order]

    total = 0
    for modulus in divisors_from_factorization(modulus_factors):
        if has_exact_order(modulus, order, proper_order_divisors):
            total += modulus + 1
    return total


if __name__ == "__main__":
    print(solve())
