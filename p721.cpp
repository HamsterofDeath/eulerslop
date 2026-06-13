#include <cstdint>
#include <cstdlib>
#include <iostream>

namespace {

using i64 = long long;
using u64 = unsigned long long;

constexpr i64 MOD = 999'999'937LL;
constexpr int DEFAULT_N = 5'000'000;

struct LucasState {
    i64 v_n;
    i64 v_next;
    i64 q_n;
};

i64 mod_norm(i64 value) {
    value %= MOD;
    if (value < 0) {
        value += MOD;
    }
    return value;
}

i64 mod_pow(i64 base, u64 exponent) {
    i64 result = 1;
    base %= MOD;
    while (exponent) {
        if (exponent & 1ULL) {
            result = result * base % MOD;
        }
        base = base * base % MOD;
        exponent >>= 1ULL;
    }
    return result;
}

LucasState lucas_pair(i64 p, i64 q, u64 n) {
    if (n == 0) {
        return {2, p % MOD, 1};
    }

    LucasState half = lucas_pair(p, q, n >> 1ULL);
    const i64 q_next = half.q_n * q % MOD;
    const i64 v_even = mod_norm(half.v_n * half.v_n % MOD - 2 * half.q_n % MOD);
    const i64 v_odd = mod_norm(half.v_n * half.v_next % MOD - p * half.q_n % MOD);
    const i64 q_even = half.q_n * half.q_n % MOD;

    if ((n & 1ULL) == 0) {
        return {v_even, v_odd, q_even};
    }

    const i64 v_next_even = mod_norm(half.v_next * half.v_next % MOD - 2 * q_next % MOD);
    return {v_odd, v_next_even, q_even * q % MOD};
}

i64 term(int a) {
    int b = 1;
    while (b * b < a) {
        ++b;
    }

    const u64 exponent = static_cast<u64>(a) * static_cast<u64>(a);
    if (b * b == a) {
        return mod_pow(2LL * b, exponent);
    }

    const i64 p = (2LL * b) % MOD;
    const i64 q = (1LL * b * b - a) % MOD;
    return mod_norm(lucas_pair(p, q, exponent).v_n - 1);
}

i64 solve(int limit) {
    i64 total = 0;
    int b = 1;
    for (int a = 1; a <= limit; ++a) {
        while (b * b < a) {
            ++b;
        }
        const u64 exponent = static_cast<u64>(a) * static_cast<u64>(a);
        if (b * b == a) {
            total += mod_pow(2LL * b, exponent);
        } else {
            const i64 p = (2LL * b) % MOD;
            const i64 q = (1LL * b * b - a) % MOD;
            total += lucas_pair(p, q, exponent).v_n - 1;
        }
        total %= MOD;
        if (total < 0) {
            total += MOD;
        }
    }
    return total;
}

int parse_limit(int argc, char** argv) {
    return argc > 1 ? std::atoi(argv[1]) : DEFAULT_N;
}

}  // namespace

int main(int argc, char** argv) {
    std::cout << solve(parse_limit(argc, argv)) << '\n';
    return 0;
}
