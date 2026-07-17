#!/usr/bin/env python3
"""Project Euler 851: SOP and POS via quasimodular forms.

For one coordinate, summing a+b over ab=m gives 2*sigma_1(m).  Hence
R_d(M) is the q^M coefficient of ((1-E2)/12)^d.  Ramanujan's differential
identities express E2^k, k <= 6, using Eisenstein series, derivatives, and
Delta, so evaluating the coefficient at 10000! only needs divisor sums and
the multiplicative Ramanujan tau function.
"""

from math import comb


MOD = 1_000_000_007


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for prime in range(2, int(limit**0.5) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start : limit + 1 : prime] = b"\x00" * (
                (limit - start) // prime + 1
            )
    return [value for value in range(2, limit + 1) if sieve[value]]


def factorial_exponents(limit: int, primes: list[int]) -> dict[int, int]:
    exponents = {}
    for prime in primes:
        quotient = limit
        exponent = 0
        while quotient:
            quotient //= prime
            exponent += quotient
        exponents[prime] = exponent
    return exponents


def factor_integer(value: int, primes: list[int]) -> dict[int, int]:
    exponents = {}
    remainder = value
    for prime in primes:
        if prime * prime > remainder:
            break
        while remainder % prime == 0:
            exponents[prime] = exponents.get(prime, 0) + 1
            remainder //= prime
    if remainder > 1:
        exponents[remainder] = 1
    return exponents


def number_mod(exponents: dict[int, int]) -> int:
    result = 1
    for prime, exponent in exponents.items():
        result = result * pow(prime, exponent, MOD) % MOD
    return result


def divisor_power_sum(exponents: dict[int, int], power: int) -> int:
    result = 1
    for prime, exponent in exponents.items():
        ratio = pow(prime, power, MOD)
        if ratio == 1:
            factor = exponent + 1
        else:
            factor = (pow(ratio, exponent + 1, MOD) - 1) % MOD
            factor = factor * pow(ratio - 1, MOD - 2, MOD) % MOD
        result = result * factor % MOD
    return result


def tau_values(limit: int) -> list[int]:
    """Compute tau(1..limit) from D(Delta) = E2*Delta."""
    sigma_1 = [0] * (limit + 1)
    for divisor in range(1, limit + 1):
        for multiple in range(divisor, limit + 1, divisor):
            sigma_1[multiple] += divisor

    inverses = [0] * (limit + 1)
    inverses[1] = 1
    for value in range(2, limit + 1):
        inverses[value] = (
            MOD - (MOD // value) * inverses[MOD % value] % MOD
        )

    tau = [0] * (limit + 1)
    tau[1] = 1
    for index in range(2, limit + 1):
        convolution = 0
        for left in range(1, index):
            convolution += sigma_1[left] * tau[index - left]
        tau[index] = -24 * (convolution % MOD) * inverses[index - 1] % MOD
    return tau


def tau_from_factorization(
    exponents: dict[int, int], prime_tau: list[int]
) -> int:
    result = 1
    for prime, exponent in exponents.items():
        previous = 1
        current = prime_tau[prime]
        recurrence = pow(prime, 11, MOD)
        for _ in range(2, exponent + 1):
            previous, current = (
                current,
                (prime_tau[prime] * current - recurrence * previous) % MOD,
            )
        result = result * current % MOD
    return result


def e2_power_coefficients(
    n_mod: int, sigma: dict[int, int], tau_n: int
) -> list[int]:
    """Return [q^n]E2^k for k=0..6 and n>0."""
    inverse_5 = pow(5, MOD - 2, MOD)
    inverse_7 = pow(7, MOD - 2, MOD)
    eisenstein = {
        2: -24 * sigma[1] % MOD,
        4: 240 * sigma[3] % MOD,
        6: -504 * sigma[5] % MOD,
        8: 480 * sigma[7] % MOD,
        10: -264 * sigma[9] % MOD,
        12: 65520 * pow(691, MOD - 2, MOD) * sigma[11] % MOD,
    }
    n_power = [1]
    for _ in range(5):
        n_power.append(n_power[-1] * n_mod % MOD)

    coefficient = [0] * 7
    coefficient[1] = eisenstein[2]
    coefficient[2] = eisenstein[4] + 12 * n_power[1] * eisenstein[2]
    coefficient[3] = (
        eisenstein[6]
        + 9 * n_power[1] * eisenstein[4]
        + 72 * n_power[2] * eisenstein[2]
    )
    coefficient[4] = (
        eisenstein[8]
        + 8 * n_power[1] * eisenstein[6]
        + 216 * inverse_5 * n_power[2] * eisenstein[4]
        + 288 * n_power[3] * eisenstein[2]
    )
    coefficient[5] = (
        eisenstein[10]
        + 15 * pow(2, MOD - 2, MOD) * n_power[1] * eisenstein[8]
        + 240 * inverse_7 * n_power[2] * eisenstein[6]
        + 144 * n_power[3] * eisenstein[4]
        + 864 * n_power[4] * eisenstein[2]
    )
    coefficient[6] = (
        eisenstein[12]
        - 4608 * pow(24185, MOD - 2, MOD) * tau_n
        + 36 * inverse_5 * n_power[1] * eisenstein[10]
        + 30 * n_power[2] * eisenstein[8]
        + 720 * inverse_7 * n_power[3] * eisenstein[6]
        + 2592 * inverse_7 * n_power[4] * eisenstein[4]
        + 10368 * inverse_5 * n_power[5] * eisenstein[2]
    )
    return [value % MOD for value in coefficient]


def r_value(
    dimensions: int, exponents: dict[int, int], tau_n: int = 0
) -> int:
    n_mod = number_mod(exponents)
    sigma = {
        power: divisor_power_sum(exponents, power)
        for power in (1, 3, 5, 7, 9, 11)
    }
    coefficients = e2_power_coefficients(n_mod, sigma, tau_n)
    expansion = sum(
        (-1) ** power * comb(dimensions, power) * coefficients[power]
        for power in range(1, dimensions + 1)
    )
    return expansion * pow(pow(12, dimensions, MOD), MOD - 2, MOD) % MOD


def solve() -> int:
    primes = primes_up_to(10_000)
    assert r_value(1, factor_integer(10, primes)) == 36
    assert r_value(2, factor_integer(100, primes)) == 1_873_044
    assert r_value(2, factorial_exponents(100, primes)) == 446_575_636

    exponents = factorial_exponents(10_000, primes)
    tau_n = tau_from_factorization(exponents, tau_values(10_000))
    return r_value(6, exponents, tau_n)


if __name__ == "__main__":
    print(solve())
