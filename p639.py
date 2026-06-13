#!/usr/bin/env python3
from math import isqrt


MOD = 1_000_000_007
N = 10**12
MAX_K = 50


def primes_upto(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, isqrt(limit) + 1):
        if sieve[p]:
            start = p * p
            sieve[start : limit + 1 : p] = b"\x00" * (((limit - start) // p) + 1)
    return [p for p in range(2, limit + 1) if sieve[p]]


def power_sum_table(limit_k):
    inv = [0] * (limit_k + 2)
    for i in range(1, limit_k + 2):
        inv[i] = pow(i, MOD - 2, MOD)

    choose = [[0] * (limit_k + 2) for _ in range(limit_k + 2)]
    for n in range(limit_k + 2):
        choose[n][0] = choose[n][n] = 1
        for k in range(1, n):
            choose[n][k] = (choose[n - 1][k - 1] + choose[n - 1][k]) % MOD
    return inv, choose


def all_power_sums(n, inv, choose):
    """Return [sum i^0, sum i^1, ..., sum i^MAX_K] modulo MOD."""
    base = (n + 1) % MOD
    powers = [1] * (MAX_K + 2)
    for i in range(1, MAX_K + 2):
        powers[i] = powers[i - 1] * base % MOD

    sums = [0] * (MAX_K + 1)
    sums[0] = n % MOD
    for k in range(1, MAX_K + 1):
        acc = (powers[k + 1] - 1) % MOD
        row = choose[k + 1]
        for j in range(k):
            acc = (acc - row[j] * sums[j]) % MOD
        sums[k] = acc * inv[k + 1] % MOD
    return sums


def extend_h_values(h_values, prime):
    """Multiply h_k by the new squarefull-prime factor p^k - p^(2k)."""
    p = prime % MOD
    p_power = 1
    out = []
    append = out.append
    for h in h_values:
        p_power = p_power * p % MOD
        factor = (p_power - p_power * p_power) % MOD
        append(h * factor % MOD)
    return tuple(out)


def solve():
    primes = primes_upto(isqrt(N))
    base_h = (1,) * MAX_K

    # f_k(n)=rad(n)^k.  Writing f_k=id_k*h_k gives
    # h_k(p)=0 and h_k(p^a)=p^k-p^(2k) for every a>=2, so only
    # squarefull d contribute to sum_d h_k(d) * sum_{m<=N/d} m^k.
    coefficients = {N: list(base_h)}

    def add_coeff(q, h_values):
        row = coefficients.get(q)
        if row is None:
            coefficients[q] = list(h_values)
            return
        for i in range(MAX_K):
            value = row[i] + h_values[i]
            if value >= MOD:
                value -= MOD
            row[i] = value

    def visit_squarefulls(start_index, current, h_values):
        root = isqrt(N // current)
        for index in range(start_index, len(primes)):
            p = primes[index]
            if p > root:
                break

            next_h = extend_h_values(h_values, p)
            value = current * p * p
            while value <= N:
                add_coeff(N // value, next_h)
                visit_squarefulls(index + 1, value, next_h)
                if value > N // p:
                    break
                value *= p

    visit_squarefulls(0, 1, base_h)

    inv, choose = power_sum_table(MAX_K)
    answer = 0
    for q, h_sums in coefficients.items():
        sums = all_power_sums(q, inv, choose)
        subtotal = 0
        for i, h in enumerate(h_sums, 1):
            subtotal = (subtotal + h * sums[i]) % MOD
        answer = (answer + subtotal) % MOD
    return answer


if __name__ == "__main__":
    print(solve())
