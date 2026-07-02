// Project Euler 786: billiard in the 120-90-60-90 kite, B(1e9).
//
// The table is two 30-60-90 triangles glued along the long leg, i.e. two
// fundamental domains of the p6m kaleidoscope.  Unfolding maps traces
// A -> ... -> A to straight segments between triangle centroids of the
// (side-6, integer coordinate) triangular lattice; crossings of edge lines
// always bounce, crossings of median lines bounce only on their
// centroid-midpoint thirds (position tau mod 6 in (2,4)), and touching any
// vertex/centroid/midpoint means hitting a corner.
//
// Empirically-verified consequences (brute lattice count / 3 reproduces
// B(10)=6, B(100)=478):
//  * every valid target is 6*(a,b) with gcd(a,b)=1 and a != b (mod 3);
//  * each median family with q = |a-b|, |2a+b|, |a+2b| contributes
//    ceil(q/3)-1 bounces (the crossing fractions {k p/q} sweep 1/q..);
//  * edge families contribute |a|+|b|+|a+b|.
// Hence 3*bounces = 3(|a|+|b|+|a+b|) + |a-b|+|2a+b|+|a+2b| - rho,
// rho = 4 or 5 for (a-b) mod 3 = 1 or 2.  The count is 12-fold symmetric;
// on the open sector a > b >= 1 the form is 10a+8b, plus the 6 axis traces
// (2 bounces each):
//   B(N) = 4 * #{a>b>=1: gcd=1, a!=b mod 3, 10a+8b <= 3N+rho} + 2.
// The gcd condition is removed by Moebius (3|d impossible).
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <thread>
#include <vector>

using namespace std;
typedef long long i64;

static vector<int8_t> mu;

static void sieve_mu(i64 n) {
    mu.assign(n + 1, 1);
    vector<char> comp(n + 1, 0);
    vector<int> primes;
    vector<int8_t> m(n + 1);
    m[1] = 1;
    for (i64 i = 2; i <= n; ++i) {
        if (!comp[i]) { primes.push_back(i); m[i] = -1; }
        for (int p : primes) {
            i64 j = i * p;
            if (j > n) break;
            comp[j] = 1;
            if (i % p == 0) { m[j] = 0; break; }
            m[j] = -m[i];
        }
    }
    mu = move(m);
}

// #{(s,t): s>t>=1, s !== t (mod 3), 10 d s + 8 d t <= 3N + rho(d(s-t) mod 3)}
static i64 inner(i64 N, i64 d) {
    i64 cnt = 0;
    // iterate residue classes (sigma, tau) mod 3 with sigma != tau
    for (int sg = 0; sg < 3; ++sg)
        for (int tg = 0; tg < 3; ++tg) {
            if (sg == tg) continue;
            int r = (int)((i64)(sg - tg + 3) * d % 3);
            i64 C = 3 * N + (r == 1 ? 4 : 5);
            // t >= 1, t == tg mod 3; s in [t+1, (C-8dt)/(10d)], s == sg mod 3
            for (i64 t = (tg == 0 ? 3 : tg);; t += 3) {
                i64 rem = C - 8 * d * t;
                if (rem < 10 * d * (t + 1)) break;
                i64 smax = rem / (10 * d);
                i64 smin = t + 1;
                // count s in [smin, smax] with s == sg (mod 3)
                i64 lo = smin + ((sg - smin) % 3 + 3) % 3;
                if (lo <= smax) cnt += (smax - lo) / 3 + 1;
            }
        }
    return cnt;
}

static i64 B(i64 N) {
    if (N < 2) return 0;
    i64 dmax = (3 * N + 5) / 18;  // 10ds+8dt >= 18d for s=... minimal s>t>=1: s=2,t=1: 28d
    dmax = (3 * N + 5) / 28;
    if ((i64)mu.size() <= dmax) sieve_mu(dmax + 1);
    int nth = max(1u, thread::hardware_concurrency());
    vector<i64> part(nth, 0);
    vector<thread> ths;
    for (int ti = 0; ti < nth; ++ti)
        ths.emplace_back([&, ti]() {
            i64 acc = 0;
            for (i64 d = 1 + ti; d <= dmax; d += nth) {
                if (d % 3 == 0 || mu[d] == 0) continue;
                acc += (i64)mu[d] * inner(N, d);
            }
            part[ti] = acc;
        });
    for (auto& t : ths) t.join();
    i64 sector = 0;
    for (i64 v : part) sector += v;
    return 4 * sector + 2;
}

int main() {
    sieve_mu((3LL * 1000000000 + 5) / 28 + 2);
    if (B(10) != 6 || B(100) != 478 || B(1000) != 45790) {
        fprintf(stderr, "self-test failed: %lld %lld %lld\n", B(10), B(100),
                B(1000));
        return 1;
    }
    printf("%lld\n", B(1000000000LL));
    return 0;
}
