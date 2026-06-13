#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <set>
#include <vector>

using u64 = unsigned long long;

struct Digits {
    int length = 0;
    std::uint32_t mask = 0;
    bool unique = true;
};

Digits digit_mask(u64 value, int base) {
    Digits result;
    while (value > 0) {
        int digit = static_cast<int>(value % base);
        std::uint32_t bit = 1u << digit;
        if (result.mask & bit) {
            result.unique = false;
        }
        result.mask |= bit;
        ++result.length;
        value /= base;
    }
    return result;
}

int digit_length(u64 value, const std::vector<u64>& powers) {
    int length = 1;
    while (length + 1 < static_cast<int>(powers.size()) && value >= powers[length]) {
        ++length;
    }
    return length;
}

int max_largest_side_digits(int base, const std::vector<u64>& powers) {
    int best = 1;
    for (int length = 2; length <= 7; ++length) {
        // For sorted sides x <= y < z, (2z-2y-x)(2z+2y+x)=3x^2, so
        // 3x^2 > 2z.  Also y has at least length-1 digits because z<x+y.
        u64 z_min = powers[length - 1];
        u64 x = 1;
        while (3 * x * x <= 2 * z_min) {
            ++x;
        }
        int lower_total = length + (length - 1) + digit_length(x, powers);
        if (lower_total <= base) {
            best = length;
        }
    }
    return best;
}

bool is_pandigital_triangle(u64 a, u64 b, u64 c, int base) {
    Digits da = digit_mask(a, base);
    if (!da.unique) {
        return false;
    }

    Digits db = digit_mask(b, base);
    if (!db.unique || (da.mask & db.mask)) {
        return false;
    }

    Digits dc = digit_mask(c, base);
    if (!dc.unique || ((da.mask | db.mask) & dc.mask)) {
        return false;
    }

    std::uint32_t full_mask = (1u << base) - 1u;
    return da.length + db.length + dc.length == base
        && (da.mask | db.mask | dc.mask) == full_mask;
}

u64 solve_base(int base) {
    std::vector<u64> powers(base + 2, 1);
    for (int i = 1; i < static_cast<int>(powers.size()); ++i) {
        powers[i] = powers[i - 1] * static_cast<u64>(base);
    }

    int max_digits = max_largest_side_digits(base, powers);
    u64 max_c = powers[max_digits] - 1;
    std::set<std::array<u64, 3>> seen;
    u64 total = 0;

    for (u64 m = 2; m * m <= max_c; ++m) {
        for (u64 n = 1; n < m; ++n) {
            u64 a0 = m * m - n * n;
            u64 b0 = 2 * m * n + n * n;
            u64 c0 = m * m + m * n + n * n;
            if (c0 > max_c) {
                break;
            }

            if (std::gcd(m, n) != 1 || (m - n) % 3 == 0) {
                continue;
            }

            u64 d = 1;
            while (true) {
                u64 a = d * a0;
                u64 b = d * b0;
                u64 c = d * c0;
                int length_sum = digit_length(a, powers)
                    + digit_length(b, powers)
                    + digit_length(c, powers);
                if (length_sum > base) {
                    break;
                }
                if (length_sum == base && is_pandigital_triangle(a, b, c, base)) {
                    std::array<u64, 3> key = {std::min(a, b), std::max(a, b), c};
                    if (seen.insert(key).second) {
                        total += c;
                    }
                }
                ++d;
            }
        }
    }

    return total;
}

int main() {
    u64 answer = 0;
    for (int base = 9; base <= 18; ++base) {
        answer += solve_base(base);
    }
    std::cout << answer << '\n';
    return 0;
}
