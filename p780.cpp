// Project Euler 780: toroidal tilings by unit equilateral triangles,
// G(1e9) mod 1e9+7.
//
// A tiling of a rectangular a x b torus by n = 2m unit triangles is a stack
// of k parallel strips of circumference c (kc = m), whose common direction
// closes up as a (p,q) loop: c^2 = (pa)^2 + (qb)^2, ab = m*sqrt(3)/2.
// Sliding strips along their fault lines is a legal motion, so on a fixed
// torus each (direction, k, c) gives one class, except that all three edge
// directions of an edge-to-edge (lattice) structure merge into a single
// class.  Lattice structures correspond to embeddings Lambda = <s*u, t*u_perp>
// with u a primitive Eisenstein vector of norm Q (3 nmid Q), u_perp of norm
// 3Q, st = m/(2Q); embeddings are counted up to 60-degree rotations, i.e.
// with weight h(Q) = 2^omega(Q) if every prime factor of Q is 1 mod 3
// (h(1)=1, else 0), times 2 rectangle orientations.
// Hence, with M = N/2:
//   tuples: axes 2*Dtil(M);  diagonals 4*D(M),
//     D(M) = sum_{k>=1} sum_{t=pq, gcd(p,q)=1} (floor(M/k) - floor(sqrt3 t k))^+
//          = sum_{k,t} 2^omega(t) (...)   (t = pq, coprime ordered pairs)
//   embeddings: A(M) = 2 * sum_Q h(Q) Dtil(floor(M/(2Q)))
//   G(N) = 2*Dtil(M) + 4*D(M) - 2*A(M)
// (each embedding accounts for 3 tuples merged into 1 class: -2 per
// embedding).  Verified: G(6)=14, G(100)=8090, G(1e5) mod p = 645124048.
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <thread>
#include <unordered_map>
#include <vector>

using namespace std;
typedef unsigned long long u64;
typedef long long i64;
typedef __int128 i128;

static const u64 MOD = 1000000007ULL;

static i64 isqrt64(i64 x) {
    if (x < 0) return -1;
    i64 r = (i64)sqrtl((long double)x);
    while (r * r > x) --r;
    while ((r + 1) * (r + 1) <= x) ++r;
    return r;
}

static u64 Dtil(i64 x) {  // sum floor(x/k), exact (fits u64 for x <= 5e8)
    u64 s = 0;
    for (i64 k = 1; k <= x;) {
        i64 v = x / k, k2 = x / v;
        s += (u64)v * (u64)(k2 - k + 1);
        k = k2 + 1;
    }
    return s;
}

// omega sieve (number of distinct prime factors) for 2..lim, and
// "good" flag: all prime factors == 1 mod 3
static void sieve_omega(i64 lim, vector<uint8_t>& om, vector<uint8_t>& bad) {
    om.assign(lim + 1, 0);
    bad.assign(lim + 1, 0);
    vector<char> comp(lim + 1, 0);
    for (i64 p = 2; p <= lim; ++p) {
        if (comp[p]) continue;
        bool pbad = (p % 3 != 1);
        for (i64 j = p; j <= lim; j += p) {
            if (j > p) comp[j] = 1;
            om[j]++;
            if (pbad) bad[j] = 1;
        }
    }
}

static u64 solve(i64 N) {
    const i64 M = N / 2;
    // sieve up to max(M/sqrt3, M/2)
    i64 lim_t = (i64)((long double)M / sqrtl(3.0L)) + 2;
    i64 lim_q = M / 2;
    i64 lim = max(lim_t, lim_q);
    vector<uint8_t> om, bad;
    sieve_omega(lim, om, bad);

    // ---- D(M) ----
    int nth = max(1u, thread::hardware_concurrency());
    i64 kmax = isqrt64((i64)((long double)M / sqrtl(3.0L))) + 2;
    vector<u64> partD(nth, 0);
    {
        vector<thread> ths;
        for (int ti = 0; ti < nth; ++ti)
            ths.emplace_back([&, ti]() {
                u64 acc = 0;  // mod-reduced accumulator
                for (i64 k = 1 + ti; ; k += nth) {
                    i64 Mk = M / k;
                    if (isqrt64(3 * k * k) >= Mk) { if (k > kmax + nth) break; else continue; }
                    u64 lacc = 0;  // per-k, fits u64
                    // f3(t) = floor(sqrt(3) t k) via incremental isqrt
                    i64 base = 0;  // f3 for current t
                    i64 d0 = isqrt64(3 * k * k);  // approx step
                    i64 t = 1;
                    base = isqrt64(3 * k * k);  // t=1
                    while (base < Mk) {
                        u64 w = 1u << om[t];
                        lacc += w * (u64)(Mk - base);
                        ++t;
                        i64 v = 3 * k * k * t * t;
                        base += d0;
                        while (base * base > v) --base;
                        while ((base + 1) * (base + 1) <= v) ++base;
                    }
                    acc = (acc + lacc % MOD) % MOD;
                }
                partD[ti] = acc;
            });
        for (auto& t : ths) t.join();
    }
    u64 D = 0;
    for (u64 v : partD) D = (D + v) % MOD;

    // ---- A(M) = 2 sum_Q h(Q) Dtil(M/(2Q)) ----
    // memoize Dtil on quotient values
    unordered_map<i64, u64> dmemo;
    auto DtilM = [&](i64 x) {
        auto it = dmemo.find(x);
        if (it != dmemo.end()) return it->second;
        u64 v = Dtil(x) % MOD;
        dmemo.emplace(x, v);
        return v;
    };
    vector<u64> partA(nth, 0);
    {
        // parallel over Q with per-thread local memo would race; do serial
        // grouped by quotient blocks: for large Q, Dtil arg constant.
        u64 acc = 0;
        for (i64 Q = 1; 2 * Q <= M; ++Q) {
            if (Q > 1 && (bad[Q] || om[Q] == 0)) continue;
            u64 hh = (Q == 1) ? 1 : (1u << om[Q]);
            acc = (acc + hh % MOD * DtilM(M / (2 * Q))) % MOD;
        }
        partA[0] = acc;
    }
    u64 A = 2 * partA[0] % MOD;

    u64 G = (2 * (Dtil(M) % MOD) % MOD + 4 * D % MOD + 2 * (MOD - A) % MOD) % MOD;
    return G;
}

int main() {
    if (solve(6) != 14 || solve(100) != 8090 || solve(100000) != 645124048ULL) {
        fprintf(stderr, "self-test failed: %llu %llu %llu\n", solve(6),
                solve(100), solve(100000));
        return 1;
    }
    printf("%llu\n", solve(1000000000LL));
    return 0;
}
