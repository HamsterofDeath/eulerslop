#!/usr/bin/env python3
from math import comb


def solve():
    distinct = {comb(n, k) for n in range(51) for k in range(n + 1)}
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

    def squarefree(v):
        return all(v % (p * p) != 0 for p in primes)

    return sum(v for v in distinct if squarefree(v))


if __name__ == "__main__":
    print(solve())
