import numpy as np


def sieve_primes(limit):
    s = np.ones(limit + 1, dtype=bool)
    s[:2] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = False
    return np.nonzero(s)[0].astype(np.int64)


def solve():
    # Sum s(n, 10^8) = sum over primes p <= 10^8 of p * #{n <= N : p | n^15 + 1}.
    # For odd p, x^15 = -1 (mod p) iff (-x)^15 = 1, so the solutions are the
    # negatives of the 15th roots of unity mod p; there are exactly
    # g = gcd(15, p-1) of them (g is odd, so -1 is always a 15th power).
    #   g = 1  : the only root is x = -1; #n = floor((N+1)/p).
    #   g > 1  : build a generator w of the order-g subgroup from an element of
    #            order 3 (z = a^((p-1)/3) != 1) and/or order 5; the roots are
    #            p - w^j, j = 0..g-1, each hitting floor(N/p) or +1 values of n.
    # p = 2 divides n^15+1 exactly for odd n.
    N = 10 ** 11
    M = 10 ** 8

    primes = sieve_primes(M)
    total = 2 * ((N + 1) // 2)  # p = 2

    odd = primes[1:]
    pm1 = odd - 1
    has3 = (pm1 % 3 == 0)
    has5 = (pm1 % 5 == 0)
    g1 = ~(has3 | has5)

    # g == 1 primes, vectorized: contribution p * floor((N+1)/p).
    pg1 = odd[g1]
    total += int(np.sum(pg1 * ((N + 1) // pg1)))

    rest = odd[~g1].tolist()
    r3 = has3[~g1].tolist()
    r5 = has5[~g1].tolist()

    # Fixed bases for finding a cubic/quintic non-residue: each fails with
    # "probability" 1/3 (resp. 1/5), so this list is effectively never
    # exhausted; a while-loop fallback keeps it strictly correct.
    bases = (2, 3, 5, 6, 7, 10, 11, 12, 13, 14, 17, 19, 23, 29, 31, 37, 41,
             43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107)

    def order_elem(p, e):
        # return a^e mod p != 1 for some base a (an element of order 3 or 5)
        for a in bases:
            if a % p:
                z = pow(a, e, p)
                if z != 1:
                    return z
        a = bases[-1] + 1
        while True:
            z = pow(a, e, p)
            if z != 1:
                return z
            a += 1

    for p, b3, b5 in zip(rest, r3, r5):
        pm = p - 1
        if b3:
            w = order_elem(p, pm // 3)
            if b5:
                w = w * order_elem(p, pm // 5) % p
                g = 15
            else:
                g = 3
        else:
            w = order_elem(p, pm // 5)
            g = 5
        # roots are p - w^j; n-count for root r is N//p (+1 if r <= N % p)
        q, rem = divmod(N, p)
        c = 1
        extra = 0
        for _ in range(g):
            if p - c <= rem:
                extra += 1
            c = c * w % p
        total += p * (g * q + extra)

    return total


if __name__ == "__main__":
    print(solve())
