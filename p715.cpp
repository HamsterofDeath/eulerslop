#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <unordered_map>

namespace {

using i64 = long long;

constexpr i64 MOD = 1'000'000'007LL;
constexpr i64 DEFAULT_N = 1'000'000'000'000LL;

struct SplitMixHash {
    static std::uint64_t splitmix64(std::uint64_t x) {
        x += 0x9e3779b97f4a7c15ULL;
        x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
        x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
        return x ^ (x >> 31);
    }

    std::size_t operator()(std::uint64_t x) const {
        return static_cast<std::size_t>(splitmix64(x));
    }
};

std::unordered_map<i64, int, SplitMixHash> memo;

int character_prefix(i64 n) {
    const int r = static_cast<int>(n & 3LL);
    return (r == 1 || r == 2) ? 1 : 0;
}

int summatory_inverse_character(i64 n) {
    if (n <= 0) {
        return 0;
    }

    auto found = memo.find(n);
    if (found != memo.end()) {
        return found->second;
    }

    i64 total = 0;
    const i64 half = n / 2;
    for (i64 left = 1, right; left <= half; left = right + 1) {
        const i64 quotient = n / left;
        right = n / quotient;
        if (character_prefix(quotient)) {
            total += summatory_inverse_character(right);
            total -= summatory_inverse_character(left - 1);
            total %= MOD;
        }
    }

    i64 value = 1 + summatory_inverse_character(half) - total;
    value %= MOD;
    if (value < 0) {
        value += MOD;
    }

    memo.emplace(n, static_cast<int>(value));
    return static_cast<int>(value);
}

int cube_prefix_sum(i64 n) {
    i64 a = n % MOD;
    i64 b = (n + 1) % MOD;
    i64 half_product;
    if ((n & 1LL) == 0) {
        half_product = ((n / 2) % MOD) * b % MOD;
    } else {
        half_product = a * (((n + 1) / 2) % MOD) % MOD;
    }
    return static_cast<int>(half_product * half_product % MOD);
}

int solve(i64 n) {
    memo.reserve(4'500'000);
    memo.max_load_factor(0.7);
    memo.emplace(0, 0);

    i64 answer = 0;
    for (i64 left = 1, right; left <= n; left = right + 1) {
        const i64 quotient = n / left;
        right = n / quotient;

        i64 block = summatory_inverse_character(right);
        block -= summatory_inverse_character(left - 1);
        block %= MOD;
        if (block < 0) {
            block += MOD;
        }

        answer += block * cube_prefix_sum(quotient) % MOD;
        answer %= MOD;
    }

    return static_cast<int>(answer);
}

i64 parse_n(int argc, char** argv) {
    return argc > 1 ? std::atoll(argv[1]) : DEFAULT_N;
}

}  // namespace

int main(int argc, char** argv) {
    std::cout << solve(parse_n(argc, argv)) << '\n';
    return 0;
}
