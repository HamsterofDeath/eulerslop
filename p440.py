#!/usr/bin/env python3
import numpy as np

MOD = 987898789


def solve():
    # T(n) = 10*T(n-1) + T(n-2) (10 digit tiles or one domino at the end),
    # T(1)=10, T(2)=101.  With the companion Lucas sequence U(0)=0, U(1)=1,
    # U(n)=10*U(n-1)+U(n-2) we have T(n) = U(n+1), and U is a strong
    # divisibility sequence: gcd(U(m),U(n)) = U(gcd(m,n)).  Hence
    #   gcd(T(c^a),T(c^b)) = U(gcd(c^a+1, c^b+1)).
    # With g = gcd(a,b):  gcd(c^a+1, c^b+1) = c^g+1 if a/g and b/g are both
    # odd, else 2 (c odd) or 1 (c even).  So
    #   S(L) = sum_g cntO(g) * sum_c U(c^g+1)  +  cntE * (10*#odd c + #even c)
    # where cntO(g) = #{(a,b): gcd(a,b)=g, a/g and b/g odd} and
    # cntE = L^2 - sum_g cntO(g).
    L = 2000

    # Moebius sieve up to L
    mu = np.ones(L + 1, dtype=np.int64)
    primes = []
    is_comp = bytearray(L + 1)
    for i in range(2, L + 1):
        if not is_comp[i]:
            primes.append(i)
            mu[i] = -1
        for q in primes:
            if i * q > L:
                break
            is_comp[i * q] = 1
            if i % q == 0:
                mu[i * q] = 0
                break
            mu[i * q] = -mu[i]

    # O(M) = #{1<=x,y<=M : x,y odd, gcd(x,y)=1}
    #      = sum over odd squarefree d of mu(d) * (#odd multiples of d <= M)^2
    def odd_coprime_pairs(M):
        s = 0
        for d in range(1, M + 1, 2):
            if mu[d]:
                s += int(mu[d]) * ((M // d + 1) // 2) ** 2
        return s

    ocp = {}
    cntO = [0] * (L + 1)
    for g in range(1, L + 1):
        M = L // g
        if M not in ocp:
            ocp[M] = odd_coprime_pairs(M)
        cntO[g] = ocp[M]
    cntE = L * L - sum(cntO)

    # Period of U mod MOD: MOD is prime, 26 (discriminant/4) is a QR, and the
    # order of the recurrence matrix turns out to be exactly MOD-1 (verified:
    # U(pi)=0, U(pi+1)=1, and no proper divisor of MOD-1 works).
    pi = MOD - 1

    def upair(n):  # (U(n) mod MOD, U(n+1) mod MOD) by fast doubling
        if n == 0:
            return (0, 1)
        a, b = upair(n >> 1)
        c = a * ((2 * b - 10 * a) % MOD) % MOD  # U(2k)
        d = (a * a + b * b) % MOD               # U(2k+1)
        return (d, (10 * d + c) % MOD) if n & 1 else (c, d)

    assert upair(pi) == (0, 1)  # confirms index reduction mod pi is valid

    # indices n[g][c] = (c^g + 1) mod pi for c = 1..L, each row g = 1..L
    cvec = np.arange(1, L + 1, dtype=np.int64)
    idx = np.empty((L, L), dtype=np.int64)
    cur = np.ones(L, dtype=np.int64)
    for g in range(L):
        cur = cur * cvec % pi          # c^(g+1) mod pi (fits in int64)
        idx[g] = (cur + 1) % pi

    # vectorized fast doubling over all L*L indices, MSB first:
    # state (a,b) = (U(k), U(k+1)) for the processed bit prefix k
    n = idx.ravel()
    a = np.zeros(n.shape, dtype=np.int64)
    b = np.ones(n.shape, dtype=np.int64)
    for k in range(pi.bit_length() - 1, -1, -1):
        c = a * ((2 * b - 10 * a) % MOD) % MOD  # U(2k), products < MOD^2 < 2^63
        d = (a * a + b * b) % MOD               # U(2k+1)
        bit = (n >> k) & 1
        a = np.where(bit == 1, d, c)
        b = np.where(bit == 1, (10 * d + c) % MOD, d)

    usum = a.reshape(L, L).sum(axis=1) % MOD    # sum_c U(c^g+1) per g

    total = 0
    for g in range(1, L + 1):
        total += cntO[g] * int(usum[g - 1])
    odd_c = (L + 1) // 2
    total += cntE * (10 * odd_c + (L - odd_c))  # pairs with gcd index 2 or 1
    return total % MOD


if __name__ == "__main__":
    print(solve())
