#include <algorithm>
#include <cassert>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <tuple>

using i64 = std::int64_t;
using i128 = __int128_t;
using u64 = std::uint64_t;

namespace {

constexpr i64 MODULUS = 1'095'912'793;  // 1031^3 + 2

i128 fourth_power(i64 value) {
    const i128 square = static_cast<i128>(value) * value;
    return square * square;
}

i64 fourth_root_ceiling(i64 value) {
    i64 root = static_cast<i64>(
        std::sqrt(std::sqrt(static_cast<long double>(value)))
    );
    while (fourth_power(root) < value) {
        ++root;
    }
    while (root > 0 && fourth_power(root - 1) >= value) {
        --root;
    }
    return root;
}

i64 square_root_floor(i64 value) {
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

bool is_cube(i64 value) {
    i64 root = static_cast<i64>(std::cbrt(
        static_cast<long double>(value)
    ));
    while (static_cast<i128>(root + 1) * (root + 1) * (root + 1) <= value) {
        ++root;
    }
    while (static_cast<i128>(root) * root * root > value) {
        --root;
    }
    return static_cast<i128>(root) * root * root == value;
}

i64 sum_of_squares_modulo(i64 limit) {
    i128 first = limit;
    i128 second = limit + 1;
    i128 third = 2 * static_cast<i128>(limit) + 1;
    if (first % 2 == 0) {
        first /= 2;
    } else {
        second /= 2;
    }
    if (first % 3 == 0) {
        first /= 3;
    } else if (second % 3 == 0) {
        second /= 3;
    } else {
        third /= 3;
    }
    return static_cast<i64>(
        (first % MODULUS)
        * (second % MODULUS)
        % MODULUS
        * (third % MODULUS)
        % MODULUS
    );
}

i64 nested_pair_sum(i64 limit) {
    const i64 radius = fourth_root_ceiling(limit);
    const i64 coordinate_bound = 2 * radius;
    i64 result = 0;

    // If beta^2 cancels 2*alpha*gamma in the square of three
    // cube roots, their integer radicands satisfy b^2 = -8ac.
    // Its primitive parametrization gives
    //
    //   x = e^2 p(p+2q)^3,
    //   y = e^2 q(q-4p)^3/4,
    //
    // where gcd(p,q)=1 and e is 1 for even q, otherwise 2.  All
    // remaining solutions are square multiples of this primitive pair.
    for (i64 p = 1; p <= coordinate_bound; ++p) {
        for (i64 q = -coordinate_bound; q <= coordinate_bound; ++q) {
            if (q == 0 || std::gcd(p, std::abs(q)) != 1) {
                continue;
            }

            // Swapping a and c swaps x and y and sends q/p to -2p/q.
            // Retain one of these two equivalent parametrizations.
            const i64 swap_divisor = std::gcd(std::abs(q), 2 * p);
            i64 swapped_p = q / swap_divisor;
            i64 swapped_q = -2 * p / swap_divisor;
            if (swapped_p < 0) {
                swapped_p = -swapped_p;
                swapped_q = -swapped_q;
            }
            if (std::tie(p, q) > std::tie(swapped_p, swapped_q)) {
                continue;
            }

            const i64 first_factor = p + 2 * q;
            const i64 second_factor = q - 4 * p;
            if (first_factor == 0 || second_factor == 0) {
                continue;
            }

            // x/y differs from 4p/q by a rational cube.
            const i64 ratio_divisor = std::gcd(4 * p, std::abs(q));
            if (
                is_cube(4 * p / ratio_divisor)
                && is_cube(std::abs(q) / ratio_divisor)
            ) {
                continue;
            }

            const i64 e_squared = (q % 2 == 0 ? 1 : 4);
            i128 x = (
                static_cast<i128>(e_squared)
                * p * first_factor * first_factor * first_factor
            );
            i128 y_numerator = (
                static_cast<i128>(e_squared)
                * q * second_factor * second_factor * second_factor
            );
            assert(y_numerator % 4 == 0);
            i128 y = y_numerator / 4;
            const i128 absolute_x = x < 0 ? -x : x;
            const i128 absolute_y = y < 0 ? -y : y;
            const i128 largest = std::max(absolute_x, absolute_y);
            if (largest > limit) {
                continue;
            }

            const i64 scale_limit = square_root_floor(
                limit / static_cast<i64>(largest)
            );
            const i64 pair_size_modulo = static_cast<i64>(
                (absolute_x + absolute_y) % MODULUS
            );
            result = (
                result
                + static_cast<i128>(pair_size_modulo)
                    * sum_of_squares_modulo(scale_limit)
            ) % MODULUS;
        }
    }
    return result;
}

}  // namespace

int main(int argc, char** argv) {
    const i64 limit = (
        argc > 1 ? std::stoll(argv[1]) : 1'000'000'000'000'000LL
    );
    std::cout << nested_pair_sum(limit) << '\n';
}
