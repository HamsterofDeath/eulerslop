#!/usr/bin/env python3

def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return is_prime

def solve():
    # For 8-value family, we need the right pattern
    # Pattern with 3 repeated digits works: **X** or similar
    is_prime = sieve(1_000_000)
    for p in range(56003, 1_000_000):
        if not is_prime[p]:
            continue
        s = str(p)
        for digit in "012":
            if s.count(digit) != 3:
                continue
            family = 0
            first = None
            for r in "0123456789":
                t = s.replace(digit, r)
                if t[0] == '0':
                    continue
                if is_prime[int(t)]:
                    family += 1
                    if first is None:
                        first = int(t)
            if family == 8:
                return first
    return 0

if __name__ == "__main__":
    print(solve())
