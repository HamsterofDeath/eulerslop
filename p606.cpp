#include <cmath>
#include <cstdint>
#include <iostream>
#include <vector>

using int64 = long long;

static constexpr int64 X = 1000000000000LL;
static constexpr int64 MOD = 1000000000LL;

// The ordered-factorization count for an exponent multiset is 252 only for
// (3, 3), so S(10^36) is sum (p*q)^3 over distinct primes p < q, p*q <= 10^12.
// The weighted Legendre sieve below computes sum prime^3 <= v for every
// required quotient v = floor(X / i), modulo 10^9.

static int64 cube_mod(int64 x) {
    int64 a = x % MOD;
    return static_cast<int64>((__int128)a * a % MOD * a % MOD);
}

static int64 sum_cubes_to(int64 n) {
    int64 a = n;
    int64 b = n + 1;
    if (a & 1LL) {
        b /= 2;
    } else {
        a /= 2;
    }
    int64 t = static_cast<int64>((__int128)(a % MOD) * (b % MOD) % MOD);
    return static_cast<int64>((__int128)t * t % MOD);
}

int main() {
    const int64 root = static_cast<int64>(std::sqrt(static_cast<long double>(X)));

    std::vector<int64> values;
    values.reserve(2 * root);
    for (int64 l = 1; l <= X;) {
        int64 v = X / l;
        values.push_back(v);
        l = X / v + 1;
    }

    const int64 size = static_cast<int64>(values.size());
    auto index_of = [&](int64 v) -> int64 {
        return v <= root ? size - v : X / v - 1;
    };

    std::vector<int64> prime_cube_sum;
    prime_cube_sum.reserve(values.size());
    for (int64 v : values) {
        prime_cube_sum.push_back((sum_cubes_to(v) - 1 + MOD) % MOD);
    }

    std::vector<int> primes;
    for (int64 p = 2; p <= root; ++p) {
        if (prime_cube_sum[index_of(p)] == prime_cube_sum[index_of(p - 1)]) {
            continue;
        }

        primes.push_back(static_cast<int>(p));
        const int64 before_p = prime_cube_sum[index_of(p - 1)];
        const int64 p_cube = cube_mod(p);
        const int64 p_square = p * p;

        for (int64 j = 0; j < size && values[j] >= p_square; ++j) {
            int64 reduced = values[j] / p;
            int64 diff = prime_cube_sum[index_of(reduced)] - before_p;
            diff %= MOD;
            if (diff < 0) {
                diff += MOD;
            }
            prime_cube_sum[j] -= static_cast<int64>((__int128)p_cube * diff % MOD);
            prime_cube_sum[j] %= MOD;
            if (prime_cube_sum[j] < 0) {
                prime_cube_sum[j] += MOD;
            }
        }
    }

    std::vector<int64> prefix(root + 1, 0);
    std::size_t next_prime = 0;
    int64 running = 0;
    for (int64 n = 1; n <= root; ++n) {
        if (next_prime < primes.size() && primes[next_prime] == n) {
            running += cube_mod(n);
            running %= MOD;
            ++next_prime;
        }
        prefix[n] = running;
    }

    int64 answer = 0;
    for (int p : primes) {
        int64 limit = X / p;
        int64 larger_prime_sum = prime_cube_sum[index_of(limit)] - prefix[p];
        larger_prime_sum %= MOD;
        if (larger_prime_sum < 0) {
            larger_prime_sum += MOD;
        }
        answer += static_cast<int64>((__int128)cube_mod(p) * larger_prime_sum % MOD);
        answer %= MOD;
    }

    std::cout << answer << '\n';
    return 0;
}
