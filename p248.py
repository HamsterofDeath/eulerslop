#!/usr/bin/env python3
import math

def is_prime(n):
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

def divisors_of(factorization):
    divs = [1]
    for p, e in factorization.items():
        divs = [d * p ** k for d in divs for k in range(e + 1)]
    return divs

def solve():
    target = math.factorial(13)  # 6227020800 = 2^10 * 3^5 * 5^2 * 7 * 11 * 13
    fact = {2: 10, 3: 5, 5: 2, 7: 1, 11: 1, 13: 1}

    # Candidate primes p must satisfy (p - 1) | 13!
    candidates = sorted(
        (d + 1 for d in divisors_of(fact) if is_prime(d + 1)),
        reverse=True,
    )

    results = []

    def dfs(idx, remaining, n):
        if remaining == 1:
            results.append(n)
            if n % 2:
                # phi(2) = 1, so 2n is also a solution when n is odd.
                # This case is unreachable via the loop below because using
                # p = 2 with e = 1 leaves `remaining` unchanged.
                results.append(2 * n)
            return
        for i in range(idx, len(candidates)):
            p = candidates[i]
            if p - 1 > remaining:
                continue
            if remaining % (p - 1):
                continue
            # use prime p with exponent e >= 1
            rem = remaining // (p - 1)
            pe = p  # p^e
            while True:
                dfs(i + 1, rem, n * pe)
                if rem % p:
                    break
                rem //= p
                pe *= p

    dfs(0, target, 1)
    results.sort()
    return results[150000 - 1]

if __name__ == "__main__":
    print(solve())
