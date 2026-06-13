#include <algorithm>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <vector>

namespace {

using u64 = std::uint64_t;

constexpr int TARGET_MOD = 10'000'019;
constexpr int TARGET_DIGITS = 32;

std::vector<int> powers10(int max_power, int mod) {
    std::vector<int> pow10(max_power + 1, 1);
    for (int i = 1; i <= max_power; ++i) {
        pow10[i] = static_cast<int>((10LL * pow10[i - 1]) % mod);
    }
    return pow10;
}

std::vector<int> palindrome_coefficients(int length, int mod,
                                         const std::vector<int>& pow10) {
    const int half = (length + 1) / 2;
    std::vector<int> coeffs;
    coeffs.reserve(half);

    for (int i = 0; i < half; ++i) {
        const int mirror = length - 1 - i;
        if (i == mirror) {
            coeffs.push_back(pow10[i]);
        } else {
            coeffs.push_back((pow10[i] + pow10[mirror]) % mod);
        }
    }

    return coeffs;
}

u64 assignment_count(int variables, bool includes_leading_digit) {
    if (variables == 0) return 1;

    u64 count = includes_leading_digit ? 9 : 1;
    for (int i = includes_leading_digit ? 1 : 0; i < variables; ++i) {
        count *= 10;
    }
    return count;
}

std::vector<int> residue_sums(const std::vector<int>& coeffs, int begin, int end,
                              bool first_digit_nonzero, int mod) {
    std::vector<int> sums;
    sums.reserve(static_cast<std::size_t>(
        assignment_count(end - begin, first_digit_nonzero)));

    const auto dfs = [&](const auto& self, int pos, int residue) -> void {
        if (pos == end) {
            sums.push_back(residue);
            return;
        }

        const int first_digit = (pos == begin && first_digit_nonzero) ? 1 : 0;
        const int coeff = coeffs[pos];
        for (int digit = first_digit; digit <= 9; ++digit) {
            self(self, pos + 1,
                 static_cast<int>((residue + 1LL * digit * coeff) % mod));
        }
    };

    dfs(dfs, begin, 0);
    return sums;
}

int best_split(int variables) {
    int best = 1;
    u64 best_work = assignment_count(1, true) + assignment_count(variables - 1, false);

    for (int split = 2; split <= variables; ++split) {
        const u64 work = assignment_count(split, true)
                       + assignment_count(variables - split, false);
        if (work < best_work) {
            best_work = work;
            best = split;
        }
    }

    return best;
}

void add_counted_side(const std::vector<int>& coeffs, int variables, int mod,
                      std::vector<std::uint32_t>& counts) {
    const int first_chunk = std::min(4, variables);
    const std::vector<int> left = residue_sums(coeffs, 0, first_chunk, true, mod);
    const std::vector<int> right = residue_sums(coeffs, first_chunk, variables, false, mod);

    for (const int a : left) {
        for (const int b : right) {
            int residue = a + b;
            if (residue >= mod) residue -= mod;
            ++counts[residue];
        }
    }
}

u64 query_free_side(const std::vector<int>& coeffs, int begin, int end, int mod,
                    const std::vector<std::uint32_t>& counts) {
    const int first_chunk_end = std::min(begin + 4, end);
    const std::vector<int> left = residue_sums(coeffs, begin, first_chunk_end, false, mod);
    const std::vector<int> right = residue_sums(coeffs, first_chunk_end, end, false, mod);

    u64 total = 0;
    for (const int a : left) {
        for (const int b : right) {
            int residue = a + b;
            if (residue >= mod) residue -= mod;
            total += counts[residue == 0 ? 0 : mod - residue];
        }
    }
    return total;
}

u64 count_length(int length, int mod, std::vector<std::uint32_t>& counts,
                 const std::vector<int>& pow10) {
    const std::vector<int> coeffs = palindrome_coefficients(length, mod, pow10);
    const int variables = static_cast<int>(coeffs.size());
    const int split = best_split(variables);

    std::fill(counts.begin(), counts.end(), 0);
    add_counted_side(coeffs, split, mod, counts);
    return query_free_side(coeffs, split, variables, mod, counts);
}

u64 count_palindromes(int max_digits, int mod) {
    const std::vector<int> pow10 = powers10(max_digits, mod);
    std::vector<std::uint32_t> counts(static_cast<std::size_t>(mod));

    u64 total = 0;
    for (int length = 1; length <= max_digits; ++length) {
        total += count_length(length, mod, counts, pow10);
    }
    return total;
}

}  // namespace

int main() {
    if (count_palindromes(5, 109) != 9) {
        throw std::runtime_error("validation against the sample failed");
    }

    std::cout << count_palindromes(TARGET_DIGITS, TARGET_MOD) << '\n';
    return 0;
}
