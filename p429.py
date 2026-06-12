import numpy as np

MOD = 1_000_000_009  # prime


def solve(n=10**8):
    # n! = prod p^e_p with e_p from Legendre's formula. Unitary divisors of
    # n! pick each prime power wholly or not at all, so S is multiplicative:
    # S(n!) = prod over primes p <= n of (1 + p^(2 e_p)) mod MOD.
    sieve = np.ones(n + 1, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            sieve[i * i :: i] = False
    primes = np.flatnonzero(sieve).astype(np.int64)

    # Legendre: e_p = sum_k floor(n / p^k). For p > sqrt(n) only k=1 counts.
    e = n // primes
    nsmall = int(np.searchsorted(primes, int(n**0.5) + 1))
    for j in range(nsmall):
        p = int(primes[j])
        pk = p * p
        ex = n // p
        while pk <= n:
            ex += n // pk
            pk *= p
        e[j] = ex

    # term_p = p^(2 e_p) mod MOD, vectorized square-and-multiply.
    # MOD is prime and p < MOD, so reduce exponents mod MOD-1 (Fermat).
    expo = (2 * e) % (MOD - 1)
    b = primes % MOD
    terms = np.ones_like(primes)
    while expo.max() > 0:
        sel = (expo & 1) == 1
        terms[sel] = terms[sel] * b[sel] % MOD
        b = b * b % MOD
        expo >>= 1

    # Product of (1 + term_p) mod MOD via pairwise tree reduction.
    vals = (1 + terms) % MOD
    while vals.size > 1:
        if vals.size & 1:
            vals = np.append(vals, 1)
        vals = vals[0::2] * vals[1::2] % MOD
    return int(vals[0])


if __name__ == "__main__":
    print(solve())
