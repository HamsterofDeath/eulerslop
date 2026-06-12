"""Project Euler 443: GCD sequence g(n) = g(n-1) + gcd(n, g(n-1)), g(4)=13. Find g(10^15)."""
import random
from math import gcd


def is_prime(n):
    # deterministic Miller-Rabin for n < 3.3e24 with these bases
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def pollard_brent(n):
    # Brent's variant of Pollard's rho; returns a nontrivial factor of composite n
    if n % 2 == 0:
        return 2
    while True:
        y = random.randrange(1, n)
        c = random.randrange(1, n)
        m = 128
        g_ = r = q = 1
        x = ys = y
        while g_ == 1:
            x = y
            for _ in range(r):
                y = (y * y + c) % n
            k = 0
            while k < r and g_ == 1:
                ys = y
                for _ in range(min(m, r - k)):
                    y = (y * y + c) % n
                    q = q * abs(x - y) % n
                g_ = gcd(q, n)
                k += m
            r *= 2
        if g_ == n:
            g_ = 1
            while g_ == 1:
                ys = (ys * ys + c) % n
                g_ = gcd(abs(x - ys), n)
        if g_ != n:
            return g_


def prime_factors(n):
    # set of distinct prime factors via trial division of tiny primes + Pollard rho
    res = set()
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47):
        while n % p == 0:
            res.add(p)
            n //= p
    stack = [n] if n > 1 else []
    while stack:
        m = stack.pop()
        if m == 1:
            continue
        if is_prime(m):
            res.add(m)
            continue
        d = pollard_brent(m)
        stack.append(d)
        stack.append(m // d)
    return res


def g_of(N):
    # Simulate with jumps. Let c = g - n. While gcd(n+j, g(n+j-1)) = 1 the value g
    # rises by 1 each step, so c stays fixed and g(n+j-1) = (n+j) + (c-1). Hence
    # gcd(n+j, g(n+j-1)) = gcd(n+j, c-1). The next "event" is the smallest j >= 1
    # with n+j divisible by some prime factor of m = c-1; there g jumps by
    # d = gcd(n+j, m) instead of 1. Jump directly between events.
    n, g = 4, 13
    while n < N:
        m = g - n - 1
        # m >= 8 always here (c = g-n only grows), but keep a guard
        if m == 0:
            g += 1 + n + 1 - 1  # gcd(n+1, 0) = n+1; g(n+1) = g + (n+1)
            n += 1
            continue
        k = min(p - n % p for p in prime_factors(m))
        if n + k >= N:
            # no event strictly before N except possibly at N itself
            if n + k == N:
                g += (k - 1) + gcd(N, m)
            else:
                g += N - n
            n = N
            break
        d = gcd(n + k, m)
        g += (k - 1) + d
        n += k
    return g


def solve():
    return g_of(10**15)


if __name__ == "__main__":
    print(solve())
