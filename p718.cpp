#include <cstdint>
#include <exception>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

using i64 = long long;
using i128 = __int128_t;

constexpr i64 kDefaultP = 6;
constexpr i64 kMod = 1'000'000'007LL;

i64 mod_value(i128 value) {
    value %= kMod;
    if (value < 0) {
        value += kMod;
    }
    return static_cast<i64>(value);
}

i64 checked_pow(i64 base, i64 exp) {
    i128 result = 1;
    for (i64 i = 0; i < exp; ++i) {
        result *= base;
        if (result > static_cast<i128>(INT64_MAX)) {
            throw std::overflow_error("power does not fit in int64");
        }
    }
    return static_cast<i64>(result);
}

i64 extended_gcd(i64 a, i64 b, i64& x, i64& y) {
    if (b == 0) {
        x = 1;
        y = 0;
        return a;
    }

    i64 x1 = 0;
    i64 y1 = 0;
    const i64 g = extended_gcd(b, a % b, x1, y1);
    x = y1;
    y = x1 - (a / b) * y1;
    return g;
}

i64 inverse_mod(i64 value, i64 modulus) {
    i64 x = 0;
    i64 y = 0;
    const i64 g = extended_gcd(value, modulus, x, y);
    if (g != 1) {
        throw std::invalid_argument("inverse does not exist");
    }

    x %= modulus;
    if (x < 0) {
        x += modulus;
    }
    return x;
}

i64 parse_p(int argc, char** argv) {
    i64 p = kDefaultP;
    for (int i = 1; i < argc; ++i) {
        const std::string arg(argv[i]);
        const std::string prefix = "--p=";
        if (arg.rfind(prefix, 0) != 0) {
            throw std::invalid_argument("unknown argument: " + arg);
        }

        p = 0;
        for (char c : arg.substr(prefix.size())) {
            if (c < '0' || c > '9') {
                throw std::invalid_argument("invalid --p value");
            }
            p = 10 * p + (c - '0');
        }
        if (p <= 0) {
            throw std::invalid_argument("--p must be positive");
        }
    }
    return p;
}

i64 solve(i64 p) {
    const i64 a = checked_pow(17, p);
    const i64 b = checked_pow(19, p);
    const i64 c = checked_pow(23, p);
    const i64 start = a + b + c;

    const i64 inverse_c = inverse_mod(c % a, a);
    const i64 step = static_cast<i64>((static_cast<i128>(b % a) * inverse_c) % a);
    const i64 cycle = b * a;

    std::vector<i64> suffix_min(static_cast<std::size_t>(a));

    i64 z = static_cast<i64>((static_cast<i128>(a - 1) * step) % a);
    i64 best = c * z - b * (a - 1);
    for (i64 x = a - 1; x >= 0; --x) {
        const i64 h = c * z - b * x;
        if (h < best) {
            best = h;
        }
        suffix_min[static_cast<std::size_t>(x)] = best;

        if (x > 0) {
            if (z < step) {
                z += a;
            }
            z -= step;
        }
    }

    i64 total = mod_value(static_cast<i128>(start) * (start - 1) / 2);
    i64 prefix_min = 0;
    z = 0;
    for (i64 x = 0; x < a; ++x) {
        const i64 h = c * z - b * x;
        if (x == 0 || h < prefix_min) {
            prefix_min = h;
        }

        i64 best_h = prefix_min;
        if (x + 1 < a) {
            const i64 wrapped = cycle + suffix_min[static_cast<std::size_t>(x + 1)];
            if (wrapped < best_h) {
                best_h = wrapped;
            }
        }

        const i64 apery_value = b * x + best_h;
        const i64 residue = apery_value % a;
        const i64 gap_count = (apery_value - residue) / a;
        const i128 gap_sum =
            static_cast<i128>(gap_count) * residue
            + static_cast<i128>(a) * gap_count * (gap_count - 1) / 2;
        const i128 shifted_sum =
            static_cast<i128>(gap_count) * start + gap_sum;

        total += mod_value(shifted_sum);
        if (total >= kMod) {
            total -= kMod;
        }

        z += step;
        if (z >= a) {
            z -= a;
        }
    }

    return total;
}

}  // namespace

int main(int argc, char** argv) {
    try {
        std::cout << solve(parse_p(argc, argv)) << '\n';
    } catch (const std::exception& exc) {
        std::cerr << exc.what() << '\n';
        return 1;
    }
}
