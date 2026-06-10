#!/usr/bin/env python3
# Admissible numbers < 10^9 are products of the first k primes (k >= 1) with all
# exponents >= 1 (powers of 2 are the k = 1 case).  Since 2*3*5*...*23 = 223092870
# and multiplying by 29 exceeds 10^9, only the primes up to 23 can appear.
# For each admissible N find the smallest M > 1 with N + M prime (N is even, so
# N + M must be odd => M odd, M >= 3) and sum the distinct M values.

LIMIT = 10 ** 9
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23]


def is_prime(n):
    # Deterministic Miller-Rabin for n < 3,215,031,751 with bases 2, 3, 5, 7.
    if n < 2:
        return False
    for p in (2, 3, 5, 7):
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def solve():
    # Generate all admissible numbers via DFS over consecutive prime products.
    admissible = []

    def dfs(i, base):
        m = base * PRIMES[i]
        while m < LIMIT:
            admissible.append(m)
            if i + 1 < len(PRIMES):
                dfs(i + 1, m)
            m *= PRIMES[i]

    dfs(0, 1)

    pseudo = set()
    for n in admissible:
        m = 3
        while not is_prime(n + m):
            m += 2
        pseudo.add(m)
    return sum(pseudo)


if __name__ == "__main__":
    print(solve())
