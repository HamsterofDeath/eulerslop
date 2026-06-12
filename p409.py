MOD = 1_000_000_007


def solve(n=10_000_000):
    # Piles are n distinct nonzero values in [1, 2^n - 1] = nonzero vectors of F_2^n.
    # Position is losing iff XOR of piles is 0. W(2)=6 implies positions are ordered tuples.
    # a_k = #ordered k-tuples of distinct nonzero vectors with XOR 0.
    # Take any (k-1)-tuple (D(k-1) ways, D = falling factorial of M = 2^n - 1);
    # the forced k-th element s = XOR of them is invalid iff s = 0 (a_{k-1} ways) or
    # s equals some earlier element x_i (then the other k-2 XOR to 0: (k-1)*(M-k+2)*a_{k-2} ways,
    # since x_i can be any vector not among those k-2).
    #   a_k = D(k-1) - a_{k-1} - (k-1)*(M-k+2)*a_{k-2}
    # W(n) = D(n) - a_n (all ordered distinct tuples minus losing ones).
    M = (pow(2, n, MOD) - 1) % MOD
    D = 1  # D(k-1), starts at D(0) = 1
    a2, a1 = 1, 0  # a_{k-2}, a_{k-1} starting with a_0, a_1
    for k in range(2, n + 1):
        D = D * (M - k + 2) % MOD  # now D(k-1)
        a2, a1 = a1, (D - a1 - (k - 1) * (M - k + 2) % MOD * a2) % MOD
    if n == 1:
        a1 = 0
    D = D * (M - n + 1) % MOD  # D(n)
    return (D - a1) % MOD


if __name__ == "__main__":
    print(solve())
