#!/usr/bin/env python3
"""Project Euler 773: Ruff numbers in one residue class."""


MOD = 1_000_000_007


def primes_ending_in_7(count: int) -> list[int]:
    primes = []
    n = 7
    while len(primes) < count:
        is_prime = True
        divisor = 2
        while divisor * divisor <= n:
            if n % divisor == 0:
                is_prime = False
                break
            divisor += 1
        if is_prime:
            primes.append(n)
        n += 10
    return primes


def f_value(count: int) -> int:
    inv2 = pow(2, -1, MOD)
    inv10 = pow(10, -1, MOD)

    product_mod = 1
    phi_mod = 1
    signed_product_sum = 1
    signed_residue_counts = [0] * 10
    signed_residue_counts[1] = 1

    for prime in primes_ending_in_7(count):
        product_mod = product_mod * prime % MOD
        phi_mod = phi_mod * (prime - 1) % MOD
        signed_product_sum = signed_product_sum * (1 - prime) % MOD

        updated = signed_residue_counts[:]
        for residue, value in enumerate(signed_residue_counts):
            updated[(residue * 7) % 10] = (updated[(residue * 7) % 10] - value) % MOD
        signed_residue_counts = updated

    product_mod_10 = pow(7, count, 10)
    multiplier = 7 * pow(product_mod_10, -1, 10) % 10
    signed_floor_residue_sum = sum(
        (multiplier * residue % 10) * value
        for residue, value in enumerate(signed_residue_counts)
    ) % MOD

    sign = -1 if count % 2 else 1
    rough_prefix_count = (
        sign
        * (multiplier * signed_product_sum - signed_floor_residue_sum)
        * inv10
    ) % MOD

    forbidden_shift = (multiplier * product_mod - 7) * inv10 % MOD
    shifted_unit_sum = (
        phi_mod * product_mod * inv2
        + phi_mod * forbidden_shift
        - product_mod * rough_prefix_count
    ) % MOD
    return (10 * shifted_unit_sum + 7 * phi_mod) % MOD


def solve() -> int:
    assert f_value(3) == 76_101_452
    return f_value(97)


if __name__ == "__main__":
    print(solve())
