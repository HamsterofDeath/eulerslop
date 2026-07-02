// Project Euler 735: F(1e12), f(n) = #divisors of 2n^2 not exceeding n.
//
// A pair d * e = 2n^2 with gcd factored out canonically:
// w = gcd(d,e), d = w d', e = w e', gcd(d',e') = 1, d'e' = 2m^2 (m = n/w);
// coprimality forces {d', e'} = {2s^2, t^2} (t odd) or {s^2, 2t^2} (s odd)
// with m = st, gcd(s,t) = 1.  The condition d <= n becomes t >= 2s in the
// first case and t >= s in the second.  Hence, bijectively,
//   F(N) = sum_{gcd(s,t)=1, t odd, t>=2s} floor(N/st)
//        + sum_{gcd(s,t)=1, s odd, t>=s}  floor(N/st)
// (validated by brute force up to N = 1000).  Moebius over g = gcd (g odd)
// and floor(N/st) = #{j : st <= N/j} turn each part into
//   sum_{g odd} mu(g) sum_j Ncone(N/(g^2 j)),
// with Ncone(y) counting cone lattice points with st <= y in O(sqrt y).
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <thread>
#include <vector>

using namespace std;
typedef long long i64;
typedef unsigned long long u64;

static i64 isqrt64(i64 x) {
    i64 r = (i64)sqrtl((long double)x);
    while (r * r > x) --r;
    while ((r + 1) * (r + 1) <= x) ++r;
    return r;
}

static inline i64 odds_upto(i64 x) { return x <= 0 ? 0 : (x + 1) / 2; }

// #{(s,t): t odd, t >= 2s, s*t <= y}
static i64 Na(i64 y) {
    i64 c = 0, smax = isqrt64(y / 2);
    for (i64 s = 1; s <= smax; ++s)
        c += odds_upto(y / s) - odds_upto(2 * s - 1);
    return c;
}

// #{(s,t): s odd, t >= s, s*t <= y}
static i64 Nb(i64 y) {
    i64 c = 0, smax = isqrt64(y);
    for (i64 s = 1; s <= smax; s += 2) c += y / s - s + 1;
    return c;
}

// sum_j Na(M/j) + Nb(M/j)
static i64 AB(i64 M) {
    i64 tot = 0;
    for (i64 j = 1; j <= M;) {
        i64 y = M / j, j2 = M / y;
        tot += (j2 - j + 1) * (Na(y) + Nb(y));
        j = j2 + 1;
    }
    return tot;
}

static i64 F(i64 N) {
    i64 gmax = isqrt64(N);
    // mobius sieve
    vector<int8_t> mu(gmax + 1, 1);
    {
        vector<char> comp(gmax + 1, 0);
        vector<int> primes;
        vector<int8_t> m(gmax + 1, 0);
        m[1] = 1;
        for (i64 i = 2; i <= gmax; ++i) {
            if (!comp[i]) { primes.push_back(i); m[i] = -1; }
            for (int p : primes) {
                i64 j = i * p;
                if (j > gmax) break;
                comp[j] = 1;
                if (i % p == 0) { m[j] = 0; break; }
                m[j] = -m[i];
            }
        }
        mu = move(m);
    }
    int nth = max(1u, thread::hardware_concurrency());
    vector<i64> part(nth, 0);
    vector<thread> ths;
    for (int ti = 0; ti < nth; ++ti)
        ths.emplace_back([&, ti]() {
            i64 acc = 0;
            for (i64 g = 1 + 2 * ti; g <= gmax; g += 2 * nth) {
                if (mu[g] == 0) continue;
                acc += (i64)mu[g] * AB(N / (g * g));
            }
            part[ti] = acc;
        });
    for (auto& t : ths) t.join();
    i64 s = 0;
    for (i64 v : part) s += v;
    return s;
}

int main() {
    if (F(15) != 63 || F(1000) != 15066) {
        fprintf(stderr, "self-test failed: %lld %lld\n", F(15), F(1000));
        return 1;
    }
    printf("%lld\n", F(1000000000000LL));
    return 0;
}
