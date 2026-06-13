#!/usr/bin/env python3
from math import isqrt


MOD = 10**8
N = 10**8 + 7
K = 10**4 + 7


def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d <= isqrt(n):
        if n % d == 0:
            return False
        d += 2
    return True


def solve():
    # A win is the first occurrence of a 10 transition in the coin-toss stream.
    # If that transition starts at round t, then Pr(T=t)=t/2^(t+1).
    m = N if K == 1 else K - 1

    # For residue m modulo N:
    # P = 2^(N-m-1) * (m*2^N + N - m) / (2^N - 1)^2.
    # Here N is prime and 2^N == 2 (mod N), so gcd(N, 2^N-1)=1; since the
    # numerator is congruent to N modulo 2^N-1, the fraction is already reduced.
    assert is_prime(N)
    assert pow(2, N, N) != 1

    two_n = pow(2, N, MOD)
    numerator = pow(2, N - m - 1, MOD) * (m * two_n + N - m) % MOD
    denominator = (two_n - 1) ** 2 % MOD
    return numerator * denominator % MOD


if __name__ == "__main__":
    print(solve())
