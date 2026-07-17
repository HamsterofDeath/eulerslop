#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <map>
#include <vector>

using u32 = std::uint32_t;
using u64 = std::uint64_t;

namespace {

constexpr u32 MODULUS = 83'456'729;

std::vector<int> primes_up_to(int limit) {
    std::vector<int> primes;
    for (int candidate = 2; candidate <= limit; ++candidate) {
        bool is_prime = true;
        for (int prime : primes) {
            if (prime * prime > candidate) {
                break;
            }
            if (candidate % prime == 0) {
                is_prime = false;
                break;
            }
        }
        if (is_prime) {
            primes.push_back(candidate);
        }
    }
    return primes;
}

u64 odd_prime_mask(int number, const std::vector<int>& odd_primes) {
    u64 mask = 0;
    for (int index = 0;
         index < static_cast<int>(odd_primes.size());
         ++index) {
        if (number % odd_primes[index] == 0) {
            mask |= 1ULL << index;
        }
    }
    return mask;
}

struct StateSpace {
    std::vector<int> limits;
    std::vector<int> strides;
    std::vector<std::vector<int>> layers;
    std::vector<int> rank;
    std::vector<unsigned char> used;
    int type_count;
    int state_count;

    explicit StateSpace(const std::vector<int>& counts)
        : limits(counts),
          type_count(static_cast<int>(counts.size())) {
        strides.resize(type_count);
        state_count = 1;
        int item_count = 0;
        for (int type = 0; type < type_count; ++type) {
            strides[type] = state_count;
            state_count *= limits[type] + 1;
            item_count += limits[type];
        }

        layers.resize(item_count + 1);
        rank.resize(state_count);
        used.resize(static_cast<std::size_t>(state_count) * type_count);
        for (int code = 0; code < state_count; ++code) {
            int total_used = 0;
            for (int type = 0; type < type_count; ++type) {
                const int count = (
                    code / strides[type] % (limits[type] + 1)
                );
                used[static_cast<std::size_t>(code) * type_count + type] = (
                    static_cast<unsigned char>(count)
                );
                total_used += count;
            }
            rank[code] = static_cast<int>(layers[total_used].size());
            layers[total_used].push_back(code);
        }
    }

