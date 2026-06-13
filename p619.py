#!/usr/bin/env python3

MOD = 1_000_000_007


def primes_upto(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, int(limit**0.5) + 1):
        if sieve[p]:
            start = p * p
            sieve[start : limit + 1 : p] = b"\x00" * (((limit - start) // p) + 1)
    return [n for n in range(limit + 1) if sieve[n]]


def square_parity_rank(first, last):
    small_primes = primes_upto(int(last**0.5))
    prime_bits = {}
    next_bit = 0
    basis = {}
    rank = 0

    def bit_for_prime(prime):
        nonlocal next_bit
        bit = prime_bits.get(prime)
        if bit is None:
            bit = next_bit
            prime_bits[prime] = bit
            next_bit += 1
        return bit

    for value in range(first, last + 1):
        rest = value
        vector = 0
        for prime in small_primes:
            if prime * prime > rest:
                break
            if rest % prime == 0:
                odd_power = False
                while rest % prime == 0:
                    rest //= prime
                    odd_power = not odd_power
                if odd_power:
                    vector ^= 1 << bit_for_prime(prime)
        if rest > 1:
            vector ^= 1 << bit_for_prime(rest)

        while vector:
            lead = vector.bit_length() - 1
            pivot = basis.get(lead)
            if pivot is None:
                basis[lead] = vector
                rank += 1
                break
            vector ^= pivot

    return rank


def solve(first=1_000_000, last=1_234_567):
    count = last - first + 1
    rank = square_parity_rank(first, last)
    return (pow(2, count - rank, MOD) - 1) % MOD


if __name__ == "__main__":
    print(solve())
