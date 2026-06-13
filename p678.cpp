#include <algorithm>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <unordered_map>
#include <utility>
#include <vector>

using i64 = long long;
using u64 = unsigned long long;
using u128 = __uint128_t;

static constexpr u64 LIMIT = 1000000000000000000ULL;
static constexpr int ROOT_LIMIT = 1000000;

static u64 pow_limited(u64 base, int exponent, u64 limit = LIMIT) {
    u128 value = 1;
    for (int i = 0; i < exponent; ++i) {
        value *= base;
        if (value > limit) return limit + 1;
    }
    return static_cast<u64>(value);
}

static u64 int_root(u64 n, int exponent) {
    u64 lo = 1;
    u64 hi = 1;
    while (pow_limited(hi + 1, exponent, n) <= n) hi *= 2;
    while (lo < hi) {
        u64 mid = (lo + hi + 1) / 2;
        if (pow_limited(mid, exponent, n) <= n) {
            lo = mid;
        } else {
            hi = mid - 1;
        }
    }
    return lo;
}

static std::vector<int> smallest_prime_factors() {
    std::vector<int> spf(ROOT_LIMIT + 1);
    std::iota(spf.begin(), spf.end(), 0);
    for (int p = 2; p * p <= ROOT_LIMIT; ++p) {
        if (spf[p] == p) {
            for (int n = p * p; n <= ROOT_LIMIT; n += p) {
                if (spf[n] == n) spf[n] = p;
            }
        }
    }
    return spf;
}

static std::vector<std::pair<int, int>> factor(int n, const std::vector<int>& spf) {
    std::vector<std::pair<int, int>> result;
    while (n > 1) {
        int p = spf[n];
        int exponent = 0;
        while (n % p == 0) {
            n /= p;
            ++exponent;
        }
        result.push_back({p, exponent});
    }
    return result;
}

static i64 square_sum_count(const std::vector<std::pair<int, int>>& factorisation, int power) {
    i64 product = 1;
    bool square = true;
    bool twice_square = false;

    for (const auto& [p, exponent_in_c] : factorisation) {
        int exponent = exponent_in_c * power;
        if (p % 4 == 3 && exponent % 2 == 1) return 0;
        if (p % 4 == 1) product *= exponent + 1;
        if (exponent % 2 == 1) square = false;
        if (p == 2) {
            twice_square = exponent % 2 == 1;
        } else if (exponent % 2 == 1) {
            twice_square = false;
        }
    }

    i64 r2 = 4 * product;
    return (r2 - (square ? 4 : 0) - (twice_square ? 4 : 0)) / 8;
}

static void divisors_up_to(
    const std::vector<std::pair<int, int>>& factorisation,
    u64 limit,
    int index,
    u64 current,
    std::vector<u64>& divisors
) {
    if (index == static_cast<int>(factorisation.size())) {
        divisors.push_back(current);
        return;
    }

    auto [p, exponent] = factorisation[index];
    u64 value = current;
    for (int i = 0; i <= exponent && value <= limit; ++i) {
        divisors_up_to(factorisation, limit, index + 1, value, divisors);
        if (i != exponent) value *= static_cast<u64>(p);
    }
}

static i64 cube_sum_count(
    int c,
    int power,
    const std::vector<std::vector<std::pair<int, int>>>& factors
) {
    u64 n = pow_limited(c, power);
    std::vector<std::pair<int, int>> powered_factorisation;
    powered_factorisation.reserve(factors[c].size());
    for (const auto& [p, exponent] : factors[c]) {
        powered_factorisation.push_back({p, exponent * power});
    }

    std::vector<u64> divisors;
    divisors_up_to(powered_factorisation, 2 * int_root(n, 3) + 2, 0, 1, divisors);

    i64 count = 0;
    for (u64 sum : divisors) {
        u64 quotient = n / sum;
        if (4 * quotient <= sum * sum) continue;
        u64 numerator = 4 * quotient - sum * sum;
        if (numerator % 3 != 0) continue;
        u64 diff_squared = numerator / 3;
        u64 diff = static_cast<u64>(std::sqrt(static_cast<long double>(diff_squared)));
        while ((diff + 1) * (u128)(diff + 1) <= diff_squared) ++diff;
        while (diff * (u128)diff > diff_squared) --diff;
        if (diff == 0 || diff * diff != diff_squared || (sum < diff) || ((sum - diff) & 1)) {
            continue;
        }
        u64 a = (sum - diff) / 2;
        u64 b = (sum + diff) / 2;
        if (a > 0 && a < b && a * (u128)a * a + b * (u128)b * b == n) {
            ++count;
        }
    }
    return count;
}

static i64 count_e2_and_e3(const std::vector<std::vector<std::pair<int, int>>>& factors) {
    i64 total = 0;
    for (int f = 3; pow_limited(2, f) <= LIMIT; ++f) {
        int max_c = static_cast<int>(int_root(LIMIT, f));
        for (int c = 1; c <= max_c; ++c) {
            total += square_sum_count(factors[c], f);
            total += cube_sum_count(c, f, factors);
        }
    }
    return total;
}

struct VectorHash {
    std::size_t operator()(u64 value) const {
        return std::hash<u64>{}(value);
    }
};

static i64 count_e_at_least_4() {
    std::unordered_map<u64, int, VectorHash> perfect_powers;
    perfect_powers.reserve(1100000);
    for (int f = 3; pow_limited(2, f) <= LIMIT; ++f) {
        for (u64 c = 1;; ++c) {
            u64 value = pow_limited(c, f);
            if (value > LIMIT) break;
            ++perfect_powers[value];
        }
    }

    i64 total = 0;
    for (int e = 4; pow_limited(2, e) + 1 <= LIMIT; ++e) {
        std::vector<u64> powers(1, 0);
        for (u64 n = 1;; ++n) {
            u64 value = pow_limited(n, e);
            if (value > LIMIT) break;
            powers.push_back(value);
        }

        int count = static_cast<int>(powers.size()) - 1;
        for (int b = 2; b <= count; ++b) {
            u64 b_power = powers[b];
            for (int a = 1; a < b; ++a) {
                u64 sum = b_power + powers[a];
                if (sum < b_power || sum > LIMIT) break;
                auto found = perfect_powers.find(sum);
                if (found != perfect_powers.end()) total += found->second;
            }
        }
    }
    return total;
}

int main() {
    std::vector<int> spf = smallest_prime_factors();
    std::vector<std::vector<std::pair<int, int>>> factors(ROOT_LIMIT + 1);
    for (int n = 1; n <= ROOT_LIMIT; ++n) {
        factors[n] = factor(n, spf);
    }

    std::cout << count_e2_and_e3(factors) + count_e_at_least_4() << '\n';
    return 0;
}
