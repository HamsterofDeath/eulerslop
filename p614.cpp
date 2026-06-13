#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>

using namespace std;

static constexpr int TARGET_MOD = 1000000007;
static constexpr int LIMIT = 10000000;

template <int MOD>
static int mod_pow(long long base, long long exponent) {
    long long result = 1;
    while (exponent > 0) {
        if (exponent & 1LL) result = result * base % MOD;
        base = base * base % MOD;
        exponent >>= 1LL;
    }
    return (int)result;
}

template <int MOD, int ROOT>
static void ntt(vector<int>& a, bool inverse) {
    const int n = (int)a.size();

    for (int i = 1, j = 0; i < n; ++i) {
        int bit = n >> 1;
        for (; j & bit; bit >>= 1) j ^= bit;
        j ^= bit;
        if (i < j) swap(a[i], a[j]);
    }

    for (int len = 2; len <= n; len <<= 1) {
        int step = mod_pow<MOD>(ROOT, (MOD - 1) / len);
        if (inverse) step = mod_pow<MOD>(step, MOD - 2);
        const int half = len >> 1;

        for (int start = 0; start < n; start += len) {
            long long w = 1;
            for (int i = 0; i < half; ++i) {
                int u = a[start + i];
                int v = (int)(w * a[start + i + half] % MOD);
                int x = u + v;
                if (x >= MOD) x -= MOD;
                int y = u - v;
                if (y < 0) y += MOD;
                a[start + i] = x;
                a[start + i + half] = y;
                w = w * step % MOD;
            }
        }
    }

    if (inverse) {
        int inv_n = mod_pow<MOD>(n, MOD - 2);
        for (int& x : a) x = (int)((long long)x * inv_n % MOD);
    }
}

template <int MOD, int ROOT>
static vector<int> convolution_prime(const vector<int>& a, const vector<int>& b, int need) {
    int a_size = min((int)a.size(), need);
    int b_size = min((int)b.size(), need);
    int result_size = min(need, a_size + b_size - 1);

    int n = 1;
    while (n < a_size + b_size - 1) n <<= 1;

    vector<int> fa(n), fb(n);
    for (int i = 0; i < a_size; ++i) fa[i] = a[i] % MOD;
    for (int i = 0; i < b_size; ++i) fb[i] = b[i] % MOD;

    ntt<MOD, ROOT>(fa, false);
    ntt<MOD, ROOT>(fb, false);
    for (int i = 0; i < n; ++i) fa[i] = (int)((long long)fa[i] * fb[i] % MOD);
    ntt<MOD, ROOT>(fa, true);

    fa.resize(result_size);
    return fa;
}

static vector<int> convolution_mod(const vector<int>& a, const vector<int>& b, int need) {
    static constexpr int P1 = 998244353;
    static constexpr int P2 = 469762049;
    static constexpr int P3 = 167772161;
    static constexpr int ROOT = 3;

    if (a.empty() || b.empty() || need <= 0) return {};

    vector<int> r1 = convolution_prime<P1, ROOT>(a, b, need);
    vector<int> r2 = convolution_prime<P2, ROOT>(a, b, need);
    vector<int> r3 = convolution_prime<P3, ROOT>(a, b, need);

    const int result_size = (int)r1.size();
    vector<int> result(result_size);

    const long long inv_p1_mod_p2 = mod_pow<P2>(P1 % P2, P2 - 2);
    const long long p1_mod_p3 = P1 % P3;
    const long long p1_mod_target = P1 % TARGET_MOD;
    const long long p12_mod_p3 = (long long)(P1 % P3) * (P2 % P3) % P3;
    const long long p12_mod_target = (long long)(P1 % TARGET_MOD) * (P2 % TARGET_MOD) % TARGET_MOD;
    const long long inv_p12_mod_p3 = mod_pow<P3>(p12_mod_p3, P3 - 2);

    for (int i = 0; i < result_size; ++i) {
        long long t2 = (r2[i] - r1[i]) % P2;
        if (t2 < 0) t2 += P2;
        t2 = t2 * inv_p1_mod_p2 % P2;

        long long x12_mod_p3 = (r1[i] + p1_mod_p3 * t2) % P3;
        long long x12_mod_target = (r1[i] + p1_mod_target * t2) % TARGET_MOD;

        long long t3 = (r3[i] - x12_mod_p3) % P3;
        if (t3 < 0) t3 += P3;
        t3 = t3 * inv_p12_mod_p3 % P3;

        result[i] = (int)((x12_mod_target + p12_mod_target * t3) % TARGET_MOD);
    }

    return result;
}

