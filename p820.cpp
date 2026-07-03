// Project Euler 820: d_n(1/k)=floor(10 * (10^(n-1) mod k) / k).
#include <cstdint>
#include <cstdio>

using namespace std;

static uint64_t pow_mod(uint64_t base, uint64_t exp, uint64_t mod) {
    if (mod == 1) return 0;
    uint64_t result = 1 % mod;
    base %= mod;
    while (exp) {
        if (exp & 1) result = (__uint128_t)result * base % mod;
        base = (__uint128_t)base * base % mod;
        exp >>= 1;
    }
    return result;
}

static uint64_t s_value(uint64_t n) {
    uint64_t total = 0;
    for (uint64_t k = 1; k <= n; ++k) {
        uint64_t r = pow_mod(10, n - 1, k);
        total += (10 * r) / k;
    }
    return total;
}

int main() {
    if (s_value(7) != 10 || s_value(100) != 418) {
        fprintf(stderr, "self-test failed\n");
        return 1;
    }
    printf("%llu\n", (unsigned long long)s_value(10000000));
    return 0;
}
