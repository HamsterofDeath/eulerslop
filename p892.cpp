#include <cstdint>
#include <iostream>
#include <string>
#include <vector>

using u64 = std::uint64_t;

namespace {

constexpr u64 MODULUS = 1'234'567'891;

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

u64 central_binomial(int index, const std::vector<u64>& inverse) {
    u64 value = 1;
    for (int current = 1; current <= index; ++current) {
        value = (
            value
            * (2 * static_cast<u64>(2 * current - 1) % MODULUS)
            % MODULUS
            * inverse[current]
            % MODULUS
        );
    }
    return value;
}

u64 cutting_imbalance_sum(int edge_count) {
    if (edge_count <= 1) {
        return 0;
    }
    const int half = edge_count / 2;
    const auto inverse = inverse_table(half + 1);
    const u64 central = central_binomial(half, inverse);
    const u64 square = central * central % MODULUS;

    if (edge_count % 2 == 0) {
        return square * ((MODULUS + 1) / 2) % MODULUS;
    }
    return (
        square
        * (2 * static_cast<u64>(half) % MODULUS)
        % MODULUS
        * inverse[half + 1]
        % MODULUS
    );
}

u64 summatory_cutting_imbalance(int limit) {
    const int maximum_half = limit / 2;
    const auto inverse = inverse_table(maximum_half + 1);
    const u64 inverse_two = (MODULUS + 1) / 2;

    u64 result = 0;
    u64 central = 1;
    for (int half = 1; half <= maximum_half; ++half) {
        central = (
            central
            * (2 * static_cast<u64>(2 * half - 1) % MODULUS)
            % MODULUS
            * inverse[half]
            % MODULUS
        );
        const u64 square = central * central % MODULUS;

        // D(2m) = C(2m,m)^2 / 2.
        result += square * inverse_two % MODULUS;
        result %= MODULUS;

        // D(2m+1) = 2m*C(2m,m)^2/(m+1).
        if (2 * half + 1 <= limit) {
            result += (
                square
                * (2 * static_cast<u64>(half) % MODULUS)
                % MODULUS
                * inverse[half + 1]
                % MODULUS
            );
            result %= MODULUS;
        }
    }
    return result;
}

}  // namespace

int main(int argc, char** argv) {
    const int limit = argc > 1 ? std::stoi(argv[1]) : 10'000'000;
    if (argc > 2 && std::string(argv[2]) == "single") {
        std::cout << cutting_imbalance_sum(limit) << '\n';
    } else {
        std::cout << summatory_cutting_imbalance(limit) << '\n';
    }
}
