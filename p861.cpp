#include <algorithm>
#include <cassert>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <vector>

using i64 = std::int64_t;

namespace {

i64 integer_sqrt(i64 value) {
    i64 root = static_cast<i64>(std::sqrt(static_cast<long double>(value)));
    while ((root + 1) <= value / (root + 1)) {
        ++root;
    }
    while (root > value / root) {
        --root;
    }
    return root;
}

class Counter {
public:
    explicit Counter(i64 limit)
        : limit_(limit), root_(static_cast<int>(integer_sqrt(limit))) {
        build_small_sieve();
        build_prime_count_table();
    }

    std::vector<i64> compute_q_values() {
        q_values_.assign(11, 0);
        std::vector<int> used_primes;
        enumerate_powerful(0, 1, 1, used_primes);
        return q_values_;
    }

private:
    i64 limit_;
    int root_;
    std::vector<int> primes_;
    std::vector<int> small_pi_;
    std::vector<i64> prime_table_;
    int small_start_ = 0;
    int table_size_ = 0;
    std::vector<i64> q_values_;

    void build_small_sieve() {
        std::vector<char> is_prime(root_ + 1, true);
        if (root_ >= 0) {
            is_prime[0] = false;
        }
        if (root_ >= 1) {
            is_prime[1] = false;
        }
        for (int prime = 2; 1LL * prime * prime <= root_; ++prime) {
            if (!is_prime[prime]) {
                continue;
            }
            for (int multiple = prime * prime;
                 multiple <= root_;
                 multiple += prime) {
                is_prime[multiple] = false;
            }
        }

        small_pi_.assign(root_ + 1, 0);
        int count = 0;
        for (int value = 0; value <= root_; ++value) {
            if (is_prime[value]) {
                primes_.push_back(value);
                ++count;
            }
            small_pi_[value] = count;
        }
    }

    int table_index(i64 value) const {
        if (value <= small_start_) {
            return table_size_ - static_cast<int>(value);
        }
        return static_cast<int>(limit_ / value) - 1;
    }

    void build_prime_count_table() {
        small_start_ = (limit_ / root_ == root_) ? root_ - 1 : root_;
        table_size_ = root_ + small_start_;
        prime_table_.assign(table_size_, 0);

        for (int index = 0; index < root_; ++index) {
            prime_table_[index] = limit_ / (index + 1) - 1;
        }
        for (int value = 1; value <= small_start_; ++value) {
            prime_table_[table_size_ - value] = value - 1;
        }

        for (int prime : primes_) {
            const i64 prime_square = 1LL * prime * prime;
            if (prime_square > limit_) {
                break;
            }
            const i64 primes_before = prime_table_[table_size_ - (prime - 1)];

            int large_count;
            if (prime_square <= root_) {
                large_count = root_;
            } else {
                large_count = static_cast<int>(
                    std::min<i64>(root_, limit_ / prime_square)
                );
            }

            i64 denominator = prime;
            for (int index = 0; index < large_count; ++index) {
                const i64 quotient = limit_ / denominator;
                prime_table_[index] -= (
                    prime_table_[table_index(quotient)] - primes_before
                );
                denominator += prime;
            }

            if (prime_square <= small_start_) {
                for (int value = small_start_;
                     value >= prime_square;
                     --value) {
                    prime_table_[table_size_ - value] -= (
                        prime_table_[table_size_ - value / prime]
                        - primes_before
                    );
                }
            }
        }
    }

    i64 prime_pi(i64 value) const {
        if (value <= root_) {
            return small_pi_[static_cast<int>(value)];
        }
        // Every large query here is floor(limit_ / d), so it has a direct
        // entry in the hyperbola table.
        return prime_table_[static_cast<int>(limit_ / value) - 1];
    }

    static bool contains(
        const std::vector<int>& values,
        int target
    ) {
        return std::find(values.begin(), values.end(), target) != values.end();
    }

