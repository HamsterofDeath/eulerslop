#!/usr/bin/env python3

def solve():
    # For three pairwise-coprime moduli of the form pq, pr, qr (p,q,r distinct
    # primes), the Frobenius number is known to be
    #     f(pq, pr, qr) = 2pqr - pq - pr - qr.
    # Sanity check against the examples in the statement:
    #   p,q,r = 2,3,5 : 2*30 - 6 - 10 - 15 = 29  = f(6,10,15)
    #   p,q,r = 2,7,11: 2*154 - 14 - 22 - 77 = 195 = f(14,22,77)
    #
    # Summing over all triples p < q < r < 5000:
    #   sum 2pqr            = 2 * e3   (elementary symmetric polynomial)
    #   sum (pq + pr + qr)  = (n-2) * e2   (each pair occurs in n-2 triples)
    # with e2, e3 expressed via power sums S1, S2, S3 (Newton's identities).
    LIMIT = 5000
    sieve = bytearray([1]) * LIMIT
    sieve[0] = sieve[1] = 0
    for i in range(2, int(LIMIT ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
    primes = [i for i in range(LIMIT) if sieve[i]]

    n = len(primes)
    s1 = sum(primes)
    s2 = sum(p * p for p in primes)
    s3 = sum(p * p * p for p in primes)
    e2 = (s1 * s1 - s2) // 2
    e3 = (s1 ** 3 - 3 * s1 * s2 + 2 * s3) // 6

    return 2 * e3 - (n - 2) * e2

if __name__ == "__main__":
    print(solve())
