import math
from bisect import bisect_left, bisect_right


def _icbrt(n):
    x = int(round(n ** (1.0 / 3)))
    while x * x * x > n:
        x -= 1
    while (x + 1) ** 3 <= n:
        x += 1
    return x


def _products(pe):
    # all products p1^i1 * ... for 0 <= i <= e
    vals = [1]
    for p, e in pe:
        pw = [p**i for i in range(e + 1)]
        vals = [v * w for v in vals for w in pw]
    return vals


def best_triple(n, pe):
    # Minimise c/a over a <= b <= c, abc = n.  Any triple with ratio r has
    # all of a, b, c within factor r^(2/3) of n^(1/3), so divisors in a
    # window [cbrt/e^w, cbrt*e^w] suffice once r^(2/3) <= e^w.  Divisors in
    # the window come from a meet-in-the-middle split of the prime powers.
    cbrt = _icbrt(n)
    # split primes so the first half's divisor count ~ sqrt of total
    tot = 1
    for _, e in pe:
        tot *= e + 1
    half1, half2, c1 = [], [], 1
    for p, e in pe:
        if c1 * c1 < tot:
            half1.append((p, e))
            c1 *= e + 1
        else:
            half2.append((p, e))
    g1 = sorted(_products(half1))
    g2 = _products(half2)

    w = 2e-6
    while True:
        lo = max(1, int(cbrt * math.exp(-w)))
        hi = min(n, int(cbrt * math.exp(w)) + 1)
        W = []
        for v in g2:
            if v > hi:
                continue
            i = bisect_left(g1, -(-lo // v))
            j = bisect_right(g1, hi // v)
            for k in range(i, j):
                W.append(v * g1[k])
        W.sort()
        m = bisect_right(W, cbrt)
        A = W[:m][::-1]  # divisors <= cbrt, descending
        C = W[m:]        # divisors > cbrt, ascending
        best = None      # (a, b, c)
        full = lo <= 1 and hi >= n
        # only triples with ratio <= e^{1.5w} are guaranteed inside the window
        bound = math.inf if full else math.exp(1.5 * w)
        if A:
            amax = A[0]
            for c in C:
                if c > amax * bound:
                    break
                for a in A:
                    if c > a * bound or (best and c * best[0] >= best[2] * a):
                        break
                    ac = a * c
                    if n % ac == 0:
                        b = n // ac
                        if a <= b <= c and (best is None
                                            or c * best[0] < best[2] * a):
                            best = (a, b, c)
        if full:
            return best  # searched everything
        if best is not None:
            r = best[2] / best[0]
            if (2.0 / 3.0) * math.log(r) <= 0.99 * w:  # window provably covers
                return best
        w *= 2


def solve():
    n = math.factorial(43)
    pe = []
    p = 2
    while p <= 43:
        if all(p % q for q in range(2, p)):
            e, t = 0, p
            while t <= 43:
                e += 43 // t
                t *= p
            pe.append((p, e))
        p += 1
    a, b, c = best_triple(n, pe)
    return a + b + c


if __name__ == "__main__":
    print(solve())
