#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>

using u64 = std::uint64_t;

namespace {

constexpr u64 MODULUS = 912'491'249;
constexpr int PERIOD = 11'060;
constexpr int FIRST_REPEATED_INDEX = 11'382;
constexpr int PERIOD_BLOCK_START = FIRST_REPEATED_INDEX - PERIOD;
constexpr int VERIFICATION_LIMIT = 2 * FIRST_REPEATED_INDEX;

std::vector<unsigned char> verified_grundy_prefix() {
    std::vector<unsigned char> grundy(VERIFICATION_LIMIT + 1);
    for (int stones = 1; stones <= VERIFICATION_LIMIT; ++stones) {
        unsigned int reached = 0;
        for (int left = 1; left * 2 <= stones; ++left) {
            reached |= 1U << (
                grundy[left] ^ grundy[stones - left]
            );
        }
        for (int removed : {1, 2, 4, 9}) {
            if (removed <= stones) {
                reached |= 1U << grundy[stones - removed];
            }
        }

        int value = 0;
        while (((reached >> value) & 1U) != 0) {
            ++value;
        }
        grundy[stones] = static_cast<unsigned char>(value);
    }

    for (int stones = FIRST_REPEATED_INDEX;
         stones <= VERIFICATION_LIMIT;
         ++stones) {
        assert(grundy[stones] == grundy[stones - PERIOD]);
    }

    // The checked interval proves continuation by induction.  For a
    // sufficiently large split a+b=n, at least one part can be reduced
    // by PERIOD while staying inside the periodic range; the reverse
    // map adds PERIOD.  Removal followers map directly as well.
    return grundy;
}

std::array<u64, 16> grundy_frequencies(
    u64 limit,
    const std::vector<unsigned char>& grundy
) {
    std::array<u64, 16> result{};
    if (limit < PERIOD_BLOCK_START) {
        for (u64 stones = 1; stones <= limit; ++stones) {
            ++result[grundy[stones]];
        }
        return result;
    }

    for (int stones = 1; stones < PERIOD_BLOCK_START; ++stones) {
        ++result[grundy[stones]];
    }

    const u64 periodic_length = limit - PERIOD_BLOCK_START + 1;
    const u64 complete_periods = periodic_length / PERIOD;
    const int remainder = static_cast<int>(periodic_length % PERIOD);
    std::array<u64, 16> period_frequency{};
    for (int offset = 0; offset < PERIOD; ++offset) {
        ++period_frequency[grundy[PERIOD_BLOCK_START + offset]];
    }
    for (int value = 0; value < 16; ++value) {
        result[value] += complete_periods * period_frequency[value];
    }
    for (int offset = 0; offset < remainder; ++offset) {
        ++result[grundy[PERIOD_BLOCK_START + offset]];
    }
    return result;
}

std::vector<u64> inverse_table(int limit) {
    std::vector<u64> inverse(limit + 1);
    inverse[1] = 1;
    for (int value = 2; value <= limit; ++value) {
        inverse[value] = (
            MODULUS
            - (MODULUS / value) * inverse[MODULUS % value] % MODULUS
        );
    }
    return inverse;
}

std::vector<u64> multiset_coefficients(
    u64 choice_count,
    int maximum_size,
    const std::vector<u64>& inverse
) {
    std::vector<u64> coefficients(maximum_size + 1);
    coefficients[0] = 1;
    if (choice_count == 0) {
        return coefficients;
    }
    for (int size = 1; size <= maximum_size; ++size) {
        coefficients[size] = (
            coefficients[size - 1]
            * ((choice_count + size - 1) % MODULUS)
            % MODULUS
            * inverse[size]
            % MODULUS
        );
    }
    return coefficients;
}

u64 losing_positions(
    u64 pile_limit,
    int pile_count,
    const std::vector<unsigned char>& grundy
) {
    const auto frequency = grundy_frequencies(pile_limit, grundy);
    const auto inverse = inverse_table(pile_count);

    // The pile nim-values lie in the four-bit XOR group.  A Walsh
    // character turns the multiset generating function into
    //
    //   (1-t)^(-positive) (1+t)^(-negative).
    //
    // Averaging its t^m coefficient over all 16 characters extracts
    // total XOR zero.
    u64 character_sum = 0;
    for (int character = 0; character < 16; ++character) {
        u64 positive = 0;
        for (int value = 0; value < 16; ++value) {
            if (__builtin_popcount(character & value) % 2 == 0) {
                positive += frequency[value];
            }
        }
        const u64 negative = pile_limit - positive;
        const auto positive_coefficients = multiset_coefficients(
            positive,
            pile_count,
            inverse
        );
        const auto negative_coefficients = multiset_coefficients(
            negative,
            pile_count,
            inverse
        );

        u64 coefficient = 0;
        for (int negative_size = 0;
             negative_size <= pile_count;
             ++negative_size) {
            const u64 term = (
                negative_coefficients[negative_size]
                * positive_coefficients[pile_count - negative_size]
                % MODULUS
            );
            if (negative_size % 2 == 0) {
                coefficient += term;
                if (coefficient >= MODULUS) {
                    coefficient -= MODULUS;
                }
            } else {
                coefficient = (
                    coefficient >= term
                    ? coefficient - term
                    : coefficient + MODULUS - term
                );
            }
        }
        character_sum += coefficient;
        character_sum %= MODULUS;
    }

    return character_sum * inverse_table(16)[16] % MODULUS;
}

}  // namespace

int main(int argc, char** argv) {
    const u64 pile_limit = (
        argc > 1 ? std::stoull(argv[1]) : 12'491'249ULL
    );
    const int pile_count = argc > 2 ? std::stoi(argv[2]) : 1'249;
    const auto grundy = verified_grundy_prefix();
    std::cout << losing_positions(pile_limit, pile_count, grundy) << '\n';
}
