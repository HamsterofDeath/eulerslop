// Project Euler 804: 4(x^2+xy+41y^2)=(2x+y)^2+163y^2.
#include <cmath>
#include <cstdint>
#include <cstdio>

using namespace std;

static uint64_t isqrt_u64(uint64_t n) {
    uint64_t r = (uint64_t)sqrt((long double)n);
    while ((r + 1) <= n / (r + 1)) ++r;
    while (r > n / r) --r;
    return r;
}

static uint64_t parity_count(uint64_t m, int parity) {
    uint64_t total = 2 * m + 1;
    uint64_t evens = 2 * (m / 2) + 1;
    return parity == 0 ? evens : total - evens;
}

static uint64_t t_value(uint64_t n) {
    uint64_t limit = 4 * n;
    uint64_t ymax = isqrt_u64(limit / 163);
    uint64_t total = parity_count(isqrt_u64(limit), 0);
    for (uint64_t y = 1; y <= ymax; ++y) {
        uint64_t remaining = limit - 163 * y * y;
        uint64_t m = isqrt_u64(remaining);
        total += 2 * parity_count(m, (int)(y & 1));
    }
    return total - 1;  // remove (x,y)=(0,0), which represents n=0.
}

int main() {
    if (t_value(1000) != 474 || t_value(1000000) != 492128 ||
        t_value(53) - t_value(52) != 4) {
        fprintf(stderr, "self-test failed\n");
        return 1;
    }
    printf("%llu\n", (unsigned long long)t_value(10000000000000000ULL));
    return 0;
}
