#!/usr/bin/env python3


def is_prime(n):
    # deterministic Miller-Rabin, valid far beyond 10^14 with these bases
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def solve():
    # Build all right truncatable Harshad numbers (RTH) < 10^13 level by
    # level: every 1-digit number is Harshad, and appending a digit to an RTH
    # gives an RTH iff the result is Harshad.  Only a few thousand survive.
    # A sought prime p < 10^14 has p // 10 a strong RTH, so for each RTH h
    # that is strong (h / digitsum(h) prime) sum the primes 10*h + d.
    LIMIT = 10 ** 14
    total = 0
    level = [(h, h) for h in range(1, 10)]  # (value, digit sum)
    while level:
        nxt = []
        for h, ds in level:
            # strong check: h is Harshad by construction, quotient prime?
            if is_prime(h // ds):
                for d in (1, 3, 7, 9):  # prime > 10 ends in 1, 3, 7 or 9
                    p = 10 * h + d
                    if p < LIMIT and is_prime(p):
                        total += p
            if 10 * h < LIMIT // 10:  # extensions stay < 10^13
                for d in range(10):
                    t, tds = 10 * h + d, ds + d
                    if t % tds == 0:
                        nxt.append((t, tds))
        level = nxt
    return total


if __name__ == "__main__":
    print(solve())