    i64 count_squarefree(
        i64 bound,
        int factors_left,
        int start_index,
        const std::vector<int>& forbidden
    ) const {
        if (factors_left == 0) {
            return 1;
        }
        if (start_index >= static_cast<int>(primes_.size())) {
            return 0;
        }

        if (factors_left == 1) {
            const int first_prime = primes_[start_index];
            if (bound < first_prime) {
                return 0;
            }
            i64 result = prime_pi(bound);
            if (start_index > 0) {
                result -= small_pi_[primes_[start_index - 1]];
            }
            for (int prime : forbidden) {
                if (first_prime <= prime && prime <= bound) {
                    --result;
                }
            }
            return result;
        }

        i64 result = 0;
        if (factors_left == 2) {
            for (int index = start_index;
                 index < static_cast<int>(primes_.size());
                 ++index) {
                const i64 prime = primes_[index];
                if (prime > bound / prime) {
                    break;
                }
                if (contains(forbidden, static_cast<int>(prime))) {
                    continue;
                }
                const i64 upper = bound / prime;
                i64 choices = prime_pi(upper) - small_pi_[prime];
                for (int excluded : forbidden) {
                    if (prime < excluded && excluded <= upper) {
                        --choices;
                    }
                }
                result += choices;
            }
            return result;
        }

        for (int index = start_index;
             index < static_cast<int>(primes_.size());
             ++index) {
            const i64 prime = primes_[index];
            i64 minimum_product = 1;
            bool too_large = false;
            for (int count = 0; count < factors_left; ++count) {
                if (minimum_product > bound / prime) {
                    too_large = true;
                    break;
                }
                minimum_product *= prime;
            }
            if (too_large) {
                break;
            }
            if (contains(forbidden, static_cast<int>(prime))) {
                continue;
            }
            result += count_squarefree(
                bound / prime,
                factors_left - 1,
                index + 1,
                forbidden
            );
        }
        return result;
    }

    void process_powerful(
        i64 powerful,
        int divisor_count,
        const std::vector<int>& used_primes
    ) {
        const i64 bound = limit_ / powerful;
        for (int squarefree_factors = 0;
             squarefree_factors <= 4;
             ++squarefree_factors) {
            const int total_divisors = divisor_count << squarefree_factors;
            if (total_divisors > 20) {
                break;
            }
            if (total_divisors >= 4) {
                const int k = total_divisors / 2;
                q_values_[k] += count_squarefree(
                    bound,
                    squarefree_factors,
                    0,
                    used_primes
                );
            }
        }
    }

    void enumerate_powerful(
        int start_index,
        i64 powerful,
        int divisor_count,
        std::vector<int>& used_primes
    ) {
        process_powerful(powerful, divisor_count, used_primes);

        for (int index = start_index;
             index < static_cast<int>(primes_.size());
             ++index) {
            const i64 prime = primes_[index];
            if (powerful > limit_ / prime / prime) {
                break;
            }

            const i64 remaining = limit_ / powerful;
            i64 prime_power = prime * prime;
            for (int exponent = 2;
                 exponent <= 20 && prime_power <= remaining;
                 ++exponent) {
                const int local_count = (
                    exponent % 2 == 0 ? exponent : exponent + 1
                );
                const int next_count = divisor_count * local_count;
                if (next_count <= 20) {
                    used_primes.push_back(static_cast<int>(prime));
                    enumerate_powerful(
                        index + 1,
                        powerful * prime_power,
                        next_count,
                        used_primes
                    );
                    used_primes.pop_back();
                }
                if (prime_power > remaining / prime) {
                    break;
                }
                prime_power *= prime;
            }
        }
    }
};

std::vector<i64> q_values(i64 limit) {
    Counter counter(limit);
    return counter.compute_q_values();
}

i64 solve(i64 limit) {
    const auto values = q_values(limit);
    i64 result = 0;
    for (int k = 2; k <= 10; ++k) {
        result += values[k];
    }
    return result;
}

}  // namespace

int main() {
    assert(q_values(100)[2] == 51);
    assert(q_values(1'000'000)[6] == 6'189);
    std::cout << solve(1'000'000'000'000LL) << '\n';
}
