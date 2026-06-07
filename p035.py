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
    limit = 1_000_000
    is_prime = sieve(limit)
    count = 0
    for n in range(2, limit):
        if not is_prime[n]:
            continue
        s = str(n)
        if all(is_prime[int(s[i:] + s[:i])] for i in range(len(s))):
            count += 1
    return count

if __name__ == "__main__":
    print(solve())
