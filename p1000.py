#!/usr/bin/env python3
"""Project Euler Problem 1000: Meta-problem of Max And, Max Xor Sum and
Unreachable Nim.

Sub-problem Max And
    For bit k the cut weight contribution is 2^k * x_k(c_k - x_k), where
    c_k is the count of numbers in [1, n] with bit k set and x_k is the
    count of those in group A.  This is at most 2^k * floor(c_k^2 / 4),
    and a partition attaining the bound for every bit simultaneously is
    built by starting from popcount parity and swapping pairs (i, i^2^k)
    that change only x_k.

Sub-problem Max Xor Sum
    A walk whose edge weights [x, y] = x^2 xor y^2 strictly increase can
    use every edge at most once.  Process the edges in increasing weight
    order keeping dp[v] = best chain value ending at vertex v; an edge
    (u, v, w) extends the best chain ending at u or v by w.  Equal
    weights are applied in a batch since a chain needs strict increase.

Sub-problem Unreachable Nim
    Every xor = 0 status is the target of a winning move, hence
    reachable.  A xor != 0 status (a, b, c) is reachable exactly when
    some pile can be reduced to it from the xor = 0 status built from
    the other two piles, i.e. when b^c > a or a^c > b or a^b > c.
    Therefore the unreachable statuses are those with

        a xor b xor c != 0 and a >= b^c, b >= a^c, c >= a^b,

    counted by a digit DP over the bits.

Meta-problem
    M(0) = I(1000), M(1) = X(1000), M(2) = C(1000) and
    M(k) = M(k-1) M(k-2) M(k-3) for k >= 3, all modulo 10^9 + 7.
"""

from collections import defaultdict


def max_and(n: int) -> int:
    bits = n.bit_length()
    counts = []
    for k in range(bits):
        period = 1 << (k + 1)
        half = 1 << k
        full, rem = divmod(n, period)
        counts.append(full * half + max(0, rem - half + 1))
    return sum((1 << k) * (counts[k] * counts[k] // 4) for k in range(bits))


def partition_attaining_bound(n: int) -> tuple[list[int], int]:
    """Side assignment (0/1 per number) reaching the Max And bound."""
    bits = n.bit_length()
    counts = []
    for k in range(bits):
        period = 1 << (k + 1)
        half = 1 << k
        full, rem = divmod(n, period)
        counts.append(full * half + max(0, rem - half + 1))
    side = [0] * (n + 1)
    for i in range(1, n + 1):
        side[i] = bin(i).count("1") & 1
    in_a = [0] * bits
    for i in range(1, n + 1):
        if side[i]:
            for k in range(bits):
                in_a[k] += (i >> k) & 1
    for k in range(bits - 1, -1, -1):
        deficit = counts[k] // 2 - in_a[k]
        step = 1 << k
        i = 1
        while deficit != 0 and i <= n:
            j = i ^ step
            if 1 <= j <= n and side[i] != side[j]:
                carrier = i if (i >> k) & 1 else j
                delta = 1 if side[carrier] == 0 else -1
                if (deficit > 0 and delta == 1) or (deficit < 0 and delta == -1):
                    side[i] ^= 1
                    side[j] ^= 1
                    in_a[k] += delta
                    deficit -= delta
            i += 1
        assert deficit == 0, f"bit {k} unbalanced"
    cut = sum(
        i & j
        for i in range(1, n + 1)
        for j in range(i + 1, n + 1)
        if side[i] != side[j]
    )
    assert cut == max_and(n)
    return side, cut


def max_xor_sum(n: int) -> int:
    edges = []
    for x in range(1, n + 1):
        x2 = x * x
        for y in range(x + 1, n + 1):
            edges.append((x2 ^ (y * y), x, y))
    edges.sort()
    best = {}
    i, m = 0, len(edges)
    while i < m:
        weight = edges[i][0]
        j = i
        while j < m and edges[j][0] == weight:
            j += 1
        updates = []
        for k in range(i, j):
            _, x, y = edges[k]
            bx, by = best.get(x, 0), best.get(y, 0)
            if by + weight > bx:
                updates.append((x, by + weight))
            if bx + weight > by:
                updates.append((y, bx + weight))
        for vertex, value in updates:
            if value > best.get(vertex, 0):
                best[vertex] = value
        i = j
    return max(best.values())


def unreachable_nim(n: int) -> int:
    bits = n.bit_length()
    dp = defaultdict(int)
    dp[(1, 1, 1, 0, 0, 0, 0)] = 1
    for k in range(bits - 1, -1, -1):
        nbit = (n >> k) & 1
        next_dp = defaultdict(int)
        for (r1, r2, r3, x, la, lb, lc), count in dp.items():
            for ak in (0, 1):
                for bk in (0, 1):
                    for ck in (0, 1):
                        nla = la
                        if la == 0:
                            if ak > nbit:
                                continue
                            if ak < nbit:
                                nla = 1
                        nlb = lb
                        if lb == 0:
                            if bk > nbit:
                                continue
                            if bk < nbit:
                                nlb = 1
                        nlc = lc
                        if lc == 0:
                            if ck > nbit:
                                continue
                            if ck < nbit:
                                nlc = 1
                        bc = bk ^ ck
                        nr1 = r1 if r1 != 1 else (2 if ak > bc else (0 if ak < bc else 1))
                        ac = ak ^ ck
                        nr2 = r2 if r2 != 1 else (2 if bk > ac else (0 if bk < ac else 1))
                        ab = ak ^ bk
                        nr3 = r3 if r3 != 1 else (2 if ck > ab else (0 if ck < ab else 1))
                        nx = x | (ak ^ bk ^ ck)
                        next_dp[(nr1, nr2, nr3, nx, nla, nlb, nlc)] += count
        dp = next_dp
    return sum(
        count
        for (r1, r2, r3, x, la, lb, lc), count in dp.items()
        if la == lb == lc == 1 and x == 1 and r1 >= 1 and r2 >= 1 and r3 >= 1
    )


MODULUS = 1_000_000_007


def solve() -> int:
    m = [max_and(1000), max_xor_sum(1000), unreachable_nim(1000)]
    for k in range(3, 1001):
        m.append(m[k - 1] * m[k - 2] * m[k - 3] % MODULUS)
    return m[1000]


if __name__ == "__main__":
    assert max_and(10) == 50
    partition_attaining_bound(1000)
    assert max_xor_sum(4) == 71
    assert max_xor_sum(10) == 702
    assert unreachable_nim(10) == 123
    assert (max_and(1000) * max_xor_sum(1000) ** 2 * unreachable_nim(1000) ** 2) % MODULUS == 457_587_170
    print(solve())
