#!/usr/bin/env python3
"""Project Euler 621: triangular sums via three-square class numbers."""

from math import isqrt


TARGET = 17526 * 10**9


def factorize(n):
    factors = []
    exponent = 0
    while n % 2 == 0:
        n //= 2
        exponent += 1
    if exponent:
        factors.append((2, exponent))

    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            exponent = 0
            while n % divisor == 0:
                n //= divisor
                exponent += 1
            factors.append((divisor, exponent))
        divisor += 2

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


def smallest_prime_factors(limit):
    spf = list(range(limit + 1))
    if limit >= 1:
        spf[1] = 1

    for value in range(2, isqrt(limit) + 1):
        if spf[value] == value:
            for multiple in range(value * value, limit + 1, value):
                if spf[multiple] == multiple:
                    spf[multiple] = value
    return spf


def factor_small(n, spf):
    factors = []
    while n > 1:
        prime = spf[n]
        exponent = 0
        while n % prime == 0:
            n //= prime
            exponent += 1
        factors.append((prime, exponent))
    return factors


def tonelli_shanks(n, prime):
    n %= prime
    if n == 0:
        return 0
    if pow(n, (prime - 1) // 2, prime) != 1:
        return None
    if prime % 4 == 3:
        return pow(n, (prime + 1) // 4, prime)

    q = prime - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1

    z = 2
    while pow(z, (prime - 1) // 2, prime) != prime - 1:
        z += 1

    m = s
    c = pow(z, q, prime)
    t = pow(n, q, prime)
    r = pow(n, (q + 1) // 2, prime)

    while t != 1:
        i = 1
        t2 = pow(t, 2, prime)
        while t2 != 1:
            i += 1
            t2 = pow(t2, 2, prime)

        b = pow(c, 1 << (m - i - 1), prime)
        m = i
        c = (b * b) % prime
        t = (t * c) % prime
        r = (r * b) % prime

    return r


def roots_mod_prime_power(n, prime, exponent):
    if n % prime == 0:
        return [0] if exponent == 1 else []

    root = tonelli_shanks(n, prime)
    if root is None:
        return []

    modulus = prime
    for _ in range(1, exponent):
        correction = ((n - root * root) // modulus) % prime
        correction *= pow((2 * root) % prime, -1, prime)
        root += (correction % prime) * modulus
        modulus *= prime

    root %= modulus
    other = (-root) % modulus
    return [root] if root == other else [root, other]


def square_roots_mod_odd_composite(n, modulus, spf):
    if modulus == 1:
        return [0]

    roots = [0]
    current_modulus = 1
    for prime, exponent in factor_small(modulus, spf):
        prime_power = prime**exponent
        local_roots = roots_mod_prime_power(n, prime, exponent)
        if not local_roots:
            return []

        inverse = pow(current_modulus, -1, prime_power)
        combined = []
        for root in roots:
            for local_root in local_roots:
                lift = ((local_root - root) * inverse) % prime_power
                combined.append((root + current_modulus * lift) % (current_modulus * prime_power))

        roots = combined
        current_modulus *= prime_power

    return roots


def fundamental_class_number(discriminant):
    """Count reduced primitive forms for odd negative fundamental discriminants."""
    limit = isqrt((-discriminant) // 3)
    spf = smallest_prime_factors(limit)
    count = 0

    # In this problem the fundamental discriminants are 5 mod 8, so even
    # leading coefficients cannot satisfy b^2 = D (mod 4a).
    for a in range(1, limit + 1, 2):
        for residue in square_roots_mod_odd_composite(discriminant, a, spf):
            b = residue if residue % 2 else residue + a
            if b > a:
                b -= 2 * a

            c = (b * b - discriminant) // (4 * a)
            if a <= c and not (a == c and b < 0):
                count += 1

    return count


def legendre_symbol(n, prime):
    if n % prime == 0:
        return 0
    value = pow(n % prime, (prime - 1) // 2, prime)
    return -1 if value == prime - 1 else value


def order_class_number(fundamental_discriminant, fundamental_class_number_value, conductor):
    if conductor == 1:
        return fundamental_class_number_value

    multiplier = 1
    for prime, exponent in factorize(conductor):
        multiplier *= prime ** (exponent - 1)
        multiplier *= prime - legendre_symbol(fundamental_discriminant, prime)

    class_number = fundamental_class_number_value * multiplier
    if fundamental_discriminant == -3:
        class_number //= 3
    elif fundamental_discriminant == -4:
        class_number //= 2
    return class_number


def solve(n=TARGET):
    square_sum = 8 * n + 3
    squarefree_part = 1
    conductor_factors = []

    for prime, exponent in factorize(square_sum):
        if exponent % 2:
            squarefree_part *= prime
        if exponent // 2:
            conductor_factors.append((prime, exponent // 2))

    fundamental_discriminant = -squarefree_part
    base_class_number = fundamental_class_number(fundamental_discriminant)

    # G(n) = r_3(8n+3) / 8 = 3 H(8n+3).
    total = 0
    for conductor in divisors_from_factorization(conductor_factors):
        if conductor == 1 and fundamental_discriminant == -3:
            total += 1
        else:
            total += 3 * order_class_number(
                fundamental_discriminant, base_class_number, conductor
            )
    return total


if __name__ == "__main__":
    print(solve())
