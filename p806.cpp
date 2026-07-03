#include <algorithm>
#include <array>
#include <cassert>
#include <functional>
#include <iostream>
#include <vector>

constexpr int MOD = 1'000'000'007;
constexpr int TARGET_N = 100'000;

struct Monomial {
    int dx;
    int dy;
    int coeff;
};

const std::array<std::vector<Monomial>, 3> INITIAL = {{
    {{0, 0, 1}},
    {{0, 0, 1}, {2, 0, 1}, {1, 1, 1}, {0, 1, 1}},
    {
        {0, 0, 1}, {2, 0, 2}, {1, 1, 3}, {0, 1, 1}, {4, 0, 1}, {3, 1, 1},
        {2, 1, 3}, {2, 2, 1}, {1, 3, 1}, {0, 2, 1}, {0, 3, 1},
    },
}};

long long mod_pow(long long base, long long exponent) {
    long long result = 1;
    while (exponent) {
        if (exponent & 1) result = result * base % MOD;
        base = base * base % MOD;
        exponent >>= 1;
    }
    return result;
}

std::vector<int> next_recurrence_row(
    const std::vector<int>& previous,
    const std::vector<int>& before_previous,
    const std::vector<int>& three_back
) {
    int length = std::max({previous.size(), before_previous.size(), three_back.size() + 1});
    std::vector<int> result(length);
    for (int i = 0; i < static_cast<int>(previous.size()); ++i) {
        result[i] = (result[i] + 2LL * previous[i]) % MOD;
    }
    for (int i = 0; i < static_cast<int>(before_previous.size()); ++i) {
        result[i] -= before_previous[i];
        if (result[i] < 0) result[i] += MOD;
    }
    for (int i = 0; i < static_cast<int>(three_back.size()); ++i) {
        result[i + 1] += three_back[i];
        if (result[i + 1] >= MOD) result[i + 1] -= MOD;
    }
    return result;
}

std::array<std::vector<int>, 3> fundamental_coefficients(int pairs) {
    std::array<std::vector<int>, 3> result;
    for (int source = 0; source < 3; ++source) {
        std::vector<int> a = source == 0 ? std::vector<int>{1} : std::vector<int>{0};
        std::vector<int> b = source == 1 ? std::vector<int>{1} : std::vector<int>{0};
        std::vector<int> c = source == 2 ? std::vector<int>{1} : std::vector<int>{0};

        if (pairs == 0) {
            result[source] = a;
        } else if (pairs == 1) {
            result[source] = b;
        } else if (pairs == 2) {
            result[source] = c;
        } else {
            for (int n = 3; n <= pairs; ++n) {
                std::vector<int> next = next_recurrence_row(c, b, a);
                a.swap(b);
                b.swap(c);
                c.swap(next);
            }
            result[source] = c;
        }
    }
    return result;
}

std::vector<std::array<int, 3>> losing_count_targets(int disks) {
    int half = disks / 2;
    std::vector<int> bits;
    for (int bit = 0; bit < 31; ++bit) {
        if ((half >> bit) & 1) bits.push_back(bit);
    }

    std::vector<std::array<int, 3>> targets;
    std::function<void(int, int, int)> dfs = [&](int index, int a, int b) {
        if (index == static_cast<int>(bits.size())) {
            targets.push_back({a, b, a ^ b});
            return;
        }
        int value = 1 << bits[index];
        dfs(index + 1, a | value, b);
        dfs(index + 1, a, b | value);
        dfs(index + 1, a | value, b | value);
    };
    dfs(0, 0, 0);
    return targets;
}

long long losing_position_count(int disks) {
    if (disks & 1) return 0;

    int pairs = disks / 2;
    std::vector<int> factorial(disks + 1), inv_factorial(disks + 1);
    factorial[0] = 1;
    for (int i = 1; i <= disks; ++i) factorial[i] = 1LL * factorial[i - 1] * i % MOD;
    inv_factorial[disks] = mod_pow(factorial[disks], MOD - 2);
    for (int i = disks; i >= 1; --i) inv_factorial[i - 1] = 1LL * inv_factorial[i] * i % MOD;

    auto multinomial = [&](int total, int a, int b) -> int {
        if (a < 0 || b < 0 || a + b > total) return 0;
        return 1LL * factorial[total] * inv_factorial[a] % MOD * inv_factorial[b] % MOD *
               inv_factorial[total - a - b] % MOD;
    };

    std::array<std::vector<int>, 3> fundamentals = fundamental_coefficients(pairs);
    std::vector<int> powers4(pairs / 3 + 10);
    powers4[0] = 1;
    for (int i = 1; i < static_cast<int>(powers4.size()); ++i) powers4[i] = 4LL * powers4[i - 1] % MOD;

    long long total = 0;
    for (auto [target_a, target_b, target_c] : losing_count_targets(disks)) {
        long long coefficient = 0;
        for (int source = 0; source < 3; ++source) {
            const auto& recurrence = fundamentals[source];
            for (int j = 0; j < static_cast<int>(recurrence.size()); ++j) {
                int recurrence_coeff = recurrence[j];
                if (recurrence_coeff == 0) continue;
                int s_power = pairs - source - 3 * j;
                if (s_power < 0) continue;
                long long base = 1LL * recurrence_coeff * powers4[j] % MOD;

                for (const Monomial& monomial : INITIAL[source]) {
                    int a = target_a - monomial.dx - 2 * j;
                    int b = target_b - monomial.dy - 2 * j;
                    if (a >= 0 && b >= 0 && a % 2 == 0 && b % 2 == 0) {
                        coefficient += base * monomial.coeff % MOD *
                                       multinomial(s_power, a / 2, b / 2) % MOD;
                        coefficient %= MOD;
                    }
                }
            }
        }
        total += coefficient;
        total %= MOD;
    }
    return total;
}

long long f_value(int disks) {
    long long count = losing_position_count(disks);
    return count * ((mod_pow(2, disks) - 1 + MOD) % MOD) % MOD * ((MOD + 1LL) / 2) % MOD;
}

int main() {
    assert(f_value(4) == 30);
    assert(f_value(10) == 67518);
    std::cout << f_value(TARGET_N) << '\n';
}
