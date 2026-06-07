#!/usr/bin/env python3

def distinct_factors(n):
    count = 0
    d = 2
    while d * d <= n:
        if n % d == 0:
            count += 1
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        count += 1
    return count

def solve():
    n = 2 * 3 * 5 * 7  # product of first 4 primes
    while True:
        if (distinct_factors(n) == 4 and
            distinct_factors(n + 1) == 4 and
            distinct_factors(n + 2) == 4 and
            distinct_factors(n + 3) == 4):
            return n
        n += 1

if __name__ == "__main__":
    print(solve())
