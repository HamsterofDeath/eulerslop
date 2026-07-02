// Project Euler 798: card stacking game, C(1e7, 1e7) mod 1e9+7.
//
// The game splits into s independent per-suit games; the first player
// loses iff the XOR of the suit Grundy values is 0.
//
// Per suit, a position is the set of visible values; encode it by the gap
// vector g_1..g_k (fresh values between consecutive visible cards, g_k
// above the top card).  Values below the minimum are dead, so a subset of
// {1..n} corresponds to exactly one gap vector with weight k + sum(g) <= n.
// Brute force (validated for all subsets with n <= 13) shows the Grundy
// value is: with r = index of first even gap (none -> G = sum of gaps),
//   G = (g_1+...+g_r) + h_r(T),  T = g_{r+1}+...+g_k,
//   h_r(T) = T if T <= r else r - ((T-r) mod 2).
//
// Counting subsets by Grundy value with generating functions (leading odd
// gaps / first even gap / conjugated tail) collapses miraculously to
//   sum_v N_v x^v = [z^n]  z (1-z-z^2)(1-z+xz) / ((1-2z)(1-z)(1-z-x^2z^2))
// (weight-cumulative), giving with g_a(t) = [z^t] (1-2z)^{-1} (1-z)^{-a}:
//   N_{2b}   = D(b+1, n-2b-1),  N_{2b+1} = D(b+2, n-2b-2),  N_0 += 1,
//   D(a,t) = g_a(t) - g_a(t-1) - g_a(t-2).
// g_a(t) = 2^t H(a-1,t), H(j,T) = sum_{i<=T} 2^{-i} C(i+j,j), with O(1)
// steps H(j+1,T) = 2H(j,T) - 2^{-T} C(T+j+1,j+1) and
// H(j,T-1) = H(j,T) - 2^{-T} C(T+j,j).
//
// Finally #losing = 2^{-L} sum_w (WHT(N)_w)^s over w < 2^L.
// Self-tests: C(3,2)=26, C(13,4)=540318329, N-distribution for n=12.
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

static vector<u64> fact, invf, pw2, ipw2;

static void tables(u64 m) {
    fact.resize(m + 1); invf.resize(m + 1);
    pw2.resize(m + 1); ipw2.resize(m + 1);
    fact[0] = 1;
    for (u64 i = 1; i <= m; ++i) fact[i] = mulm(fact[i - 1], i);
    invf[m] = powm(fact[m], MOD - 2);
    for (u64 i = m; i > 0; --i) invf[i - 1] = mulm(invf[i], i);
    pw2[0] = ipw2[0] = 1;
    u64 i2 = powm(2, MOD - 2);
    for (u64 i = 1; i <= m; ++i) {
        pw2[i] = mulm(pw2[i - 1], 2);
        ipw2[i] = mulm(ipw2[i - 1], i2);
    }
}

static inline u64 C(long long a, long long b) {
    if (b < 0 || a < 0 || b > a) return 0;
    return mulm(fact[a], mulm(invf[b], invf[a - b]));
}

// distribution N_v (v = 0..n-1) of per-suit Grundy values over subsets
static vector<u64> grundy_dist(long long n) {
    vector<u64> N(n + 1, 0);
    // family: parity 0: a = b+1, t = n-2b-1 ; parity 1: a = b+2, t = n-2b-2
    for (int par = 0; par < 2; ++par) {
        long long j = (par == 0) ? 0 : 1;     // j = a-1
        long long t = n - 1 - par;
        // H(j, t)
        u64 H = 0;
        {
            // H(0, T) = sum 2^{-i} = 2 - 2^{-T}
            long long T0 = t;
            if (T0 < 0) continue;
            H = (2 + MOD - ipw2[T0]) % MOD;
            for (long long jj = 1; jj <= j; ++jj)
                H = (2 * H % MOD + MOD - mulm(ipw2[T0], C(T0 + jj, jj))) % MOD;
        }
        for (long long b = 0;; ++b) {
            long long v = 2 * b + par;
            if (v > n || t < 0) break;
            // need H(j,t), H(j,t-1), H(j,t-2)
            u64 H1 = (t >= 1) ? (H + MOD - mulm(ipw2[t], C(t + j, j))) % MOD : 0;
            u64 H2 = (t >= 2) ? (H1 + MOD - mulm(ipw2[t - 1], C(t - 1 + j, j))) % MOD : 0;
            u64 g0 = mulm(pw2[t], H);
            u64 g1 = (t >= 1) ? mulm(pw2[t - 1], H1) : 0;
            u64 g2 = (t >= 2) ? mulm(pw2[t - 2], H2) : 0;
            if (v <= n) N[v] = (g0 + 2 * MOD - g1 - g2) % MOD;
            // advance: j+1, t-2
            if (t < 2) break;
            u64 Hn = (2 * H2 % MOD + MOD - mulm(ipw2[t - 2], C(t - 2 + j + 1, j + 1))) % MOD;
            H = Hn;
            j += 1;
            t -= 2;
        }
    }
    N[0] = (N[0] + 1) % MOD;  // empty subset
    return N;
}

static u64 solve(long long n, u64 s) {
    vector<u64> N = grundy_dist(n);
    int L = 1;
    while ((1LL << L) <= n) ++L;
    size_t sz = (size_t)1 << L;
    vector<u64> A(sz, 0);
    for (long long v = 0; v <= n; ++v) A[v] = N[v];
    // WHT mod p
    for (int len = 1; len < (int)sz; len <<= 1)
        for (size_t i = 0; i < sz; i += 2 * len)
            for (size_t k = i; k < i + (size_t)len; ++k) {
                u64 u = A[k], w = A[k + len];
                A[k] = (u + w) % MOD;
                A[k + len] = (u + MOD - w) % MOD;
            }
    int nth = max(1u, thread::hardware_concurrency());
    vector<u64> part(nth, 0);
    vector<thread> ths;
    for (int ti = 0; ti < nth; ++ti)
        ths.emplace_back([&, ti]() {
            u64 acc = 0;
            for (size_t w = ti; w < sz; w += nth)
                acc = (acc + powm(A[w], s)) % MOD;
            part[ti] = acc;
        });
    for (auto& t : ths) t.join();
    u64 tot = 0;
    for (u64 v : part) tot = (tot + v) % MOD;
    return mulm(tot, powm(powm(2, L), MOD - 2));
}

int main() {
    tables(10000000 + 100);
    // distribution self-test (game brute force for n = 12)
    {
        vector<u64> N = grundy_dist(12);
        u64 want[12] = {1026, 1034, 521, 547, 283, 303, 155, 134, 57, 28, 7, 1};
        for (int v = 0; v < 12; ++v)
            if (N[v] != want[v]) {
                fprintf(stderr, "dist mismatch v=%d got %llu want %llu\n", v,
                        N[v], want[v]);
                return 1;
            }
    }
    if (solve(3, 2) != 26) {
        fprintf(stderr, "C(3,2) failed\n");
        return 1;
    }
    if (solve(13, 4) != 540318329ULL) {
        fprintf(stderr, "C(13,4) failed\n");
        return 1;
    }
    printf("%llu\n", solve(10000000LL, 10000000ULL));
    return 0;
}
