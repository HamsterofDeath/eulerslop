#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>

using i64 = std::int64_t;

namespace {

constexpr i64 MODULUS = 1'000'000'007;

i64 modular_power(i64 base, i64 exponent) {
    i64 result = 1;
    while (exponent) {
        if (exponent & 1) {
            result = result * base % MODULUS;
        }
        base = base * base % MODULUS;
        exponent >>= 1;
    }
    return result;
}

i64 initial_gap_allocations(i64 a_count, i64 b_count, i64 c_count) {
    const i64 letters = a_count + b_count;
    i64 numerator = 1;
    i64 denominator = 1;
    for (i64 value = 1; value <= letters; ++value) {
        numerator = numerator * ((c_count + value) % MODULUS)
            % MODULUS;
        denominator = denominator * value % MODULUS;
    }
    return numerator * modular_power(denominator, MODULUS - 2)
        % MODULUS;
}

i64 count_words(i64 a_count, i64 b_count, i64 c_count) {
    assert(a_count > 0 && b_count > 0 && c_count >= 0);
    assert(a_count + b_count + c_count < MODULUS);

    const i64 smaller = std::min(a_count, b_count);
    const i64 maximum_transitions = (
        2 * smaller - (a_count == b_count ? 1 : 0)
    );
    const int transition_limit = static_cast<int>(
        std::min(maximum_transitions, c_count / 2)
    );
    if (transition_limit == 0) {
        return 0;
    }

    // Batch-invert N(N-1) for the recurrence
    // C(N-2,K) / C(N,K) = (N-K)(N-K-1) / (N(N-1)).
    const i64 initial_top = a_count + b_count + c_count;
    std::vector<i64> inverse_denominators(transition_limit);
    i64 prefix = 1;
    for (int transition = 1;
         transition <= transition_limit;
         ++transition) {
        const i64 top = initial_top - 2LL * (transition - 1);
        const i64 denominator = top % MODULUS
            * ((top - 1) % MODULUS) % MODULUS;
        prefix = prefix * denominator % MODULUS;
        inverse_denominators[transition - 1] = prefix;
    }
    i64 inverse_prefix = modular_power(prefix, MODULUS - 2);
    for (int transition = transition_limit;
         transition >= 1;
         --transition) {
        const i64 top = initial_top - 2LL * (transition - 1);
        const i64 denominator = top % MODULUS
            * ((top - 1) % MODULUS) % MODULUS;
        const i64 preceding_prefix = (
            transition == 1
            ? 1
            : inverse_denominators[transition - 2]
        );
        inverse_denominators[transition - 1] = (
            inverse_prefix * preceding_prefix % MODULUS
        );
        inverse_prefix = inverse_prefix * denominator % MODULUS;
    }

    std::vector<i64> inverses(smaller + 1);
    inverses[1] = 1;
    for (i64 value = 2; value <= smaller; ++value) {
        inverses[value] = (
            MODULUS
            - (MODULUS / value) * inverses[MODULUS % value] % MODULUS
        );
    }

    i64 gap_allocations = initial_gap_allocations(
        a_count, b_count, c_count
    );
    int current_transition = 0;
    i64 result = 0;

    const auto advance_gap_allocations = [&]() {
        const i64 remaining_c = (
            c_count - 2LL * current_transition
        ) % MODULUS;
        gap_allocations = gap_allocations
            * remaining_c % MODULUS
            * ((remaining_c - 1 + MODULUS) % MODULUS) % MODULUS
            * inverse_denominators[current_transition] % MODULUS;
        ++current_transition;
    };

    // At s alternating runs of each letter there are
    // 2*C(p-1,s-1)*C(q-1,s-1) skeletons (an odd number of
    // transitions).  With one extra run on either side, the corresponding
    // two products give the even-transition skeletons.
    i64 choose_a = 1;  // C(a_count - 1, s - 1)
    i64 choose_b = 1;  // C(b_count - 1, s - 1)
    for (i64 runs = 1; runs <= smaller; ++runs) {
        if (current_transition < transition_limit) {
            advance_gap_allocations();
            const i64 skeletons = 2 * choose_a % MODULUS
                * choose_b % MODULUS;
            result = (
                result + skeletons * gap_allocations
            ) % MODULUS;
        }

        const i64 next_choose_a = choose_a
            * ((a_count - runs) % MODULUS) % MODULUS
            * inverses[runs] % MODULUS;
        const i64 next_choose_b = choose_b
            * ((b_count - runs) % MODULUS) % MODULUS
            * inverses[runs] % MODULUS;

        if (current_transition < transition_limit) {
            advance_gap_allocations();
            const i64 skeletons = (
                next_choose_a * choose_b
                + choose_a * next_choose_b
            ) % MODULUS;
            result = (
                result + skeletons * gap_allocations
            ) % MODULUS;
        }
        choose_a = next_choose_a;
        choose_b = next_choose_b;
    }
    assert(current_transition == transition_limit);
    return result;
}

}  // namespace

int main(int argc, char** argv) {
    const i64 a_count = argc > 1 ? std::stoll(argv[1]) : 1'000'000;
    const i64 b_count = argc > 2 ? std::stoll(argv[2]) : 10'000'000;
    const i64 c_count = argc > 3 ? std::stoll(argv[3]) : 100'000'000;
    std::cout << count_words(a_count, b_count, c_count) << '\n';
}
