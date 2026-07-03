// Project Euler 850: for odd k, residues i^k and (n-i)^k pair to 1 unless
// n | i^k, hence f_k(n)=(n-z_k(n))/2.  The summatory z_k is multiplicative:
// z_k(n)=n/prod_p p^ceil(v_p(n)/k).  Since z_k(p)=1, write z_k = 1 * g_k;
// g_k is supported on powerful numbers, which are sparse enough up to N.
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <iostream>
#include <numeric>
#include <vector>

using namespace std;

static const uint64_t ANSWER_MOD = 977676779ULL;
static const uint64_t WORK_MOD = 2 * ANSWER_MOD;

static uint64_t N;
static vector<uint32_t> primes;
static vector<int> classes;          // odd k values; 0 means k > max exponent.
static vector<uint64_t> class_count; // normally 1, except the final infinity class.
static uint64_t z_sum_mod;

static uint64_t pow_mod_u64(uint64_t a, int e) {
    uint64_t r = 1 % WORK_MOD;
    a %= WORK_MOD;
    while (e) {
        if (e & 1) r = (__uint128_t)r * a % WORK_MOD;
        a = (__uint128_t)a * a % WORK_MOD;
        e >>= 1;
    }
    return r;
}

static uint64_t h_prime_power(uint64_t p, int exponent, int k) {
    if (exponent == 0) return 1;
    int removed = (k == 0) ? 1 : (exponent + k - 1) / k;
    return pow_mod_u64(p, exponent - removed);
}

static vector<uint64_t> delta_values(uint64_t p, int exponent) {
    vector<uint64_t> out(classes.size());
    for (size_t i = 0; i < classes.size(); ++i) {
        uint64_t hi = h_prime_power(p, exponent, classes[i]);
        uint64_t lo = h_prime_power(p, exponent - 1, classes[i]);
        out[i] = (hi + WORK_MOD - lo) % WORK_MOD;
    }
    return out;
}

static void add_contribution(uint64_t value, const vector<uint64_t>& g_values) {
    uint64_t weighted = 0;
    for (size_t i = 0; i < g_values.size(); ++i) {
        weighted = (weighted + (__uint128_t)(class_count[i] % WORK_MOD) * g_values[i]) %
                   WORK_MOD;
    }
    z_sum_mod = (z_sum_mod + (__uint128_t)(N / value % WORK_MOD) * weighted) % WORK_MOD;
}

static void dfs_powerful(size_t start, uint64_t value, const vector<uint64_t>& g_values) {
    add_contribution(value, g_values);
    for (size_t i = start; i < primes.size(); ++i) {
        uint64_t p = primes[i];
        if (p > N / value / p) break;
        uint64_t next = value * p * p;
        int exponent = 2;
        while (next <= N) {
            vector<uint64_t> delta = delta_values(p, exponent);
            vector<uint64_t> ng(g_values.size());
            for (size_t j = 0; j < ng.size(); ++j)
                ng[j] = (__uint128_t)g_values[j] * delta[j] % WORK_MOD;
            dfs_powerful(i + 1, next, ng);
            if (next > N / p) break;
            next *= p;
            ++exponent;
        }
    }
}

static vector<uint32_t> primes_to(uint64_t limit) {
    vector<bool> composite(limit + 1, false);
    vector<uint32_t> ps;
    for (uint64_t i = 2; i <= limit; ++i) {
        if (!composite[i]) {
            ps.push_back((uint32_t)i);
            if (i * i <= limit)
                for (uint64_t j = i * i; j <= limit; j += i) composite[j] = true;
        }
    }
    return ps;
}

static uint64_t floor_s_mod(uint64_t limit) {
    N = limit;
    int max_exp = 0;
    for (uint64_t x = limit; x; x >>= 1) ++max_exp;
    --max_exp;

    uint64_t odd_count = (limit + 1) / 2;
    classes.clear();
    class_count.clear();
    for (int k = 1; k <= max_exp && (uint64_t)k <= limit; k += 2) {
        classes.push_back(k);
        class_count.push_back(1);
    }
    uint64_t used = class_count.size();
    if (odd_count > used) {
        classes.push_back(0);
        class_count.push_back(odd_count - used);
    }

    uint64_t root = sqrt((long double)limit) + 2;
    while (root > limit / root) --root;
    while ((root + 1) <= limit / (root + 1)) ++root;
    primes = primes_to(root);

    z_sum_mod = 0;
    vector<uint64_t> ones(classes.size(), 1);
    dfs_powerful(0, 1, ones);

    uint64_t triangular = (__uint128_t)(limit % WORK_MOD) * ((limit + 1) % WORK_MOD) %
                          WORK_MOD;
    if (triangular & 1)
        triangular = (triangular + WORK_MOD) / 2;
    else
        triangular /= 2;
    uint64_t raw = ((__uint128_t)(odd_count % WORK_MOD) * triangular + WORK_MOD -
                    z_sum_mod) %
                   WORK_MOD;
    return raw / 2;
}

int main() {
    if (floor_s_mod(10) != 100 || floor_s_mod(1000) != 123687804ULL) {
        fprintf(stderr, "self-test failed\n");
        return 1;
    }
    printf("%llu\n", (unsigned long long)floor_s_mod(33557799775533ULL));
    return 0;
}
