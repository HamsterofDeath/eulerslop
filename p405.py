from collections import Counter


def f_small(n):
    # Simulate the substitution tiling with integer coords scaled by 2^n.
    # Rule (from the picture): a horizontal 2s x s tile splits into two
    # vertical tiles at its ends and two horizontal tiles stacked in the
    # middle; a vertical tile uses the 90-degree rotated rule.
    tiles = [(0, 0, 0)]  # (x, y, orientation); 0 = horizontal, 1 = vertical
    s = 1 << n
    for _ in range(n):
        h = s >> 1
        new = []
        for x, y, o in tiles:
            if o == 0:
                new += [(x, y, 1), (x + s + h, y, 1),
                        (x + h, y, 0), (x + h, y + h, 0)]
            else:
                new += [(x, y, 0), (x, y + s + h, 0),
                        (x, y + h, 1), (x + h, y + h, 1)]
        tiles = new
        s = h
    # Four tiles meet at a point iff it is a corner of exactly four tiles
    # (four 90-degree corners; a T-junction has only three incident tiles).
    c = Counter()
    for x, y, o in tiles:
        w, hh = (2 * s, s) if o == 0 else (s, 2 * s)
        for p in ((x, y), (x + w, y), (x, y + hh), (x + w, y + hh)):
            c[p] += 1
    return sum(1 for v in c.values() if v == 4)


def solve():
    # Simulation gives f = 0,0,2,16,82,368,1554,6384,25874,... whose linear
    # recurrence has roots 4,2,1,-1: f(n) = (6*4^n - 20*2^n + 15 - (-1)^n)/15.
    for n in range(9):
        assert f_small(n) == (6 * 4**n - 20 * 2**n + 15 - (-1)**n) // 15
    M = 17**7
    assert f_small(1) == 0 and f_small(4) == 82
    inv15 = pow(15, -1, M)
    # given check value f(10^9) mod 17^7
    n = 10**9
    assert (6 * pow(4, n, M) - 20 * pow(2, n, M) + 14) * inv15 % M == 126897180

    # Target n = 10^K with K = 10^18.  Since gcd(2,17)=1 we may reduce the
    # exponent modulo phi(17^7) = 16*17^6, computed by CRT:
    #   n mod 16    = 0           (16 | 10^4 | 10^K)
    #   n mod 17^6  = 10^(K mod phi(17^6)) mod 17^6   (Euler, gcd(10,17)=1)
    K = 10**18
    m17 = 17**6
    e2 = pow(10, K % (16 * 17**5), m17)
    e = 16 * ((e2 * pow(16, -1, m17)) % m17)  # CRT: e=0 mod 16, e=e2 mod 17^6
    # n = 10^K is even, so (-1)^n = 1
    return (6 * pow(4, e, M) - 20 * pow(2, e, M) + 14) * inv15 % M


if __name__ == "__main__":
    print(solve())
