// Project Euler 785: 15(x^2+y^2+z^2) = 34(xy+yz+zx).
//
// Putting s = x+y+z, the equation forces s = 8t and xy+yz+zx = 15t^2.
// Eliminating z = 8t-x-y gives x^2+xy+y^2 - 8t(x+y) + 15t^2 = 0, and with
// u = 3x-8t, v = 3y-8t this becomes  u^2+uv+v^2 = 57 t^2,
// i.e. N(w) = 57 t^2 for w = u - v*omega in the Eisenstein integers Z[w],
// N(a+b*omega) = a^2-ab+b^2.
//
// 57 = 3*19 with 3 = unit*lambda^2 (lambda = 1-omega) ramified and
// 19 = pi*conj(pi), pi = 5+2*omega, split.  For a primitive solution
// (gcd(x,y,z)=1) no rational prime p != 3 can divide w, so the split-prime
// part of w is lopsided and the exponents of lambda and pi(-bar) are odd:
// w = unit * gamma * beta^2 with gamma in {lambda*pi, lambda*conj(pi)}
// = {7-omega, 8+omega} (N=57) and t = N(beta).
//
// Enumerating beta = m+n*omega over one 60-degree sector (0 <= n < m), all
// 6 units and both gammas therefore produces every ordered primitive
// solution exactly once; the ordering x<y<z (no solutions have repeated
// coordinates since 15r^2-68r-4 has no rational roots) is the linear
// condition u < v, u+2v < 0.
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <numeric>
#include <thread>
#include <vector>

using namespace std;
typedef long long i64;
typedef unsigned long long u64;

static const int UNITS[6][2] = {
    {1, 0}, {0, 1}, {-1, -1}, {-1, 0}, {0, -1}, {1, 1}};
static const int GAMMAS[2][2] = {{7, -1}, {8, 1}};

// (a+b w)(c+d w) = (ac-bd) + (ad+bc-bd) w
static inline void emul(i64 a, i64 b, i64 c, i64 d, i64& ra, i64& rb) {
    ra = a * c - b * d;
    rb = a * d + b * c - b * d;
}

static u64 solve(i64 N) {
    const i64 T = 3 * N / 8;  // x+y+z = 8t <= 3N
    // gamma*unit combinations precomputed
    i64 ga[12], gb[12];
    for (int g = 0; g < 2; ++g)
        for (int e = 0; e < 6; ++e)
            emul(GAMMAS[g][0], GAMMAS[g][1], UNITS[e][0], UNITS[e][1],
                 ga[g * 6 + e], gb[g * 6 + e]);

    i64 mmax = 1;
    while (mmax * mmax - mmax * (mmax / 2) + (mmax / 2) * (mmax / 2) <= T)
        ++mmax;

    int nthreads = max(1u, thread::hardware_concurrency());
    vector<u64> partial(nthreads, 0);
    vector<thread> ths;
    for (int ti = 0; ti < nthreads; ++ti) {
        ths.emplace_back([&, ti]() {
            u64 acc = 0;
            for (i64 m = 1 + ti; m <= mmax; m += nthreads) {
                for (i64 n = 0; n < m; ++n) {
                    i64 t = m * m - m * n + n * n;
                    if (t > T) {
                        // norm is unimodal in n on [0,m): first decreasing
                        // then increasing; skip accordingly
                        if (2 * n >= m) break;
                        continue;
                    }
                    // beta^2 = (m^2-n^2) + (2mn-n^2) w
                    i64 sa = m * m - n * n, sb = 2 * m * n - n * n;
                    i64 t8 = 8 * t;
                    for (int c = 0; c < 12; ++c) {
                        i64 wa, wb;
                        emul(sa, sb, ga[c], gb[c], wa, wb);
                        i64 u = wa, v = -wb;
                        if (u >= v || u + 2 * v >= 0) continue;
                        if ((u - t) % 3 != 0 || (v - t) % 3 != 0) continue;
                        i64 x = (u + t8) / 3, y = (v + t8) / 3,
                            z = (t8 - u - v) / 3;
                        if (x < 1 || z > N) continue;
                        if (gcd(x, gcd(y, z)) != 1) continue;
                        acc += (u64)t8;
                    }
                }
            }
            partial[ti] = acc;
        });
    }
    for (auto& th : ths) th.join();
    u64 s = 0;
    for (u64 p : partial) s += p;
    return s;
}

static u64 brute(i64 N) {
    u64 s = 0;
    for (i64 x = 1; x <= N; ++x)
        for (i64 y = x; y <= N; ++y) {
            // 15 z^2 - 34(x+y) z + 15(x^2+y^2) - 34 x y = 0
            i64 b = 34 * (x + y), c = 15 * (x * x + y * y) - 34 * x * y;
            i64 disc = b * b - 60 * c;
            if (disc < 0) continue;
            i64 r = (i64)sqrtl((long double)disc);
            while (r * r < disc) ++r;
            while (r * r > disc) --r;
            if (r * r != disc) continue;
            for (i64 z : {(b - r) / 30, (b + r) / 30}) {
                if (z < y || z > N) continue;
                if (15 * z * z - b * z + c != 0) continue;
                if (gcd(x, gcd(y, z)) != 1) continue;
                s += (u64)(x + y + z);
                if ((b - r) / 30 == (b + r) / 30) break;
            }
        }
    return s;
}

int main() {
    if (solve(100) != 184 || solve(100) != brute(100) ||
        solve(2000) != brute(2000)) {
        fprintf(stderr, "self-test failed: solve(100)=%llu brute=%llu "
                        "solve(2000)=%llu brute=%llu\n",
                solve(100), brute(100), solve(2000), brute(2000));
        return 1;
    }
    printf("%llu\n", solve(1000000000LL));
    return 0;
}
