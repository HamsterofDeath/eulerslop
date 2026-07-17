#include <algorithm>
#include <cassert>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <vector>

using i64 = std::int64_t;
using i128 = __int128_t;

namespace {

i64 integer_square_root(i64 value) {
    i64 root = static_cast<i64>(std::sqrt(
        static_cast<long double>(value)
    ));
    while (static_cast<i128>(root + 1) * (root + 1) <= value) {
        ++root;
    }
    while (static_cast<i128>(root) * root > value) {
        --root;
    }
    return root;
}

i64 integer_cube_root(i64 value) {
    i64 root = static_cast<i64>(std::cbrt(
        static_cast<long double>(value)
    ));
    while (
        static_cast<i128>(root + 1) * (root + 1) * (root + 1)
        <= value
    ) {
        ++root;
    }
    while (static_cast<i128>(root) * root * root > value) {
        --root;
    }
    return root;
}

i64 nonzero_lattice_points(i64 norm_limit) {
    // One half-open 60-degree sector has x > 0 and y >= 0.
    // Its six rotations partition all nonzero triangular-lattice points.
    i64 sector_count = 0;
    const i64 radius = integer_square_root(norm_limit);
    for (i64 x = 1; x <= radius; ++x) {
        const i64 discriminant = 4 * norm_limit - 3 * x * x;
        const i64 root = integer_square_root(discriminant);
        const i64 largest_y = (root - x) / 2;
        sector_count += largest_y + 1;
    }
    return 6 * sector_count;
}

struct Sieve {
    std::vector<int> smallest_prime;
    std::vector<int> mobius;
};

Sieve make_sieve(int limit) {
    Sieve result{
        std::vector<int>(limit + 1),
        std::vector<int>(limit + 1),
    };
    std::vector<int> primes;
    result.mobius[1] = 1;

    for (int value = 2; value <= limit; ++value) {
        if (result.smallest_prime[value] == 0) {
            result.smallest_prime[value] = value;
            result.mobius[value] = -1;
            primes.push_back(value);
        }
        for (int prime : primes) {
            if (
                prime > result.smallest_prime[value]
                || 1LL * value * prime > limit
            ) {
                break;
            }
            result.smallest_prime[value * prime] = prime;
            if (value % prime == 0) {
                result.mobius[value * prime] = 0;
                break;
            }
            result.mobius[value * prime] = -result.mobius[value];
        }
    }
    return result;
}

i64 ordered_side_triples(int q, const std::vector<int>& smallest_prime) {
    int remaining = q;
    int exponent_of_three = 0;
    i64 divisor_count = 1;
    i64 character_sum = 1;

    while (remaining > 1) {
        const int prime = smallest_prime[remaining];
        int exponent = 0;
        while (remaining % prime == 0) {
            remaining /= prime;
            ++exponent;
        }
        if (prime == 3) {
            exponent_of_three = exponent;
        } else {
            divisor_count *= 2 * exponent + 1;
            if (prime % 3 == 1) {
                character_sum *= 2 * exponent + 1;
            }
        }
    }

    if (exponent_of_three > 0) {
        return (2 * exponent_of_three - 1) * divisor_count;
    }
    if (q % 3 == 1) {
        return (divisor_count + character_sum) / 2;
    }
    return (divisor_count - character_sum) / 2;
}

i128 weighted_lattice_sum(
    const std::vector<i64>& convolution,
    i64 norm_limit,
    const std::vector<i64>& small_lattice_counts
) {
    i128 result = 0;
    const i64 maximum_scale = integer_square_root(norm_limit);
    for (i64 scale = 1; scale <= maximum_scale; ++scale) {
        const i64 coefficient = convolution[scale];
        if (coefficient == 0) {
            continue;
        }
        const i64 reduced_limit = norm_limit / (scale * scale);
        const i64 lattice_count = (
            reduced_limit < static_cast<i64>(small_lattice_counts.size())
            ? small_lattice_counts[reduced_limit]
            : nonzero_lattice_points(reduced_limit)
        );
        result += static_cast<i128>(coefficient) * lattice_count;
    }
    return result;
}

i64 remarkable_triangles(i64 twice_radius) {
    // q^2 * Norm(z) <= 12r^2 = 3(2r)^2.
    const i64 norm_bound = 3 * twice_radius * twice_radius;
    const int maximum_q = static_cast<int>(
        integer_square_root(norm_bound)
    );
    const auto sieve = make_sieve(maximum_q);

    // A(q) counts ordered integer side triples for a distinguished
    // 60-degree vertex.  Equilateral triangles occur three times, so
    // using W(q)=3A(q)-2 makes the final division by three exact.
    std::vector<i64> convolution_multiple_of_three(maximum_q + 1);
    std::vector<i64> convolution_other(maximum_q + 1);
    for (int q = 1; q <= maximum_q; ++q) {
        const i64 weight = (
            3 * ordered_side_triples(q, sieve.smallest_prime) - 2
        );
        auto& convolution = (
            q % 3 == 0
            ? convolution_multiple_of_three
            : convolution_other
        );
        for (int factor = 1; 1LL * q * factor <= maximum_q; ++factor) {
            if (sieve.mobius[factor] != 0) {
                convolution[q * factor] += weight * sieve.mobius[factor];
            }
        }
    }

    const int small_limit = static_cast<int>(
        integer_cube_root(norm_bound) + 1
    );
    std::vector<i64> small_lattice_counts(small_limit + 1);
    for (int limit = 1; limit <= small_limit; ++limit) {
        small_lattice_counts[limit] = nonzero_lattice_points(limit);
    }

    i128 numerator = weighted_lattice_sum(
        convolution_multiple_of_three,
        norm_bound,
        small_lattice_counts
    );

    // For a primitive z, x == y (mod 3) iff 3 divides Norm(z).
    // Division by the ramified Eisenstein prime gives
    //
    //   P_diag(X) = P_all(X/3)-P_all(X/9)+P_all(X/27)-...
    i64 reduced_bound = norm_bound / 3;
    int sign = 1;
    while (reduced_bound > 0) {
        numerator += sign * weighted_lattice_sum(
            convolution_other,
            reduced_bound,
            small_lattice_counts
        );
        reduced_bound /= 3;
        sign = -sign;
    }

    assert(numerator % 3 == 0);
    return static_cast<i64>(numerator / 3);
}

}  // namespace

int main(int argc, char** argv) {
    const i64 twice_radius = (
        argc > 1 ? std::stoll(argv[1]) : 2'000'000LL
    );
    std::cout << remarkable_triangles(twice_radius) << '\n';
}
