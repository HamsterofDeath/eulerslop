from math import isqrt


MOD = 1_000_000_007
LIMIT = 100_000_000


def prime_sieve(n):
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, isqrt(n) + 1):
        if sieve[p]:
            start = p * p
            sieve[start:n + 1:p] = b"\x00" * (((n - start) // p) + 1)
    return sieve


def product_for(limit):
    is_prime = prime_sieve(limit)
    primes = [i for i in range(2, limit + 1) if is_prime[i]]
    pi_limit = len(primes)

    pi_small = [0] * (pi_limit + 1)
    count = 0
    for i in range(1, pi_limit + 1):
        if is_prime[i]:
            count += 1
        pi_small[i] = count

    counts = [0] * 32
    for idx, prime in enumerate(primes, 1):
        if idx == pi_limit:
            block = limit - prime + 1
        else:
            block = primes[idx] - prime

        y = idx
        nonprimes = 0
        while y:
            if not is_prime[y]:
                nonprimes += 1
            counts[nonprimes] = (counts[nonprimes] + 1) % MOD
            if block > 1:
                counts[nonprimes + 1] = (counts[nonprimes + 1] + block - 1) % MOD
            y = pi_small[y]

    result = 1
    for value in counts:
        if value:
            result = result * value % MOD
    return result


def solve():
    return product_for(LIMIT)


if __name__ == "__main__":
    print(solve())
