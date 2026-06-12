#!/usr/bin/env python3
from math import gcd, lcm

MOD = 87654321
FACTORS = (9, 1997, 4877)


def _order(a, m):
    x = a % m
    r = 1
    while x != 1:
        x = x * a % m
        r += 1
    return r


def _local_solutions(mod, period, residue, prefix):
    # For n = 6 + 6q + residue, valid palindrome-free strings have cumulative
    # count 84 + 200q + prefix[residue].  Thus F_5(n) == 0 mod mod iff
    # 2^(7+residue) * 64^q == 86 + prefix[residue] + 200q.
    c = pow(2, 7 + residue, mod)
    rhs0 = (86 + prefix[residue]) % mod
    base = 64 % mod
    pwr = 1
    out = []
    for q in range(period):
        if c * pwr % mod == (rhs0 + 200 * q) % mod:
            out.append(q)
        pwr = pwr * base % mod
    return out


def _combine(left, right):
    # General CRT for two residue lists with common moduli.
    left_res, left_mod = left
    right_res, right_mod = right
    g = gcd(left_mod, right_mod)
    buckets = {}
    for b in right_res:
        buckets.setdefault(b % g, []).append(b)

    step = right_mod // g
    inv = pow(left_mod // g, -1, step)
    mod = left_mod * step
    res = []
    for a in left_res:
        for b in buckets.get(a % g, ()):
            t = ((b - a) // g * inv) % step
            res.append((a + left_mod * t) % mod)
    return res, mod


def D(limit):
    periods = [lcm(m, _order(64, m)) for m in FACTORS]
    period = lcm(*periods)

    exact_period = (32, 32, 32, 34, 36, 34)
    prefix = [0]
    for v in exact_period[:-1]:
        prefix.append(prefix[-1] + v)

    total = 0
    for residue in range(6):
        if limit < 6 + residue:
            continue
        qmax = (limit - 6 - residue) // 6
        local = [(_local_solutions(m, p, residue, prefix), p)
                 for m, p in zip(FACTORS, periods)]
        combined = _combine(_combine(local[0], local[1]), local[2])[0]
        for q0 in combined:
            if q0 <= qmax:
                total += (qmax - q0) // period + 1
    return total


def solve():
    assert D(10 ** 7) == 0
    assert D(5 * 10 ** 9) == 51
    return D(10 ** 18)


if __name__ == "__main__":
    print(solve())
