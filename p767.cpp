// Project Euler 767: 16 x n binary matrices where every 2 x k window sums
// to k, for k = 1e5, n = 1e16, mod 1e9+7.
//
// Sliding a 2xk window one column shows the "adjacent-row pair sums"
// profile p(col) in {0,1,2}^15 is periodic with period k, so the columns of
// each residue class mod k share one profile.  A profile with some entry
// != 1 forces the whole 16-bit column vector (0/2 pin both bits, 1 links
// them alternately), so profiles correspond to column vectors; only the
// all-ones profile has two vectors (the two alternating ones), and a class
// with that profile lets each of its n/k columns choose freely: factor
// 2^(n/k).  The window-sum constraint says the k class profiles sum to k in
// every coordinate.
//
// With j classes on the all-ones profile the rest need per-coordinate sum
// c = k-j using non-alternating vectors, whose count by inclusion-exclusion
// over rows using the two alternating vectors collapses to
//   W(c) = sum_{m<=c} (-1)^(c-m) C(c,c-m) 2^(c-m) g(m),
//   g(m) = sum_a C(m,a)^16
// (columns of the c x 16 assignment matrix are independent given the
// alternating column sums s, k-j-s, ..., and the s-sum telescopes into g).
// Finally B = sum_j C(k,j) * (2^(n/k))^j * W(k-j)  (valid since k | n).
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <thread>
#include <vector>

using namespace std;
typedef unsigned long long u64;
typedef __uint128_t u128;

static const u64 MOD = 1000000007ULL;

static inline u64 mulm(u64 a, u64 b) { return (u128)a * b % MOD; }
static u64 powm(u64 a, u64 e) {
    u64 r = 1;
    a %= MOD;
    while (e) {
        if (e & 1) r = mulm(r, a);
        a = mulm(a, a);
        e >>= 1;
    }
    return r;
}

static u64 solve(u64 k, u64 n) {
    if (n % k) {
        fprintf(stderr, "need k | n\n");
        exit(1);
    }
    vector<u64> fact(k + 1), invf(k + 1);
    fact[0] = 1;
    for (u64 i = 1; i <= k; ++i) fact[i] = mulm(fact[i - 1], i);
    invf[k] = powm(fact[k], MOD - 2);
    for (u64 i = k; i > 0; --i) invf[i - 1] = mulm(invf[i], i);

    int nth = max(1u, thread::hardware_concurrency());
    // g[m] = sum_a C(m,a)^16
    vector<u64> g(k + 1);
    {
        vector<thread> ths;
        for (int ti = 0; ti < nth; ++ti)
            ths.emplace_back([&, ti]() {
                for (u64 m = ti; m <= k; m += nth) {
                    u64 s = 0;
                    for (u64 a = 0; 2 * a < m; ++a) {
                        u64 c = mulm(fact[m], mulm(invf[a], invf[m - a]));
                        c = mulm(c, c); c = mulm(c, c);
                        c = mulm(c, c); c = mulm(c, c);
                        s += 2 * c;
                        if (s >= 4 * MOD) s -= 4 * MOD;
                    }
                    s %= MOD;
                    if (m % 2 == 0) {
                        u64 c = mulm(fact[m], mulm(invf[m / 2], invf[m / 2]));
                        c = mulm(c, c); c = mulm(c, c);
                        c = mulm(c, c); c = mulm(c, c);
                        s = (s + c) % MOD;
                    }
                    g[m] = s;
                }
            });
        for (auto& t : ths) t.join();
    }
    // W[c] = fact[c] * sum_t q[t] h[c-t],
    // q[t] = (-1)^t invf[t] 2^t, h[m] = invf[m] g[m]
    vector<u64> q(k + 1), h(k + 1), W(k + 1);
    {
        u64 pw = 1;
        for (u64 t = 0; t <= k; ++t) {
            u64 v = mulm(invf[t], pw);
            q[t] = (t & 1) ? MOD - v : v;
            h[t] = mulm(invf[t], g[t]);
            pw = mulm(pw, 2);
        }
        vector<thread> ths;
        for (int ti = 0; ti < nth; ++ti)
            ths.emplace_back([&, ti]() {
                for (u64 c = ti; c <= k; c += nth) {
                    u64 s = 0;
                    for (u64 t = 0; t <= c; ++t) {
                        s += mulm(q[t], h[c - t]);
                        if (s >= 4 * MOD) s -= 4 * MOD;
                    }
                    W[c] = mulm(fact[c], s % MOD);
                }
            });
        for (auto& t : ths) t.join();
    }
    u64 a = powm(2, n / k);
    u64 b = 0, aj = 1;
    for (u64 j = 0; j <= k; ++j) {
        u64 cj = mulm(fact[k], mulm(invf[j], invf[k - j]));
        b = (b + mulm(mulm(cj, aj), W[k - j])) % MOD;
        aj = mulm(aj, a);
    }
    return b;
}

int main() {
    if (solve(2, 4) != 65550 || solve(3, 9) != 87273560) {
        fprintf(stderr, "self-test failed: %llu %llu\n", solve(2, 4),
                solve(3, 9));
        return 1;
    }
    printf("%llu\n", solve(100000, 10000000000000000ULL));
    return 0;
}
