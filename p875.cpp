#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>

using i64 = std::int64_t;
using u32 = std::uint32_t;

namespace {

constexpr i64 MODULUS = 1'001'961'001;

i64 prime_power_q(int prime, int exponent) {
    if (prime == 2) {
        i64 value = 128;
        i64 new_term = 2'048;
        for (int power = 2; power <= exponent; ++power) {
            value = (128 * value + new_term) % MODULUS;
            new_term = 16 * new_term % MODULUS;
        }
        return value;
    }

    const i64 p = prime % MODULUS;
    const i64 p2 = p * p % MODULUS;
    const i64 p3 = p2 * p % MODULUS;
    const i64 p7 = p3 * p3 % MODULUS * p % MODULUS;
    i64 p_to_power_minus_one = 1;
    i64 p_to_three_power = 1;
    i64 value = 1;

    for (int power = 1; power <= exponent; ++power) {
        p_to_three_power = p_to_three_power * p3 % MODULUS;
        const i64 phi = p_to_power_minus_one * (prime - 1) % MODULUS;
        value = (
            p7 * value + phi * p_to_three_power
        ) % MODULUS;
        p_to_power_minus_one = p_to_power_minus_one * p % MODULUS;
    }
    return value;
}

std::vector<u32> smallest_prime_factors(int limit) {
    std::vector<u32> smallest(limit + 1);
    std::vector<int> primes;
    for (int value = 2; value <= limit; ++value) {
        if (smallest[value] == 0) {
            smallest[value] = value;
            primes.push_back(value);
        }
        for (int prime : primes) {
            const i64 product = 1LL * value * prime;
            if (product > limit || prime > static_cast<int>(smallest[value])) {
                break;
            }
            smallest[product] = prime;
        }
    }
    return smallest;
}

std::vector<u32> q_values(int limit) {
    const auto smallest = smallest_prime_factors(limit);
    std::vector<u32> values(limit + 1);
    values[1] = 1;
    for (int number = 2; number <= limit; ++number) {
        const int prime = smallest[number];
        int remaining = number;
        int exponent = 0;
        do {
            remaining /= prime;
            ++exponent;
        } while (remaining % prime == 0);

        values[number] = static_cast<u32>(
            values[remaining] * prime_power_q(prime, exponent) % MODULUS
        );
    }
    return values;
}

}  // namespace

int main(int argc, char** argv) {
    const int limit = argc > 1 ? std::stoi(argv[1]) : 12'345'678;
    assert(limit >= 1);
    const auto values = q_values(limit);
    if (argc > 2) {
        std::cout << values[limit] << '\n';
        return 0;
    }
    i64 result = 0;
    for (int number = 1; number <= limit; ++number) {
        result += values[number];
        if (result >= MODULUS) {
            result -= MODULUS;
        }
    }
    std::cout << result << '\n';
}
