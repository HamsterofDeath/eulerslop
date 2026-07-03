// Project Euler 810: XOR multiplication is polynomial multiplication over F_2,
// so XOR-primes are the monic irreducible binary polynomials.
#include <cstdint>
#include <cstdio>
#include <vector>

using namespace std;

static inline int degree(uint64_t p) {
    return 63 - __builtin_clzll(p);
}

static uint64_t mod_reduce(uint64_t value, uint64_t mod_poly, int d) {
    while (degree(value) >= d) {
        value ^= mod_poly << (degree(value) - d);
    }
    return value;
}

static uint64_t square_mod(uint64_t value, uint64_t mod_poly, int d) {
    uint64_t square = 0;
    for (int i = 0; i < d; ++i) {
        if ((value >> i) & 1ULL) square |= 1ULL << (2 * i);
    }
    return mod_reduce(square, mod_poly, d);
}

static uint64_t gcd_poly(uint64_t a, uint64_t b) {
    while (b) {
        while (degree(a) >= degree(b)) a ^= b << (degree(a) - degree(b));
        uint64_t r = a;
        a = b;
        b = r;
    }
    return a;
}

static bool irreducible(uint64_t poly) {
    int d = degree(poly);
    if (d == 1) return true;
    if ((poly & 1ULL) == 0) return false;
    if ((__builtin_popcountll(poly) & 1) == 0) return false;  // divisible by x+1

    vector<int> checks;
    int tmp = d;
    for (int p = 2; p * p <= tmp; ++p) {
        if (tmp % p) continue;
        checks.push_back(d / p);
        while (tmp % p == 0) tmp /= p;
    }
    if (tmp > 1) checks.push_back(d / tmp);

    uint64_t x = 2;
    uint64_t h = x;
    for (int k = 1; k <= d; ++k) {
        h = square_mod(h, poly, d);
        for (int check : checks) {
            if (k != check) continue;
            if (gcd_poly(h ^ x, poly) != 1) return false;
        }
    }
    return h == x;
}

static int mobius(int n) {
    int result = 1;
    for (int p = 2; p * p <= n; ++p) {
        if (n % p) continue;
        n /= p;
        result = -result;
        if (n % p == 0) return 0;
        while (n % p == 0) n /= p;
    }
    if (n > 1) result = -result;
    return result;
}

static uint64_t irreducibles_of_degree(int d) {
    int64_t total = 0;
    for (int k = 1; k <= d; ++k) {
        if (d % k == 0) total += (int64_t)mobius(k) * (1ULL << (d / k));
    }
    return (uint64_t)(total / d);
}

static uint64_t nth_xor_prime(uint64_t target) {
    uint64_t below = 0;
    int d = 0;
    while (below < target) {
        ++d;
        uint64_t count = irreducibles_of_degree(d);
        if (below + count >= target) break;
        below += count;
    }

    uint64_t need = target - below;
    uint64_t start = 1ULL << d;
    uint64_t end = 1ULL << (d + 1);
    for (uint64_t poly = start | 1ULL; poly < end; poly += 2) {
        if (irreducible(poly) && --need == 0) return poly;
    }
    return 0;
}

int main() {
    if (nth_xor_prime(10) != 41) {
        fprintf(stderr, "self-test failed\n");
        return 1;
    }
    printf("%llu\n", (unsigned long long)nth_xor_prime(5000000));
    return 0;
}
