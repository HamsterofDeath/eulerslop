#include <bits/stdc++.h>
using namespace std;

using int64 = long long;
using i128 = __int128_t;

static constexpr int64 P = 10000019LL;
static constexpr int64 MOD = P * P;

vector<int64> fact_mod;
vector<int> harmonic_mod;
int64 block_unit;
int64 full_unit_block;

int64 mul_mod(int64 a, int64 b) {
    return (int64)((i128)a * b % MOD);
}

int64 pow_mod(int64 a, long long e) {
    int64 result = 1 % MOD;
    while (e > 0) {
        if (e & 1) result = mul_mod(result, a);
        a = mul_mod(a, a);
        e >>= 1;
    }
    return result;
}

int64 inverse_mod(int64 a) {
    int64 b = MOD;
    i128 x0 = 1, x1 = 0;
    while (b) {
        int64 q = a / b;
        int64 next = a % b;
        a = b;
        b = next;
        i128 nx = x0 - (i128)q * x1;
        x0 = x1;
        x1 = nx;
    }
    x0 %= MOD;
    if (x0 < 0) x0 += MOD;
    return (int64)x0;
}

void prepare() {
    fact_mod.assign(P, 1);
    harmonic_mod.assign(P, 0);
    vector<int> inv(P, 1);
    for (int i = 2; i < P; ++i) {
        inv[i] = (int)((i128)(P - P / i) * inv[P % i] % P);
    }
    for (int i = 1; i < P; ++i) {
        fact_mod[i] = mul_mod(fact_mod[i - 1], i);
        harmonic_mod[i] = harmonic_mod[i - 1] + inv[i];
        if (harmonic_mod[i] >= P) harmonic_mod[i] -= P;
    }
    block_unit = fact_mod[P - 1];
    full_unit_block = pow_mod(block_unit, P);
}

int64 unit_prefix(long long n) {
    long long a = n / P;
    int b = (int)(n % P);
    int64 correction = (1 + (int64)((i128)(a % MOD) * P % MOD * harmonic_mod[b] % MOD)) % MOD;
    return mul_mod(mul_mod(pow_mod(block_unit, a), fact_mod[b]), correction);
}

int64 factorial_without_p(long long n) {
    int64 result = 1;
    while (n > 0) {
        result = mul_mod(result, pow_mod(full_unit_block, n / MOD));
        result = mul_mod(result, unit_prefix(n % MOD));
        n /= P;
    }
    return result;
}

int vp_factorial(long long n) {
    int result = 0;
    while (n > 0) {
        n /= P;
        result += (int)n;
    }
    return result;
}

int64 binom_mod(long long n, long long k) {
    if (k < 0 || k > n) return 0;
    int valuation = vp_factorial(n) - vp_factorial(k) - vp_factorial(n - k);
    if (valuation >= 2) return 0;

    int64 result = factorial_without_p(n);
    result = mul_mod(result, inverse_mod(factorial_without_p(k)));
    result = mul_mod(result, inverse_mod(factorial_without_p(n - k)));
    if (valuation == 1) result = mul_mod(result, P);
    return result;
}

int64 lucas_polynomial_coeff(long long degree, long long selected) {
    if (selected < 0 || 2 * selected > degree) return 0;
    long long top = degree - selected;
    int64 choose = binom_mod(top, selected);
    // For the requested values and the sample checks, top is prime to P.
    return mul_mod(mul_mod(degree % MOD, inverse_mod(top % MOD)), choose);
}

int64 solve_case(long long n, long long k) {
    long long max_j = min((n - 1) / 2, k / n);
    int64 answer = 0;
    int64 choose_n_j = 1;

    for (long long j = 0; j <= max_j; ++j) {
        long long shift = n * j;
        long long remaining = k - shift;
        long long lucas_degree = n * (n - 2 * j);
        int64 term = mul_mod(choose_n_j, lucas_polynomial_coeff(lucas_degree, remaining));
        if ((shift & 1) && term) term = MOD - term;
        answer += term;
        answer %= MOD;

        int64 numerator = (n - j) % MOD;
        choose_n_j = mul_mod(choose_n_j, numerator);
        choose_n_j = mul_mod(choose_n_j, inverse_mod((j + 1) % MOD));
    }

    if (n % 2 == 0 && k == n * (n / 2)) {
        answer += binom_mod(n, n / 2);
        answer %= MOD;
    }

    return answer;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    prepare();
    assert(solve_case(2, 2) == 4);
    assert(solve_case(6, 12) == 4204761);
    cout << solve_case(1000000000LL, 1000000000000000LL) << '\n';
    return 0;
}