    int remaining(int code, int type) const {
        return (
            limits[type]
            - used[static_cast<std::size_t>(code) * type_count + type]
        );
    }
};

u32 coprime_permutations(int limit) {
    std::vector<int> odd_primes;
    for (int prime : primes_up_to(limit / 2)) {
        if (prime != 2) {
            odd_primes.push_back(prime);
        }
    }

    std::map<u64, int> even_groups;
    std::map<u64, int> odd_groups;
    for (int number = 2; number <= limit; ++number) {
        const u64 mask = odd_prime_mask(number, odd_primes);
        if (number % 2 == 0) {
            ++even_groups[mask];
        } else {
            ++odd_groups[mask];
        }
    }

    std::vector<u64> even_masks;
    std::vector<int> even_counts;
    for (const auto& [mask, count] : even_groups) {
        even_masks.push_back(mask);
        even_counts.push_back(count);
    }
    std::vector<u64> odd_masks;
    std::vector<int> odd_counts;
    for (const auto& [mask, count] : odd_groups) {
        odd_masks.push_back(mask);
        odd_counts.push_back(count);
    }

    const int even_total = limit / 2;
    const int odd_total = (limit - 1) - even_total;
    assert(even_total == odd_total + 1);

    const StateSpace even_states(even_counts);
    const StateSpace odd_states(odd_counts);
    const int even_type_count = even_states.type_count;
    const int odd_type_count = odd_states.type_count;

    // A valid path must alternate E-O-E-...-O-E.  At each completed
    // stage the state records all used counts and the type of the last
    // even number.  Multiplying by each remaining count labels the
    // otherwise grouped vertices.
    const int initial_odd_code = 0;
    const int initial_odd_rank = odd_states.rank[initial_odd_code];
    const int initial_even_layer_size = static_cast<int>(
        even_states.layers[1].size()
    );
    std::vector<u32> current(
        static_cast<std::size_t>(initial_even_layer_size)
        * even_type_count
    );
    for (int type = 0; type < even_type_count; ++type) {
        const int code = even_states.strides[type];
        const int rank = even_states.rank[code];
        current[
            (static_cast<std::size_t>(rank) + initial_odd_rank)
            * even_type_count
            + type
        ] = even_counts[type];
    }

    for (int used_even_count = 1;
         used_even_count < even_total;
         ++used_even_count) {
        const auto& even_layer = even_states.layers[used_even_count];
        const auto& odd_layer = odd_states.layers[used_even_count - 1];
        const auto& next_even_layer = even_states.layers[
            used_even_count + 1
        ];
        const auto& next_odd_layer = odd_states.layers[used_even_count];
        const int odd_layer_size = static_cast<int>(odd_layer.size());
        const int next_odd_layer_size = static_cast<int>(
            next_odd_layer.size()
        );

        std::vector<u32> next(
            static_cast<std::size_t>(next_even_layer.size())
            * next_odd_layer_size
            * even_type_count
        );

        for (int even_rank = 0;
             even_rank < static_cast<int>(even_layer.size());
             ++even_rank) {
            const int even_code = even_layer[even_rank];
            for (int odd_rank = 0;
                 odd_rank < odd_layer_size;
                 ++odd_rank) {
                const int odd_code = odd_layer[odd_rank];
                const std::size_t current_offset = (
                    (
                        static_cast<std::size_t>(even_rank)
                        * odd_layer_size
                        + odd_rank
                    )
                    * even_type_count
                );

                bool nonzero = false;
                for (int last = 0; last < even_type_count; ++last) {
                    nonzero |= current[current_offset + last] != 0;
                }
                if (!nonzero) {
                    continue;
                }

                for (int odd_type = 0;
                     odd_type < odd_type_count;
                     ++odd_type) {
                    const int remaining_odd = odd_states.remaining(
                        odd_code,
                        odd_type
                    );
                    if (remaining_odd == 0) {
                        continue;
                    }

                    u64 ways_to_odd = 0;
                    for (int last = 0; last < even_type_count; ++last) {
                        if (
                            (even_masks[last] & odd_masks[odd_type]) == 0
                        ) {
                            ways_to_odd += current[current_offset + last];
                        }
                    }
                    ways_to_odd = (
                        ways_to_odd % MODULUS * remaining_odd
                    ) % MODULUS;
                    if (ways_to_odd == 0) {
                        continue;
                    }

                    const int next_odd_code = (
                        odd_code + odd_states.strides[odd_type]
                    );
                    const int next_odd_rank = odd_states.rank[next_odd_code];
                    for (int next_even_type = 0;
                         next_even_type < even_type_count;
                         ++next_even_type) {
                        if (
                            (odd_masks[odd_type]
                             & even_masks[next_even_type]) != 0
                        ) {
                            continue;
                        }
                        const int remaining_even = even_states.remaining(
                            even_code,
                            next_even_type
                        );
                        if (remaining_even == 0) {
                            continue;
                        }

                        const int next_even_code = (
                            even_code
                            + even_states.strides[next_even_type]
                        );
                        const int next_even_rank = even_states.rank[
                            next_even_code
                        ];
                        const std::size_t next_index = (
                            (
                                static_cast<std::size_t>(next_even_rank)
                                * next_odd_layer_size
                                + next_odd_rank
                            )
                            * even_type_count
                            + next_even_type
                        );
                        next[next_index] = static_cast<u32>(
                            (
                                next[next_index]
                                + ways_to_odd * remaining_even
                            )
                            % MODULUS
                        );
                    }
                }
            }
        }
        current.swap(next);
    }

    u64 result = 0;
    for (u32 ways : current) {
        result += ways;
    }
    return static_cast<u32>(result % MODULUS);
}

}  // namespace

int main(int argc, char** argv) {
    const int limit = argc > 1 ? std::stoi(argv[1]) : 34;
    std::cout << coprime_permutations(limit) << '\n';
}
