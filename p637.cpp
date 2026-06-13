#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <vector>

namespace {

constexpr int LIMIT = 10'000'000;

std::vector<unsigned char> step_counts(int base) {
    std::vector<unsigned char> steps(LIMIT + 1);
    int digits[32];

    for (int n = 1; n <= LIMIT; ++n) {
        if (n < base) {
            steps[n] = 0;
            continue;
        }

        int length = 0;
        int digit_sum = 0;
        for (int remaining = n; remaining; remaining /= base) {
            int digit = remaining % base;
            digits[length++] = digit;
            digit_sum += digit;
        }
        std::reverse(digits, digits + length);

        if (digit_sum < base) {
            steps[n] = 1;
            continue;
        }

        unsigned char best = 255;
        const int masks = 1 << (length - 1);
        for (int mask = 1; mask < masks; ++mask) {
            int sum = 0;
            int block = digits[0];

            for (int i = 0; i < length - 1; ++i) {
                if ((mask >> i) & 1) {
                    sum += block;
                    block = digits[i + 1];
                } else {
                    block = block * base + digits[i + 1];
                }
            }
            sum += block;

            // Every nontrivial split is smaller than n, so its step count is
            // already known. Once a split reaches f <= 1, this n has f = 2,
            // which is optimal here because digit_sum >= base.
            unsigned char candidate = steps[sum] + 1;
            if (candidate < best) {
                best = candidate;
                if (best == 2) {
                    break;
                }
            }
        }

        steps[n] = best;
    }

    return steps;
}

std::int64_t solve() {
    const auto base10 = step_counts(10);
    const auto base3 = step_counts(3);

    std::int64_t total = 0;
    for (int n = 1; n <= LIMIT; ++n) {
        if (base10[n] == base3[n]) {
            total += n;
        }
    }
    return total;
}

}  // namespace

int main() {
    std::cout << solve() << '\n';
    return 0;
}
