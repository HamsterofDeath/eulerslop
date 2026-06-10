#!/usr/bin/env python3
# Project Euler 221: Alexandrian Integers
#
# A = p*q*r with 1/A = 1/p + 1/q + 1/r and A > 0 forces exactly one of
# p, q, r positive (say p = a > 0, q = -b, r = -c with b, c > 0).
# Then A = a*b*c and 1/A = 1/a - 1/b - 1/c, which rearranges to
#   (b - a)(c - a) = a^2 + 1.
# So every Alexandrian integer is A = a*(a + d1)*(a + d2) where
# d1*d2 = a^2 + 1, and conversely.  Since d1 + d2 > 2a, we get A > 4a^3,
# so all Alexandrian integers <= 4*a_max^3 come from a <= a_max.


def _primes_up_to(n):
    sieve = bytearray([1]) * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i :: i] = bytearray(len(sieve[i * i :: i]))
    return [i for i in range(2, n + 1) if sieve[i]]


def _sqrt_minus_one(p):
    # p is a prime with p % 4 == 1; return r with r*r % p == p - 1.
    e = (p - 1) // 4
    for x in range(2, p):
        r = pow(x, e, p)
        if r * r % p == p - 1:
            return r
    raise AssertionError("no square root of -1 found")


def _attempt(a_max, target):
    limit = 4 * a_max ** 3  # every A coming from a > a_max exceeds this

    # Sieve the odd prime factors of a^2 + 1: an odd prime p divides
    # a^2 + 1 iff p % 4 == 1 and a == +-r (mod p) where r^2 == -1 (mod p).
    factor_lists = [[] for _ in range(a_max + 1)]
    for p in _primes_up_to(a_max):
        if p % 4 != 1:
            continue
        r = _sqrt_minus_one(p)
        for root in (r, p - r):
            for a in range(root, a_max + 1, p):
                factor_lists[a].append(p)

    values = []
    for a in range(1, a_max + 1):
        n = a * a + 1
        m = n
        divisors = [1]
        if a & 1:  # a odd -> n == 2 (mod 4), exactly one factor of 2
            m //= 2
            divisors = [1, 2]
        for p in factor_lists[a]:
            e = 0
            while m % p == 0:
                m //= p
                e += 1
            divisors = [d * p ** j for d in divisors for j in range(e + 1)]
        if m > 1:
            # Any remaining cofactor is a single prime > a_max >= sqrt(n).
            divisors += [d * m for d in divisors]
        for d in divisors:
            if d * d < n:  # d = d1 <= a; partner d2 = n // d
                A = a * (a + d) * (a + n // d)
                if A <= limit:
                    values.append(A)

    values = sorted(set(values))
    if len(values) >= target:
        return values[target - 1]
    return None


def solve():
    target = 150000
    a_max = 100000
    while True:
        result = _attempt(a_max, target)
        if result is not None:
            return result
        a_max *= 2


if __name__ == "__main__":
    print(solve())
