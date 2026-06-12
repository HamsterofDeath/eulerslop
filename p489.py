#!/usr/bin/env python3


def _resultant(a, b):
    f = [1, 0, 0, b]
    g = [1, 3 * a, 3 * a * a, a ** 3 + b]
    mat = [f + [0, 0], [0] + f + [0], [0, 0] + f,
           g + [0, 0], [0] + g + [0], [0, 0] + g]
    prev = 1
    sign = 1
    n = len(mat)
    for k in range(n - 1):
        if mat[k][k] == 0:
            for i in range(k + 1, n):
                if mat[i][k]:
                    mat[k], mat[i] = mat[i], mat[k]
                    sign *= -1
                    break
        pivot = mat[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                mat[i][j] = (mat[i][j] * pivot - mat[i][k] * mat[k][j]) // prev
        prev = pivot
    return abs(sign * mat[-1][-1])


def _factor(n):
    out = []
    p = 2
    while p * p <= n:
        if n % p == 0:
            e = 0
            while n % p == 0:
                n //= p
                e += 1
            out.append((p, e))
        p += 1 if p == 2 else 2
    if n > 1:
        out.append((n, 1))
    return out


def _sqrt_mod_prime(a, p):
    a %= p
    if p == 2:
        return [a]
    if pow(a, (p - 1) // 2, p) != 1:
        return []
    if p % 4 == 3:
        r = pow(a, (p + 1) // 4, p)
        return sorted({r, (-r) % p})

    q = p - 1
    s = 0
    while q % 2 == 0:
        s += 1
        q //= 2
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
    m = s
    c = pow(z, q, p)
    t = pow(a, q, p)
    r = pow(a, (q + 1) // 2, p)
    while t != 1:
        i = 1
        tt = t * t % p
        while tt != 1:
            tt = tt * tt % p
            i += 1
        b = pow(c, 1 << (m - i - 1), p)
        m = i
        c = b * b % p
        t = t * c % p
        r = r * b % p
    return sorted({r, (-r) % p})


def _roots_mod_p(a, b, p):
    if p <= 3 or a % p == 0:
        return [
            n for n in range(p)
            if (n ** 3 + b) % p == 0 and ((n + a) ** 3 + b) % p == 0
        ]

    roots = []
    inv6 = pow(6, -1, p)
    for s in _sqrt_mod_prime(-3, p):
        n = (-3 * a + a * s) * inv6 % p
        if (pow(n, 3, p) + b) % p == 0 and (pow(n + a, 3, p) + b) % p == 0:
            roots.append(n)
    return sorted(set(roots))


def _local_roots(a, b, p, exponent):
    roots = _roots_mod_p(a, b, p)
    modulus = p
    best_modulus = modulus if roots else 1
    best_roots = roots[:]
    for _ in range(1, exponent):
        if not roots:
            break
        next_modulus = modulus * p
        new_roots = []
        for r in roots:
            for k in range(p):
                x = r + k * modulus
                if ((pow(x, 3, next_modulus) + b) % next_modulus == 0
                        and (pow(x + a, 3, next_modulus) + b) % next_modulus == 0):
                    new_roots.append(x)
        roots = sorted(set(new_roots))
        modulus = next_modulus
        if roots:
            best_modulus = modulus
            best_roots = roots[:]
    return best_modulus, best_roots


def G(a, b):
    states = [(0, 1)]
    for p, exponent in _factor(_resultant(a, b)):
        modulus, roots = _local_roots(a, b, p, exponent)
        if modulus == 1:
            continue
        combined = []
        for r1, m1 in states:
            inv = pow(m1, -1, modulus)
            for r2 in roots:
                t = ((r2 - r1) % modulus) * inv % modulus
                combined.append((r1 + m1 * t, m1 * modulus))
        states = combined
    return min(r for r, _ in states)


def H(m, n):
    return sum(G(a, b) for a in range(1, m + 1) for b in range(1, n + 1))


def solve():
    assert G(1, 1) == 5
    assert H(5, 5) == 128878
    assert H(10, 10) == 32936544
    return H(18, 1900)


if __name__ == "__main__":
    print(solve())
