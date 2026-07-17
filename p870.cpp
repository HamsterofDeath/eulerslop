#include <cassert>
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <vector>

using u64 = std::uint64_t;
using u128 = __uint128_t;

namespace {

int term_factor = 35;

struct Fraction {
    u64 numerator;
    u64 denominator;
};

struct BigInteger {
    std::vector<u64> limbs;

    explicit BigInteger(u64 value = 0) {
        if (value) {
            limbs.push_back(value);
        }
    }

    bool fits_u64() const {
        return limbs.size() <= 1;
    }

    u64 to_u64() const {
        assert(fits_u64());
        return limbs.empty() ? 0 : limbs[0];
    }
};

BigInteger add(const BigInteger& first, const BigInteger& second) {
    BigInteger result;
    const std::size_t size = std::max(
        first.limbs.size(), second.limbs.size()
    );
    result.limbs.resize(size);
    u128 carry = 0;
    for (std::size_t index = 0; index < size; ++index) {
        const u128 value = carry
            + (index < first.limbs.size() ? first.limbs[index] : 0)
            + (index < second.limbs.size() ? second.limbs[index] : 0);
        result.limbs[index] = static_cast<u64>(value);
        carry = value >> 64;
    }
    if (carry) {
        result.limbs.push_back(static_cast<u64>(carry));
    }
    return result;
}

BigInteger multiply(const BigInteger& value, u64 factor) {
    if (factor == 0 || value.limbs.empty()) {
        return BigInteger();
    }
    BigInteger result;
    result.limbs.resize(value.limbs.size());
    u128 carry = 0;
    for (std::size_t index = 0; index < value.limbs.size(); ++index) {
        const u128 product = (
            static_cast<u128>(value.limbs[index]) * factor + carry
        );
        result.limbs[index] = static_cast<u64>(product);
        carry = product >> 64;
    }
    if (carry) {
        result.limbs.push_back(static_cast<u64>(carry));
    }
    return result;
}

int compare(const BigInteger& first, const BigInteger& second) {
    if (first.limbs.size() != second.limbs.size()) {
        return first.limbs.size() < second.limbs.size() ? -1 : 1;
    }
    for (std::size_t index = first.limbs.size(); index-- > 0;) {
        if (first.limbs[index] != second.limbs[index]) {
            return first.limbs[index] < second.limbs[index] ? -1 : 1;
        }
    }
    return 0;
}

bool scaled_less(
    const BigInteger& first,
    u64 first_factor,
    const BigInteger& second,
    u64 second_factor
) {
    if (first.fits_u64() && second.fits_u64()) {
        return static_cast<u128>(first.to_u64()) * first_factor
            < static_cast<u128>(second.to_u64()) * second_factor;
    }
    return compare(
        multiply(first, first_factor),
        multiply(second, second_factor)
    ) < 0;
}

Fraction next_transition(const Fraction& current) {
    const long double current_value = (
        static_cast<long double>(current.numerator)
        / current.denominator
    );
    // Candidate indices grow roughly linearly with r.  Through the requested
    // transition the last improving candidate occurs below index 2,500;
    // this bound supplies more than 8,000 terms near the final value.  A
    // separate run with a still larger factor gives the identical answer.
    const int term_limit = std::max(
        300,
        static_cast<int>(std::ceil(term_factor * current_value)) + 100
    );

    std::vector<BigInteger> sequence;
    sequence.reserve(term_limit);
    sequence.push_back(BigInteger(1));
    std::size_t summand_index = 0;
    Fraction best{0, 1};

    for (int index = 1; index < term_limit; ++index) {
        const BigInteger& previous = sequence.back();
        while (
            scaled_less(
                sequence[summand_index],
                current.numerator,
                previous,
                current.denominator
            )
        ) {
            ++summand_index;
            assert(summand_index < sequence.size());
        }

        if (summand_index != 0) {
            const BigInteger& denominator = sequence[summand_index - 1];
            const bool exceeds_current = scaled_less(
                denominator,
                current.numerator,
                previous,
                current.denominator
            );
            const bool improves_best = (
                best.numerator == 0
                || scaled_less(
                    previous,
                    best.denominator,
                    denominator,
                    best.numerator
                )
            );
            if (exceeds_current && improves_best) {
                assert(previous.fits_u64() && denominator.fits_u64());
                best = {previous.to_u64(), denominator.to_u64()};
            }
        }
        sequence.push_back(add(previous, sequence[summand_index]));
    }
    assert(best.numerator != 0);
    const u64 divisor = std::gcd(best.numerator, best.denominator);
    best.numerator /= divisor;
    best.denominator /= divisor;
    return best;
}

Fraction transition(int index) {
    Fraction result{1, 1};
    for (int position = 1; position < index; ++position) {
        result = next_transition(result);
    }
    return result;
}

}  // namespace

int main(int argc, char** argv) {
    const int index = argc > 1 ? std::stoi(argv[1]) : 123'456;
    if (argc > 2) {
        term_factor = std::stoi(argv[2]);
    }
    assert(index >= 1);
    assert(term_factor >= 10);
    const Fraction result = transition(index);
    std::cout << std::fixed << std::setprecision(10)
              << static_cast<long double>(result.numerator)
                    / result.denominator
              << '\n';
}
