#include <cassert>
#include <cstdint>
#include <iostream>

using u64 = std::uint64_t;

namespace {

u64 xor_product(u64 left, u64 right) {
    u64 result = 0;
    while (right != 0) {
        if ((right & 1U) != 0) {
            result ^= left;
        }
        left <<= 1;
        right >>= 1;
    }
    return result;
}

u64 quadratic_form(u64 a, u64 b) {
    return (
        xor_product(a, a)
        ^ (xor_product(a, b) << 1)
        ^ xor_product(b, b)
    );
}

u64 count_solutions(u64 number_limit, u64 value_limit) {
    assert(value_limit > 0);
    const int bit_length = 64 - __builtin_clzll(value_limit);

    // For a canonical pair, deg(Q) >= 2*deg(b)-1.  Consequently every
    // orbit representative is below this small limit (2048 for the
    // requested value_limit).
    const u64 seed_limit = 1ULL << (bit_length / 2 + 1);

    u64 result = 0;
    for (u64 b = 0; b < seed_limit; ++b) {
        for (u64 a = 0; a <= b; ++a) {
            const u64 predecessor = b ^ (a << 1);

            // Q is invariant under (a,b) -> (b,a+2b), where + is XOR.
            // Apart from the fixed zero pair, take the unique member of
            // each orbit whose ordered predecessor is not smaller.
            if (
                (a != 0 || b != 0)
                && predecessor <= a
            ) {
                continue;
            }
            if (quadratic_form(a, b) > value_limit) {
                continue;
            }

            u64 first = a;
            u64 second = b;
            while (second <= number_limit) {
                ++result;
                if (first == 0 && second == 0) {
                    break;
                }
                const u64 next = first ^ (second << 1);
                first = second;
                second = next;
            }
        }
    }
    return result;
}

}  // namespace

int main(int argc, char** argv) {
    const u64 number_limit = (
        argc > 1 ? std::stoull(argv[1]) : 100'000'000'000'000'000ULL
    );
    const u64 value_limit = (
        argc > 2 ? std::stoull(argv[2]) : 1'000'000ULL
    );
    std::cout << count_solutions(number_limit, value_limit) << '\n';
}
