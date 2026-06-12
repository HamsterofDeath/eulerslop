"""Project Euler 403: Lattice points enclosed by parabola and line.

Area between y = x^2 and y = ax+b is (a^2+4b)^{3/2}/6, rational iff
a^2 + 4b = d^2 (d >= 0).  Then d = a (mod 2), so the roots
u = (a-d)/2 <= v = (a+d)/2 are integers: bijection (a,b) <-> (u <= v)
with a = u+v, b = -uv, d = v-u.  Lattice count:
L = sum_{x=u}^{v} (x-u)(v-x) + (v-u+1) = (d^3 + 5d + 6)/6 =: g(d).

S(N) = sum over u <= v, |u+v| <= N, |uv| <= N of g(v-u).  Split:
 * A: 1 <= u <= v, uv <= N (then u+v <= N except the single pair (1,N))
   -> sum_u G(floor(N/u) - u) - g(N-1), G = partial sums of g.
 * B: u <= v <= -1, equals A by the symmetry (u,v) -> (-v,-u).
 * C: u = -p <= 0 <= v: rows p=0 / v=0 give G(N) and G(N)-1; for
   p,v >= 1 only pv <= N binds -> hyperbola sums of p^i v^j in
   O(sqrt N) blocks (exact integer arithmetic).
"""


def solve():
    N = 10**12
    MOD = 10**8

    def g(d):
        return (d**3 + 5*d + 6) // 6

    def G(t):  # sum_{d=0}^{t} g(d)
        h = t * (t + 1) // 2
        return (h * h + 5 * h + 6 * (t + 1)) // 6

    # Case A (doubled later for case B)
    A = 0
    u = 1
    while u * u <= N:
        A += G(N // u - u)
        u += 1
    A -= g(N - 1)  # pair (u,v) = (1,N) has |u+v| = N+1 > N

    # Case C boundary rows: p = 0 (v = 0..N) and v = 0 (p = 1..N)
    C = 2 * G(N) - 1

    # H = sum_{p,v>=1, pv<=N} g(p+v)
    #   = (2*T30 + 6*T21 + 10*T10 + 6*T00)/6 with T_ij = sum p^i v^j
    def S2(n):
        return n * (n + 1) * (2 * n + 1) // 6

    def S3(n):
        return (n * (n + 1) // 2) ** 2

    T00 = T10 = T30 = T21 = 0
    p = 1
    while p <= N:
        q = N // p
        r = N // q  # largest p' with floor(N/p') == q
        cnt = r - p + 1
        s1 = (p + r) * cnt // 2
        s2 = S2(r) - S2(p - 1)
        s3 = S3(r) - S3(p - 1)
        T00 += cnt * q
        T10 += s1 * q
        T30 += s3 * q
        T21 += s2 * (q * (q + 1) // 2)
        p = r + 1
    H = (2 * T30 + 6 * T21 + 10 * T10 + 6 * T00) // 6

    return (2 * A + C + H) % MOD


if __name__ == "__main__":
    print(solve())
