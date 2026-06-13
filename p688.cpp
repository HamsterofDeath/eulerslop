#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>

namespace {

using i64 = long long;
using i128 = __int128_t;

constexpr i64 kDefaultN = 10'000'000'000'000'000LL;
constexpr i64 kMod = 1'000'000'007LL;

i64 parse_n(int argc, char** argv) {
    i64 n = kDefaultN;
    for (int i = 1; i < argc; ++i) {
        const std::string arg(argv[i]);
        const std::string prefix = "--n=";
        if (arg.rfind(prefix, 0) != 0) {
            throw std::invalid_argument("unknown argument: " + arg);
        }

        n = 0;
        for (char c : arg.substr(prefix.size())) {
            if (c < '0' || c > '9') {
                throw std::invalid_argument("invalid --n value");
            }
            n = 10 * n + (c - '0');
        }
    }
    return n;
}

i64 max_k(i64 n) {
    i64 lo = 0;
    i64 hi = 1;
    while (static_cast<i128>(hi) * (hi + 1) / 2 <= n) {
        hi *= 2;
    }

    while (lo + 1 < hi) {
        const i64 mid = lo + (hi - lo) / 2;
        if (static_cast<i128>(mid) * (mid + 1) / 2 <= n) {
            lo = mid;
        } else {
            hi = mid;
        }
    }
    return lo;
}

i64 mod_value(i128 value) {
    value %= kMod;
    if (value < 0) {
        value += kMod;
    }
    return static_cast<i64>(value);
}

i64 solve(i64 n) {
    i64 total = 0;
    const i64 limit = max_k(n);

    for (i64 k = 1; k <= limit; ++k) {
        const i128 offset = static_cast<i128>(k) * (k - 1) / 2;
        const i128 q = (static_cast<i128>(n) - offset) / k;

        // For this k, q is the largest possible smallest pile.  Summing the
        // number of n values that admit each minimum m=1..q gives this term.
        const i128 term =
            q * (static_cast<i128>(n) + 1 - offset)
            - static_cast<i128>(k) * q * (q + 1) / 2;
        total += mod_value(term);
        if (total >= kMod) {
            total -= kMod;
        }
    }

    return total;
}

}  // namespace

int main(int argc, char** argv) {
    try {
        std::cout << solve(parse_n(argc, argv)) << '\n';
    } catch (const std::exception& exc) {
        std::cerr << exc.what() << '\n';
        return 1;
    }
}
