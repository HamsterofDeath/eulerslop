#!/usr/bin/env python3
import heapq
from math import isqrt

MOD = 500500507
K = 500500


def _first_primes(count):
    # p_500500 is below 7.4e6; this bound keeps the sieve compact and avoids a
    # resizing loop in the hot path.
    limit = 7_400_000
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, isqrt(limit) + 1):
        if sieve[p]:
            start = p * p
            sieve[start:limit + 1:p] = b"\x00" * ((limit - start) // p + 1)
    primes = [i for i in range(limit + 1) if sieve[i]]
    assert len(primes) >= count
    return primes[:count]


def solve():
    # A number with 2^K divisors has exponents of the form 2^a-1.  Adding one
    # more factor of 2 to the divisor count costs either a new prime p, or
    # upgrading an existing prime exponent by multiplying by p^(old_exp+1).
    heap = _first_primes(K)
    heapq.heapify(heap)
    ans = 1
    for _ in range(K):
        x = heapq.heappop(heap)
        ans = ans * (x % MOD) % MOD
        heapq.heappush(heap, x * x)
    return ans


if __name__ == "__main__":
    print(solve())