static vector<int> inverse_series(const vector<int>& f, int need) {
    vector<int> inverse(1, mod_pow<TARGET_MOD>(f[0], TARGET_MOD - 2));

    while ((int)inverse.size() < need) {
        int next_size = min(2 * (int)inverse.size(), need);
        vector<int> prefix(f.begin(), f.begin() + next_size);
        vector<int> correction = convolution_mod(prefix, inverse, next_size);
        correction.resize(next_size);

        correction[0] = (2 - correction[0]) % TARGET_MOD;
        if (correction[0] < 0) correction[0] += TARGET_MOD;
        for (int i = 1; i < next_size; ++i) {
            if (correction[i] != 0) correction[i] = TARGET_MOD - correction[i];
        }

        inverse = convolution_mod(inverse, correction, next_size);
        inverse.resize(next_size);
    }

    return inverse;
}

static vector<int> theta4_series(int degree) {
    vector<int> theta(degree + 1);
    theta[0] = 1;
    for (long long k = 1; k * k <= degree; ++k) {
        theta[(int)(k * k)] = (k & 1LL) ? TARGET_MOD - 2 : 2;
    }
    return theta;
}

static int special_partition_value(int n, const vector<int>& overpartitions) {
    long long total = 0;
    for (long long r = 0;; ++r) {
        long long triangular = r * (r + 1) / 2;
        if (triangular > n) break;
        if (((n - triangular) & 3LL) == 0) {
            total += overpartitions[(int)((n - triangular) / 4)];
        }
    }
    return (int)(total % TARGET_MOD);
}

static int solve() {
    const int max_overpartition_index = LIMIT / 4;

    // The special-partition generating function is
    //   psi(q) / theta_4(q^4),
    // where psi(q)=sum q^(r(r+1)/2).  Thus the q^4 component is the inverse
    // of theta_4(x)=1+2*sum_{k>=1}(-1)^k x^(k^2).
    vector<int> overpartitions = inverse_series(
        theta4_series(max_overpartition_index),
        max_overpartition_index + 1
    );

    assert(special_partition_value(1, overpartitions) == 1);
    assert(special_partition_value(2, overpartitions) == 0);
    assert(special_partition_value(3, overpartitions) == 1);
    assert(special_partition_value(6, overpartitions) == 1);
    assert(special_partition_value(10, overpartitions) == 3);
    assert(special_partition_value(100, overpartitions) == 37076);
    assert(
        special_partition_value(1000, overpartitions)
        == (int)(3699177285485660336ULL % TARGET_MOD)
    );

    for (int i = 1; i <= max_overpartition_index; ++i) {
        overpartitions[i] += overpartitions[i - 1];
        if (overpartitions[i] >= TARGET_MOD) overpartitions[i] -= TARGET_MOD;
    }

    long long total = 0;
    for (long long r = 0;; ++r) {
        long long triangular = r * (r + 1) / 2;
        if (triangular > LIMIT) break;
        total += overpartitions[(int)((LIMIT - triangular) / 4)];
        total %= TARGET_MOD;
    }

    // Remove the empty partition contribution at n=0; the problem starts at 1.
    return (int)((total + TARGET_MOD - 1) % TARGET_MOD);
}

int main() {
    cout << solve() << '\n';
    return 0;
}
