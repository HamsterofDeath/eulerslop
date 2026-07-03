// Project Euler 837: count words with fixed adjacent-transposition counts and
// identity product.  The standard S3 representation gives the coefficient of
// (x^2 - xy + y^2)^((m+n)/2).
#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <vector>

using namespace std;

static const uint32_t MOD = 1234567891U;

static uint64_t mod_pow(uint64_t a, uint64_t e) {
    uint64_t r = 1;
    while (e) {
        if (e & 1) r = r * a % MOD;
        a = a * a % MOD;
        e >>= 1;
    }
    return r;
}

static vector<uint32_t> inverses(uint32_t limit) {
    vector<uint32_t> inv(limit + 1);
    inv[1] = 1;
    for (uint32_t i = 2; i <= limit; ++i)
        inv[i] = (uint64_t)(MOD - MOD / i) * inv[MOD % i] % MOD;
    return inv;
}

static uint32_t amidakuji(uint32_t m, uint32_t n) {
    uint64_t length = (uint64_t)m + n;
    if (length & 1) return 0;
    uint32_t h = (uint32_t)(length / 2);
    uint32_t small = min(m, n);
    vector<uint32_t> inv = inverses(small + 2);

    uint64_t binom = 1;
    for (uint32_t i = 1; i <= m; ++i)
        binom = binom * ((uint64_t)(length - m + i) % MOD) % MOD * inv[i] % MOD;

    uint32_t b = m & 1U;
    uint32_t a = (m - b) / 2;
    uint32_t c = (n - b) / 2;

    uint64_t term = 1;
    for (uint32_t i = 1; i <= a; ++i)
        term = term * (uint64_t)(h - a + i) % MOD * inv[i] % MOD;
    if (b == 1) term = term * (c + 1ULL) % MOD;
    if (b & 1U) term = (MOD - term) % MOD;

    uint64_t coeff = 0;
    while (b <= small) {
        coeff += term;
        coeff %= MOD;
        if (b + 2 > small) break;
        term = term * a % MOD * c % MOD * inv[b + 1] % MOD * inv[b + 2] % MOD;
        --a;
        --c;
        b += 2;
    }

    return (uint32_t)((binom + 2 * coeff) % MOD * mod_pow(3, MOD - 2) % MOD);
}

int main() {
    if (amidakuji(3, 3) != 2 || amidakuji(123, 321) != 172633303U) {
        fprintf(stderr, "self-test failed\n");
        return 1;
    }
    printf("%u\n", amidakuji(123456789U, 987654321U));
    return 0;
}
