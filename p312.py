"""Project Euler 312: Cyclic paths on Sierpinski graphs.

S_{n+1} consists of three copies of S_n glued pairwise at three shared
corners.  A Hamiltonian cycle of S_{n+1}, restricted to one copy, must be a
single Hamiltonian path between that copy's two shared corners (any other
degree pattern at the shared corners leaves a path-union with an odd number
of endpoints or a closed subcycle).  Hence

    C(n+1) = P(n)^3

where P(n) = number of Hamiltonian paths of S_n between two given corners.
Decomposing a corner-to-corner Hamiltonian path of S_{n+1} the same way
(with E(n) = paths between two corners covering everything except the third
corner) yields, for n >= 2:

    P(n+1) = 2 P(n)^2 E(n),   E(n+1) = 2 P(n) E(n)^2,   P(2)=2, E(2)=3.

The ratio E/P = 3/2 is invariant, so P(n+1) = 3 P(n)^3 and

    C(n) = 2^(3^(n-2)) * 3^((3^(n-2)-3)/2)      for n >= 3.

C(C(C(10000))) mod 13^8 is computed by reducing the exponent tower with the
generalized Euler theorem:  a^x = a^(phi(m) + x mod phi(m)) (mod m) for any
a once x >= log2(m), recursing through the phi-chain of the modulus.
"""


# ---------- brute-force verification of the recurrence on real graphs ----------

def build_edges(n):
    """Sierpinski graph S_n; vertices are integer coords, corners
    (0,0), (s,0), (0,s) with s = 2^(n-1)."""
    edges = {frozenset(p) for p in (((0, 0), (1, 0)), ((0, 0), (0, 1)),
                                    ((1, 0), (0, 1)))}
    for k in range(1, n):
        s = 2 ** (k - 1)
        new = set(edges)
        for dx, dy in ((s, 0), (0, s)):
            for e in edges:
                (x1, y1), (x2, y2) = tuple(e)
                new.add(frozenset(((x1 + dx, y1 + dy), (x2 + dx, y2 + dy))))
        edges = new
    return edges


def adjacency(edges):
    adj = {}
    for e in edges:
        a, b = tuple(e)
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    return adj


def count_ham_cycles(adj):
    verts = sorted(adj)
    n = len(verts)
    start = verts[0]
    count = 0

    def dfs(v, visited, depth):
        nonlocal count
        for w in adj[v]:
            if w == start:
                if depth == n:
                    count += 1
            elif w not in visited:
                visited.add(w)
                dfs(w, visited, depth + 1)
                visited.remove(w)

    dfs(start, {start}, 1)
    return count // 2  # each cycle counted in both directions


def count_ham_paths(adj, u, v, skip=None):
    """Paths u -> v covering every vertex except `skip` (if given)."""
    need = len(adj) - (1 if skip is not None else 0)
    count = 0

    def dfs(x, visited, depth):
        nonlocal count
        if x == v:
            if depth == need:
                count += 1
            return
        for w in adj[x]:
            if w != skip and w not in visited:
                visited.add(w)
                dfs(w, visited, depth + 1)
                visited.remove(w)

    dfs(u, {u}, 1)
    return count


# ---------- closed form and modular machinery ----------

def C_exact(n):
    if n <= 2:
        return 1
    a = 3 ** (n - 2)
    return 2 ** a * 3 ** ((a - 3) // 2)


def C_mod_exact_n(n, m):
    """C(n) mod m for an exactly known n >= 3 (exponent 3^(n-2) kept exact)."""
    a = 3 ** (n - 2)
    return pow(2, a, m) * pow(3, (a - 3) // 2, m) % m


def phi(m):
    res, d, x = 1, 2, m
    while d * d <= x:
        if x % d == 0:
            x //= d
            pk = d
            while x % d == 0:
                x //= d
                pk *= d
            res *= pk - pk // d
        d += 1
    if x > 1:
        res *= x - 1
    return res


def C_reduce(n_mod, p2, m):
    """C(n) mod m given n mod p2 (= phi(2*phi(m))), assuming n is huge."""
    p = phi(m)
    m2 = 2 * p
    # a = 3^(n-2) mod 2*phi(m), generalized Euler (n-2 >> log2(m2))
    e = (n_mod - 2) % p2 + p2
    a2 = pow(3, e, m2)
    # 2^a mod m, generalized Euler (a >> log2(m))
    res = pow(2, a2 % p + p, m)
    # b = (a-3)/2 mod phi(m): a-3 is even, reduce mod 2*phi(m) then halve
    t = (a2 - 3) % m2
    res = res * pow(3, t // 2 + p, m) % m
    return res


def C_tower_mod(level, m):
    """V mod m, where V = C applied (level+1) times to 10000."""
    if m == 1:
        return 0
    if level == 0:
        return C_mod_exact_n(10000, m)
    p2 = phi(2 * phi(m))
    return C_reduce(C_tower_mod(level - 1, p2), p2, m)


def solve():
    # --- validate recurrence base values by brute force on S_2 and S_3 ---
    adj2 = adjacency(build_edges(2))
    assert count_ham_paths(adj2, (0, 0), (2, 0)) == 2            # P(2)
    assert count_ham_paths(adj2, (0, 0), (2, 0), skip=(0, 2)) == 3  # E(2)
    adj3 = adjacency(build_edges(3))
    assert count_ham_cycles(adj3) == 8                           # C(3) = P(2)^3
    assert count_ham_paths(adj3, (0, 0), (4, 0)) == 24           # P(3) = 2 P2^2 E2
    assert count_ham_paths(adj3, (0, 0), (4, 0), skip=(0, 4)) == 36  # E(3)

    # --- validate closed form against the values given in the statement ---
    assert C_exact(3) == 8
    assert C_exact(5) == 71328803586048
    assert C_mod_exact_n(10000, 10 ** 8) == 37652224
    assert C_mod_exact_n(10000, 13 ** 8) == 617720485

    # --- validate the exponent-tower reduction against exact computation ---
    for m in (13 ** 8, 10 ** 8, 24 * 13 ** 7, 12 * 13 ** 6):
        p2 = phi(2 * phi(m))
        for n in (100, 137, 5000):
            assert C_reduce(n % p2, p2, m) == C_mod_exact_n(n, m)

    # --- C(C(C(10000))) mod 13^8 ---
    return C_tower_mod(2, 13 ** 8)


if __name__ == "__main__":
    print(solve())
