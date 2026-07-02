// Project Euler 747: triangular pizza cuts, Psi(1e8) mod 1e9+7.
//
// All n pieces are triangles iff every pizza corner is either hit by a cut
// or cut off by a pair of colinear cuts (a chord) through the interior
// point P.  With P = (alpha,beta,gamma) in barycentric area coordinates:
//
// * no chord: cuts to all three corners; side piece counts (i,j,k>=1)
//   force P = (i/n, j/n, k/n): C(n-1,2) ways.
// * one chord (at corner C say, cutting off a triangle of area 1/n whose
//   vertices sit at fractions w (on CA) and t=1/(nw) (on CB) from C, with
//   P on the chord: alpha/w + beta/t = 1).  With a,b,c side pieces on
//   AB,BC,CA (a>=1, a+b+c = n-1) elimination gives
//     (c+1) n w^2 - (n+b+c+1) w + (b+1) = 0.
//   For b,c>=1 both roots of this quadratic lie in the valid interval
//   (1/n,1) with all positivity holding, so the count is 2 (1 if disc=0).
//   For b=0 (or c=0) the chord passes through corner B (or A) - a cevian -
//   and every c in 1..n-2 (resp. b) works: 2(n-2) ways per corner.
// * two or three chords: no solutions (verified exactly for n<=16, and
//   the Psi(1000) check below would fail otherwise).
//
// So psi(n) = C(n-1,2) + 6(n-2) + 3*g(n), g(n) = #valid quadratic roots.
// Writing B=b+1, C=c+1 >= 2, D=BC, m=B+C-1, the discriminant condition
// disc > 0 becomes n > n+ = 2D-m+2*sqrt(D(D-m)) (the lower root branch is
// always < s = B+C+... < n), so summing over n<=N:
//   sum g = 2 * sum_{B,C>=2} max(0, N - floor(n+))  +  #{n+ integer <= N}.
// Verified: psi(3)=7, psi(6)=34, psi(10)=90, Psi(10)=345,
// Psi(1000)=172166601.
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <thread>
#include <vector>

using namespace std;
typedef unsigned long long u64;
typedef long long i64;

static const u64 MOD = 1000000007ULL;

static u64 isqrt64(u64 x) {
    u64 r = (u64)sqrtl((long double)x);
    while (r * r > x) --r;
    while ((r + 1) * (r + 1) <= x) ++r;
    return r;
}

// sum over n<=N of g(n), exact (fits u64 for N<=1e8)
static u64 sum_g(u64 N) {
    int nth = max(1u, thread::hardware_concurrency());
    vector<u64> part(nth, 0);
    vector<thread> ths;
    for (int ti = 0; ti < nth; ++ti)
        ths.emplace_back([&, ti]() {
            u64 acc = 0;
            for (u64 B = 2 + ti;; B += nth) {
                bool any = false;
                for (u64 C = 2;; ++C) {
                    u64 D = B * C, m = B + C - 1;
                    u64 E = D * (D - m);
                    u64 r = isqrt64(4 * E);
                    u64 nf = 2 * D - m + r;
                    if (nf >= N) break;
                    any = true;
                    acc += 2 * (N - nf);
                    if (r * r == 4 * E) acc += 1;
                }
                if (!any && 2 * (2 * B) - (B + 1) > N) break;
            }
            part[ti] = acc;
        });
    for (auto& t : ths) t.join();
    u64 s = 0;
    for (u64 v : part) s += v;
    return s;
}

static u64 g_direct(u64 n) {
    u64 cnt = 0;
    for (u64 b = 1; b + 1 <= n - 2; ++b)
        for (u64 c = 1; b + c <= n - 2; ++c) {
            i64 disc = (i64)((n + b + c + 1) * (n + b + c + 1)) -
                       (i64)(4 * (b + 1) * (c + 1) * n);
            if (disc > 0) cnt += 2;
            else if (disc == 0) cnt += 1;
        }
    return cnt;
}

static u64 psi_direct(u64 n) {
    return (n - 1) * (n - 2) / 2 + 6 * (n - 2) + 3 * g_direct(n);
}

int main() {
    if (psi_direct(3) != 7 || psi_direct(6) != 34 || psi_direct(10) != 90) {
        fprintf(stderr, "psi self-test failed\n");
        return 1;
    }
    u64 s10 = 0;
    for (u64 n = 3; n <= 10; ++n) s10 += psi_direct(n);
    u64 s1000 = 0;
    for (u64 n = 3; n <= 1000; ++n) s1000 += psi_direct(n);
    if (s10 != 345 || s1000 != 172166601ULL) {
        fprintf(stderr, "Psi self-test failed: %llu %llu\n", s10, s1000);
        return 1;
    }
    if (sum_g(1000) != (s1000 - (1000ULL * 999 * 998 / 6) - 3ULL * 999 * 998) / 3) {
        fprintf(stderr, "sum_g mismatch at 1000\n");
        return 1;
    }
    const u64 N = 100000000ULL;
    // Psi(N) = C(N,3) + 3(N-1)(N-2) + 3*sum_g(N)  (mod p)
    u64 c3 = (u64)((__uint128_t)N % MOD * ((N - 1) % MOD) % MOD * ((N - 2) % MOD) % MOD);
    c3 = (u64)((__uint128_t)c3 * 166666668ULL % MOD);  // /6 mod p
    u64 cev = (__uint128_t)3 * ((N - 1) % MOD) % MOD * ((N - 2) % MOD) % MOD;
    u64 sg = sum_g(N) % MOD;
    u64 ans = (c3 + cev + 3 * sg) % MOD;
    printf("%llu\n", ans);
    return 0;
}
