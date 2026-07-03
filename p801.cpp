// Project Euler 801: for prime p, the nonzero residue/exponent pairs reduce
// to counting 2x2 matrices over Z/(p-1)Z with determinant exactly zero.
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <vector>

using namespace std;

static const uint64_t MOD = 993353399ULL;

static uint64_t pow_mod(uint64_t a, uint64_t e, uint64_t mod) {
    uint64_t r = 1 % mod;
    a %= mod;
    while (e) {
        if (e & 1) r = (uint64_t)((__uint128_t)r * a % mod);
        a = (uint64_t)((__uint128_t)a * a % mod);
        e >>= 1;
    }
    return r;
}

static vector<uint32_t> primes_to(uint32_t limit) {
    vector<uint32_t> primes;
    if (limit < 2) return primes;
    if (limit >= 2) primes.push_back(2);
    uint32_t n = (limit - 1) / 2;
    vector<bool> composite(n + 1, false);
    for (uint32_t i = 1; 2 * i + 1 <= limit; ++i) {
        if (composite[i]) continue;
        uint32_t p = 2 * i + 1;
        primes.push_back(p);
        if ((uint64_t)p * p > limit) continue;
        for (uint64_t j = ((uint64_t)p * p - 1) / 2; j <= n; j += p)
            composite[(size_t)j] = true;
    }
    return primes;
}

static uint64_t zero_det_prime_power(uint64_t q, int e) {
    // q^(2e-1) * ((q+1)q^e - 1), reduced modulo MOD.
    uint64_t left = pow_mod(q, 2ULL * e - 1, MOD);
    uint64_t qe = pow_mod(q, e, MOD);
    uint64_t right = (((q + 1) % MOD) * qe) % MOD;
    right = (right + MOD - 1) % MOD;
    return (uint64_t)((__uint128_t)left * right % MOD);
}

static uint64_t range_sum(uint64_t lo, uint64_t hi) {
    uint64_t root = (uint64_t)sqrt((long double)hi) + 2;
    while (root * root > hi) --root;
    while ((root + 1) * (root + 1) <= hi) ++root;
    vector<uint32_t> primes = primes_to((uint32_t)root);

    size_t len = (size_t)(hi - lo + 1);
    vector<bool> composite(len, false);
    for (uint32_t p : primes) {
        uint64_t pp = (uint64_t)p * p;
        uint64_t start = pp >= lo ? pp : ((lo + p - 1) / p) * (uint64_t)p;
        for (uint64_t x = start; x <= hi; x += p) composite[(size_t)(x - lo)] = true;
    }
    if (lo == 0) {
        if (len > 0) composite[0] = true;
        if (len > 1) composite[1] = true;
    } else if (lo == 1) {
        composite[0] = true;
    }

    vector<uint64_t> rem(len), zmod(len, 1);
    for (size_t i = 0; i < len; ++i) rem[i] = lo + i - 1;

    for (uint32_t q : primes) {
        uint64_t r = (lo <= 1) ? 0 : (q - ((lo - 1) % q)) % q;
        for (uint64_t i = r; i < len; i += q) {
            int e = 0;
            while (rem[(size_t)i] != 0 && rem[(size_t)i] % q == 0) {
                rem[(size_t)i] /= q;
                ++e;
            }
            if (e) {
                zmod[(size_t)i] = (uint64_t)((__uint128_t)zmod[(size_t)i] *
                                             zero_det_prime_power(q, e) % MOD);
            }
        }
    }

    uint64_t total = 0;
    for (size_t i = 0; i < len; ++i) {
        uint64_t p = lo + i;
        if (composite[i]) continue;
        if (rem[i] > 1) {
            zmod[i] = (uint64_t)((__uint128_t)zmod[i] *
                                 zero_det_prime_power(rem[i], 1) % MOD);
        }
        uint64_t n = (p - 1) % MOD;
        uint64_t fp = ((uint64_t)((__uint128_t)n * n % MOD) + zmod[i]) % MOD;
        total += fp;
        if (total >= MOD) total -= MOD;
    }
    return total;
}

static uint64_t f_prime(uint64_t p) {
    return range_sum(p, p);
}

int main() {
    if (f_prime(5) != 104 || f_prime(97) != 1614336) {
        fprintf(stderr, "f(p) self-test failed: %llu %llu\n",
                (unsigned long long)f_prime(5),
                (unsigned long long)f_prime(97));
        return 1;
    }
    if (range_sum(1, 100) != 7381000ULL) {
        fprintf(stderr, "S(1,100) self-test failed\n");
        return 1;
    }
    if (range_sum(1, 100000) != 701331986ULL) {
        fprintf(stderr, "S(1,100000) self-test failed\n");
        return 1;
    }

    printf("%llu\n",
           (unsigned long long)range_sum(10000000000000000ULL,
                                         10000000001000000ULL));
    return 0;
}
