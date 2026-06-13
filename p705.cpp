#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>

namespace {

constexpr int MOD = 1'000'000'007;
constexpr int DEFAULT_LIMIT = 100'000'000;

struct Block {
    int mult = 1;
    int constant = 0;
    std::array<int, 10> add{};
    std::array<int, 10> linear{};
};

std::int64_t mod_pow(std::int64_t base, std::int64_t exponent) {
    std::int64_t result = 1;
    while (exponent > 0) {
        if (exponent & 1) {
            result = result * base % MOD;
        }
        base = base * base % MOD;
        exponent >>= 1;
    }
    return result;
}

std::array<std::vector<int>, 10> digit_divisors() {
    std::array<std::vector<int>, 10> divisors;
    for (int digit = 1; digit <= 9; ++digit) {
        for (int candidate = 1; candidate <= digit; ++candidate) {
            if (digit % candidate == 0) {
                divisors[digit].push_back(candidate);
            }
        }
    }
    return divisors;
}

std::array<Block, 10000> build_blocks() {
    const auto divisors = digit_divisors();
    std::array<int, 10> tau{};
    std::array<int, 10> inv_tau{};
    std::array<std::array<int, 10>, 10> inversions{};
    std::array<std::array<int, 10>, 10> row_add{};

    for (int digit = 1; digit <= 9; ++digit) {
        tau[digit] = static_cast<int>(divisors[digit].size());
        inv_tau[digit] = static_cast<int>(mod_pow(tau[digit], MOD - 2));
    }

    for (int left = 1; left <= 9; ++left) {
        for (int right = 1; right <= 9; ++right) {
            int count = 0;
            for (int a : divisors[left]) {
                for (int b : divisors[right]) {
                    if (a > b) {
                        ++count;
                    }
                }
            }
            inversions[left][right] = count;
        }
    }

    for (int digit = 1; digit <= 9; ++digit) {
        for (int target = 1; target <= 9; ++target) {
            row_add[digit][target] =
                static_cast<int>(static_cast<std::int64_t>(inv_tau[digit]) * inversions[digit][target] % MOD);
        }
    }

    std::array<Block, 10000> blocks;
    for (int value = 0; value < 10000; ++value) {
        Block block;
        const int digits[4] = {value / 1000, value / 100 % 10, value / 10 % 10, value % 10};
        for (int digit : digits) {
            if (digit == 0) {
                continue;
            }

            const int old_mult = block.mult;
            block.mult = static_cast<int>(static_cast<std::int64_t>(block.mult) * tau[digit] % MOD);
            for (int target = 1; target <= 9; ++target) {
                block.linear[target] =
                    static_cast<int>(static_cast<std::int64_t>(block.linear[target]) * tau[digit] % MOD);
            }
            block.linear[digit] += old_mult;
            if (block.linear[digit] >= MOD) {
                block.linear[digit] -= MOD;
            }
            block.constant =
                static_cast<int>((static_cast<std::int64_t>(block.constant) * tau[digit] +
                                  static_cast<std::int64_t>(old_mult) * block.add[digit]) %
                                 MOD);
            for (int target = 1; target <= 9; ++target) {
                block.add[target] += row_add[digit][target];
                if (block.add[target] >= MOD) {
                    block.add[target] -= MOD;
                }
            }
        }
        blocks[value] = block;
    }
    return blocks;
}

class Solver {
  public:
    explicit Solver(int limit) : limit_(limit), blocks_(build_blocks()) {}

    int run() {
        if (limit_ > 2) {
            apply_prime(2);
        }

        const int size = limit_ > 3 ? (limit_ - 2) / 2 : 0;
        std::vector<std::uint8_t> sieve(size, 1);
        for (int index = 0; index < size; ++index) {
            if (!sieve[index]) {
                continue;
            }
            const std::int64_t prime = 2LL * index + 3;
            if (prime * prime >= limit_) {
                break;
            }
            const std::int64_t start = (prime * prime - 3) / 2;
            for (std::int64_t composite = start; composite < size; composite += prime) {
                sieve[static_cast<std::size_t>(composite)] = 0;
            }
        }

        for (int index = 0; index < size; ++index) {
            if (sieve[index]) {
                apply_prime(2 * index + 3);
            }
        }

        return static_cast<int>(sum_);
    }

  private:
    void apply_block(const Block& block) {
        std::int64_t dot = block.constant;
        for (int digit = 1; digit <= 9; ++digit) {
            dot += static_cast<std::int64_t>(block.linear[digit]) * weighted_counts_[digit];
        }
        dot %= MOD;

        sum_ = (static_cast<std::int64_t>(block.mult) * sum_ + total_sequences_ * dot) % MOD;
        total_sequences_ = total_sequences_ * block.mult % MOD;
        for (int digit = 1; digit <= 9; ++digit) {
            weighted_counts_[digit] += block.add[digit];
            if (weighted_counts_[digit] >= MOD) {
                weighted_counts_[digit] -= MOD;
            }
        }
    }

    void apply_prime(int prime) {
        const int high = prime / 10000;
        if (high != 0) {
            apply_block(blocks_[high]);
        }
        apply_block(blocks_[prime % 10000]);
    }

    int limit_;
    std::array<Block, 10000> blocks_;
    std::int64_t sum_ = 0;
    std::int64_t total_sequences_ = 1;
    std::array<int, 10> weighted_counts_{};
};

}  // namespace

int main(int argc, char** argv) {
    const int limit = argc > 1 ? std::atoi(argv[1]) : DEFAULT_LIMIT;
    Solver solver(limit);
    std::cout << solver.run() << '\n';
    return 0;
}
