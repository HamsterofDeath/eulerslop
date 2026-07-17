#include <algorithm>
#include <cassert>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <thread>
#include <vector>

using i64 = std::int64_t;
using i128 = __int128_t;

namespace {

constexpr i64 TARGET = 123'567'101'113LL;
constexpr i64 SPLIT = 60'000'000LL;
constexpr int MAX_ROOTS = 64;

struct PrimeRoots {
    int prime;
    i64 square;
    i64 first;
    i64 second;
};

struct RootSet {
    int size = 0;
    i64 values[MAX_ROOTS]{};
};

std::vector<PrimeRoots> admissible_primes;
std::vector<int> factor_primes;

i64 integer_sqrt(i64 value) {
    i64 root = static_cast<i64>(std::sqrt(static_cast<long double>(value)));
    while ((root + 1) <= value / (root + 1)) {
        ++root;
    }
    while (root > value / root) {
        --root;
    }
    return root;
}

i64 modular_power(i64 base, i64 exponent, i64 modulus) {
    i64 result = 1 % modulus;
    while (exponent) {
        if (exponent & 1) {
            result = static_cast<i64>((i128)result * base % modulus);
        }
        base = static_cast<i64>((i128)base * base % modulus);
        exponent >>= 1;
    }
    return result;
}

i64 extended_gcd(i64 first, i64 second, i64& x, i64& y) {
    if (second == 0) {
        x = 1;
        y = 0;
        return first;
    }
    i64 next_x;
    i64 next_y;
    const i64 divisor = extended_gcd(
        second, first % second, next_x, next_y
    );
    x = next_y;
    y = next_x - static_cast<i64>(
        (i128)next_y * (first / second)
    );
    return divisor;
}

i64 modular_inverse(i64 value, i64 modulus) {
    i64 x;
    i64 y;
    assert(extended_gcd(value, modulus, x, y) == 1);
    x %= modulus;
    return x < 0 ? x + modulus : x;
}

i64 square_root_minus_one(int prime) {
    for (i64 candidate = 2; candidate < prime; ++candidate) {
        if (modular_power(candidate, (prime - 1) / 2, prime) == prime - 1) {
            return modular_power(candidate, (prime - 1) / 4, prime);
        }
    }
    return -1;
}

PrimeRoots lift_roots(int prime) {
    const i64 root = square_root_minus_one(prime);
    const i64 square = 1LL * prime * prime;
    const i64 quotient = (root * root + 1) / prime;
    const i64 inverse = modular_power(2 * root % prime, prime - 2, prime);
    i64 lift = (prime - quotient % prime) % prime;
    lift = static_cast<i64>((i128)lift * inverse % prime);
    const i64 lifted_root = root + prime * lift;
    return {prime, square, lifted_root, square - lifted_root};
}

std::vector<char> prime_sieve(int limit) {
    std::vector<char> is_prime(limit + 1, true);
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

void initialize_primes() {
    const auto is_prime = prime_sieve(static_cast<int>(SPLIT));
    for (int prime = 5; prime <= SPLIT; prime += 4) {
        if (is_prime[prime]) {
            admissible_primes.push_back(lift_roots(prime));
        }
    }

    constexpr int FACTOR_LIMIT = 400'000;
    const auto is_factor_prime = prime_sieve(FACTOR_LIMIT);
    for (int prime = 2; prime <= FACTOR_LIMIT; ++prime) {
        if (is_factor_prime[prime]) {
            factor_primes.push_back(prime);
        }
    }
}

i64 count_residues(i64 limit, i64 modulus, const RootSet& roots) {
    i64 result = limit / modulus * roots.size;
    const i64 remainder = limit % modulus;
    for (int index = 0; index < roots.size; ++index) {
        result += roots.values[index] <= remainder;
    }
    return result;
}

RootSet combine_roots(
    const RootSet& old_roots,
    const PrimeRoots& new_prime,
    i64 old_modulus
) {
    RootSet combined;
    combined.size = 2 * old_roots.size;
    assert(combined.size <= MAX_ROOTS);
    const i64 inverse = modular_inverse(
        old_modulus % new_prime.square, new_prime.square
    );
    int output = 0;

    for (int index = 0; index < old_roots.size; ++index) {
        const i64 old_root = old_roots.values[index];
        const i64 targets[2] = {new_prime.first, new_prime.second};
        for (i64 target : targets) {
            i64 difference = target - old_root % new_prime.square;
            if (difference < 0) {
                difference += new_prime.square;
            }
            const i64 multiplier = static_cast<i64>(
                (i128)difference * inverse % new_prime.square
            );
            combined.values[output++] = static_cast<i64>(
                old_root + (i128)old_modulus * multiplier
            );
        }
    }
    return combined;
}

void enumerate_small_divisors(
    int start,
    i64 divisor,
    i64 square,
    const RootSet& roots,
    int mobius,
    i64 limit,
    i64 split,
    i64& result
) {
    for (int index = start;
         index < static_cast<int>(admissible_primes.size());
         ++index) {
        const auto& prime_roots = admissible_primes[index];
        if (divisor > split / prime_roots.prime) {
            break;
        }

        const i64 next_divisor = divisor * prime_roots.prime;
        const i64 next_square = next_divisor * next_divisor;
        const RootSet next_roots = combine_roots(
            roots, prime_roots, square
        );
        const int next_mobius = -mobius;
        result += next_mobius
            * count_residues(limit, next_square, next_roots);
        enumerate_small_divisors(
            index + 1,
            next_divisor,
            next_square,
            next_roots,
            next_mobius,
            limit,
            split,
            result
        );
    }
}

i64 small_divisor_contribution(i64 limit, i64 split) {
    if (split < 5) {
        return 0;
    }
    unsigned worker_count = std::thread::hardware_concurrency();
    worker_count = std::max(1U, std::min(16U, worker_count));
    std::vector<i64> subtotals(worker_count, 0);
    std::vector<std::thread> workers;

    for (unsigned worker = 0; worker < worker_count; ++worker) {
        workers.emplace_back([&, worker]() {
            i64 subtotal = 0;
            for (int index = static_cast<int>(worker);
                 index < static_cast<int>(admissible_primes.size());
                 index += static_cast<int>(worker_count)) {
                const auto& prime_roots = admissible_primes[index];
                if (prime_roots.prime > split) {
                    break;
                }
                RootSet roots;
                roots.size = 2;
                roots.values[0] = prime_roots.first;
                roots.values[1] = prime_roots.second;
                subtotal -= count_residues(
                    limit, prime_roots.square, roots
                );
                enumerate_small_divisors(
                    index + 1,
                    prime_roots.prime,
                    prime_roots.square,
                    roots,
                    -1,
                    limit,
                    split,
                    subtotal
                );
            }
            subtotals[worker] = subtotal;
        });
    }
    for (auto& worker : workers) {
        worker.join();
    }

    i64 result = 0;
    for (i64 subtotal : subtotals) {
        result += subtotal;
    }
    return result;
}

bool fundamental_negative_pell(i64 coefficient, i64 x_limit, i64& x, i64& y) {
    const i64 initial = integer_sqrt(coefficient);
    if (initial * initial == coefficient) {
        return false;
    }

    i64 middle = 0;
    i64 denominator = 1;
    i64 term = initial;
    i128 previous_numerator = 1;
    i128 previous_denominator = 0;
    i128 numerator = initial;
    i128 denominator_value = 1;

    for (int step = 1; ; ++step) {
        middle = denominator * term - middle;
        denominator = (coefficient - middle * middle) / denominator;
        term = (initial + middle) / denominator;

        const i128 next_numerator = term * numerator + previous_numerator;
        const i128 next_denominator =
            term * denominator_value + previous_denominator;
        previous_numerator = numerator;
        previous_denominator = denominator_value;
        numerator = next_numerator;
        denominator_value = next_denominator;

        if (denominator == 1 && term == 2 * initial) {
            if (
                step % 2 == 1
                && previous_numerator <= x_limit
                && previous_denominator <= x_limit
            ) {
                x = static_cast<i64>(previous_numerator);
                y = static_cast<i64>(previous_denominator);
                return true;
            }
            return false;
        }
        if (numerator > x_limit || denominator_value > x_limit) {
            return false;
        }
    }
}

int mobius(i64 value) {
    int result = 1;
    for (int prime : factor_primes) {
        if (1LL * prime * prime > value) {
            break;
        }
        if (value % prime == 0) {
            value /= prime;
            if (value % prime == 0) {
                return 0;
            }
            result = -result;
        }
    }
    if (value > 1) {
        result = -result;
    }
    return result;
}

std::vector<char> admissible_pell_coefficients(int maximum) {
    std::vector<char> valid(maximum + 1, true);
    valid[0] = false;
    const auto is_prime = prime_sieve(maximum);
    for (int prime = 3; prime <= maximum; prime += 4) {
        if (!is_prime[prime]) {
            continue;
        }
        for (int multiple = prime; multiple <= maximum; multiple += prime) {
            valid[multiple] = false;
        }
    }
    return valid;
}

i64 large_divisor_contribution(i64 limit, i64 split) {
    const int maximum = static_cast<int>(
        ((i128)limit * limit + 1) / ((i128)split * split)
    );
    if (maximum == 0) {
        return 0;
    }
    const auto valid = admissible_pell_coefficients(maximum);
    unsigned worker_count = std::thread::hardware_concurrency();
    worker_count = std::max(1U, std::min(16U, worker_count));
    std::vector<i64> subtotals(worker_count, 0);
    std::vector<std::thread> workers;

    for (unsigned worker = 0; worker < worker_count; ++worker) {
        workers.emplace_back([&, worker]() {
            i64 subtotal = 0;
            for (int coefficient = 1 + static_cast<int>(worker);
                 coefficient <= maximum;
                 coefficient += static_cast<int>(worker_count)) {
                if (!valid[coefficient]) {
                    continue;
                }
                const i64 root = integer_sqrt(coefficient);
                if (root * root == coefficient) {
                    continue;
                }

                i64 first_x;
                i64 first_y;
                if (!fundamental_negative_pell(
                        coefficient, limit, first_x, first_y)) {
                    continue;
                }

                const i128 unit_x =
                    (i128)first_x * first_x
                    + (i128)coefficient * first_y * first_y;
                const i128 unit_y = 2 * (i128)first_x * first_y;
                i64 x = first_x;
                i64 y = first_y;

                while (x <= limit) {
                    if (y > split) {
                        subtotal += mobius(y);
                    }
                    const i128 next_x =
                        (i128)x * unit_x
                        + (i128)coefficient * y * unit_y;
                    const i128 next_y =
                        (i128)x * unit_y + (i128)y * unit_x;
                    if (next_x > limit) {
                        break;
                    }
                    x = static_cast<i64>(next_x);
                    y = static_cast<i64>(next_y);
                }
            }
            subtotals[worker] = subtotal;
        });
    }
    for (auto& worker : workers) {
        worker.join();
    }

    i64 result = 0;
    for (i64 subtotal : subtotals) {
        result += subtotal;
    }
    return result;
}

i64 squarefree_values(i64 limit) {
    const i64 split = std::min(limit, SPLIT);
    return limit
        + small_divisor_contribution(limit, split)
        + large_divisor_contribution(limit, split);
}

}  // namespace

int main() {
    initialize_primes();
    assert(squarefree_values(10) == 9);
    assert(squarefree_values(1'000) == 895);
    std::cout << squarefree_values(TARGET) << '\n';
}
