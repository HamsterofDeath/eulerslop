MOD = 1_000_000_007
INV2 = (MOD + 1) // 2
INV8 = pow(8, MOD - 2, MOD)


def identity_and_diagonal(n):
    """Return identity and diagonal-reflection fixed counts modulo MOD."""
    fact = 1
    for k in range(1, n + 1):
        fact = fact * k % MOD

    if n == 0:
        identity = 1
    elif n == 1:
        identity = 0
    else:
        # Bipartite 2-regular graphs: exp(-z/2) / sqrt(1-z).
        prev, cur = 1, 0
        for k in range(1, n):
            nxt = (
                k * (k + 1) * cur
                + INV2 * (k + 1) % MOD * k % MOD * k % MOD * prev
            ) % MOD
            prev, cur = cur, nxt
        identity = cur

    diagonal_base = [1, 0, 1, 4]
    if n < len(diagonal_base):
        diagonal = diagonal_base[n]
    else:
        # Symmetric row-sum-2 matrices: loop-ended paths and loopless cycles.
        d0, d1, d2, d3 = diagonal_base
        for k in range(3, n):
            nxt = (
                2 * k * d3
                + (2 - k) * k * d2
                - INV2 * k % MOD * (k - 1) % MOD * (k - 2) % MOD * d0
            ) % MOD
            d0, d1, d2, d3 = d1, d2, d3, nxt
        diagonal = d3

    return identity, diagonal, fact


def vertical_reflection(n, fact):
    if n % 2:
        return 0
    return fact * pow(pow(2, n // 2, MOD), MOD - 2, MOD) % MOD


def half_turn(n):
    if n % 2 == 0:
        m = n // 2
        if m == 0:
            return 1
        prev, cur = 1, 1
        for k in range(1, m):
            nxt = (
                (k + 1) * (4 * k + 1) * cur
                + 4 * (k + 1) * k % MOD * k % MOD * prev
            ) % MOD
            prev, cur = cur, nxt
        return cur

    m = n // 2
    if m == 0:
        return 0
    if m == 1:
        return 2

    # Odd size leaves one deficient row-pair/column-pair connected by a path.
    prev, cur = 2, 10
    for t in range(1, m - 1):
        nxt = (
            (t + 1) * (4 * t + 5) * cur
            + 4 * (t + 1) * t % MOD * t % MOD * prev
        ) % MOD
        prev, cur = cur, nxt
    return m * m % MOD * cur % MOD


def quarter_turn(n):
    if n % 2:
        return 0
    m = n // 2
    if m == 0:
        return 1
    if m == 1:
        return 1
    if m == 2:
        return 2

    # C4 orbits are loops or two-colour edges in a 2-regular graph on n/2
    # opposite row/column pairs.
    older, prev, cur = 1, 1, 2
    for k in range(2, m):
        nxt = ((2 * k + 1) * cur - k * prev + 2 * k * (k - 1) * older) % MOD
        older, prev, cur = prev, cur, nxt
    return cur


def g(n):
    identity, diagonal, fact = identity_and_diagonal(n)
    vertical = vertical_reflection(n, fact)
    return (
        identity
        + 2 * vertical
        + half_turn(n)
        + 2 * diagonal
        + 2 * quarter_turn(n)
    ) * INV8 % MOD


def solve():
    assert g(4) == 20
    assert g(7) == 390816
    assert g(8) == 23462347
    return (g(7**7) + g(8**8)) % MOD


if __name__ == "__main__":
    print(solve())
