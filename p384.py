#!/usr/bin/env python3

def solve():
    # b(n) = (-1)^(number of adjacent 11 pairs in binary n)  (Rudin-Shapiro),
    # s(n) = sum_{i<=n} b(i).  Concatenation rule: for n = p*2^j + r (r in j
    # bits, leading zeros allowed) the pair count is  a(p) + a_j(r) + e*u,
    # where e = lowest bit of p and u = top bit of the j-bit field of r, so
    # b(p*2^j + r) = b(p) * (-1)^(a_j(r) + e*u).
    #
    # Hence the sum of b over a full 2^j block following a prefix ending in
    # bit e is b(p)*A_j (e=0) or b(p)*B_j (e=1), with
    #   A_0 = B_0 = 1,  A_j = A_{j-1} + B_{j-1},  B_j = A_{j-1} - B_{j-1},
    # giving A_j = 2^ceil(j/2) (powers of two - this keeps the state space
    # of the counting recursion tiny, since all reachable targets lie in a
    # coarse lattice).
    M = 64
    A, B = [1], [1]
    for _ in range(M):
        a, b = A[-1] + B[-1], A[-1] - B[-1]
        A.append(a)
        B.append(b)

    # |partial block sum| <= maxg[j] = 1 + A_0 + ... + A_{j-1}  (each level
    # adds at most a full half-block A_{j-1}); used to prune dead branches.
    maxg = [1]
    for j in range(1, M + 1):
        maxg.append(maxg[-1] + A[j - 1])

    memo = {}

    def h(j, e, t):
        # number of r in [0, 2^j) whose cumulative sum
        # G(e,j,r) = sum_{r'<=r} (-1)^(a_j(r') + e*topbit_j(r'))  equals t.
        # Split on the top bit of r: lower half contributes plain (j-1)-bit
        # partial sums (junction bit 0); upper half starts after a full
        # lower half (+A_{j-1}) and is sign-flipped by (-1)^e with junction
        # bit 1 against the new leading 1.
        if t < -maxg[j] or t > maxg[j]:
            return 0
        if j == 0:
            return 1 if t == 1 else 0
        key = (j, e, t)
        v = memo.get(key)
        if v is None:
            v = h(j - 1, 0, t) \
                + h(j - 1, 1, t - A[j - 1] if e == 0 else A[j - 1] - t)
            memo[key] = v
        return v

    def g(t, c):
        # Index of the c-th occurrence of value t in s.  Walk the bits of n
        # from the top, keeping base = s-value accumulated from skipped full
        # blocks, bp = b(prefix), ep = last prefix bit.  The bit-0 subtree
        # at level j holds h(j, 0, (t-base)*bp) occurrences (its prefix ends
        # in 0 and s(n) = base + bp*G there); steer left/right accordingly.
        assert h(M, 0, t) == t  # all t occurrences of t lie below 2^M
        base, bp, ep, n = 0, 1, 0, 0
        for j in range(M - 1, -1, -1):
            cnt0 = h(j, 0, (t - base) * bp)
            if c <= cnt0:
                n, ep = 2 * n, 0
            else:
                c -= cnt0
                base += bp * A[j]          # skip the full bit-0 subtree
                if ep:
                    bp = -bp               # appending 1 after a 1 flips b
                n, ep = 2 * n + 1, 1
        assert c == 1
        return n

    # examples from the statement
    assert g(3, 3) == 6 and g(4, 2) == 7
    assert g(54321, 12345) == 1220847710

    F = [1, 1]
    for _ in range(2, 46):
        F.append(F[-1] + F[-2])
    return sum(g(F[t], F[t - 1]) for t in range(2, 46))


if __name__ == "__main__":
    print(solve())
