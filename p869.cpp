#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <limits>
#include <vector>

using i64 = std::int64_t;
using u32 = std::uint32_t;
using u64 = std::uint64_t;

namespace {

std::vector<bool> prime_sieve(int limit) {
    std::vector<bool> is_prime(limit + 1, true);
    is_prime[0] = false;
    is_prime[1] = false;
    for (int prime = 2; 1LL * prime * prime <= limit; ++prime) {
        if (!is_prime[prime]) {
            continue;
        }
        for (int multiple = prime * prime;
             multiple <= limit;
             multiple += prime) {
            is_prime[multiple] = false;
        }
    }
    return is_prime;
}

int bit_length(int value) {
    int result = 0;
    while (value) {
        ++result;
        value >>= 1;
    }
    return result;
}

u32 reverse_bits(u32 value, int bits) {
    u32 result = 0;
    for (int bit = 0; bit < bits; ++bit) {
        result = (result << 1) | ((value >> bit) & 1U);
    }
    return result;
}

long double optimal_expected_score(int limit) {
    const int bits = bit_length(limit);
    const auto is_prime = prime_sieve(limit);
    std::vector<u64> ordered_primes;
    ordered_primes.reserve(limit / 16);

    for (int prime = 2; prime <= limit; ++prime) {
        if (is_prime[prime]) {
            const u32 key = reverse_bits(prime, bits);
            ordered_primes.push_back(
                (static_cast<u64>(key) << bits) | prime
            );
        }
    }
    std::sort(ordered_primes.begin(), ordered_primes.end());

    const u64 value_mask = (1ULL << bits) - 1;
    i64 correct_guesses = 0;

    // Sorting by reversed bits makes every known least-significant-bit
    // suffix a contiguous block.  At each node of that implicit trie, the
    // optimal guess is simply its more numerous child.
    for (int depth = 0; depth < bits; ++depth) {
        const u32 minimum_value = 1U << depth;
        u32 current_prefix = std::numeric_limits<u32>::max();
        i64 zero_count = 0;
        i64 one_count = 0;

        for (u64 encoded : ordered_primes) {
            const u32 key = encoded >> bits;
            const u32 prefix = key >> (bits - depth);
            if (prefix != current_prefix) {
                correct_guesses += std::max(zero_count, one_count);
                current_prefix = prefix;
                zero_count = 0;
                one_count = 0;
            }

            const u32 prime = encoded & value_mask;
            if (prime < minimum_value) {
                continue;
            }
            const int next_bit = (
                key >> (bits - depth - 1)
            ) & 1U;
            if (next_bit) {
                ++one_count;
            } else {
                ++zero_count;
            }
        }
        correct_guesses += std::max(zero_count, one_count);
    }

    return static_cast<long double>(correct_guesses)
        / ordered_primes.size();
}

}  // namespace

int main(int argc, char** argv) {
    const int limit = argc > 1 ? std::stoi(argv[1]) : 100'000'000;
    assert(limit >= 2);
    std::cout << std::fixed << std::setprecision(8)
              << optimal_expected_score(limit) << '\n';
}
