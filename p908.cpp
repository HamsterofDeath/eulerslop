#include <algorithm>
#include <cstdint>
#include <iostream>
#include <utility>
#include <vector>

using int64 = std::int64_t;

constexpr int64 MODULUS = 1111211113;

class ClockCounter {
 public:
  explicit ClockCounter(int limit) : limit_(limit) {
    build_primes();
    generate_moduli(0, 1, 1);
  }

  int64 count() {
    std::vector<int64> inverse(limit_ + 1);
    std::vector<int64> represented(limit_ + 1);
    inverse[1] = 1;
    for (int value = 2; value <= limit_; ++value) {
      inverse[value] =
          MODULUS
          - (MODULUS / value) * inverse[MODULUS % value]
                % MODULUS;
    }

    // A(p): words represented with a period of exactly p entries.
    for (const auto& [total, required] : moduli_) {
      const int optional = total - required;
      const int maximum_chosen =
          std::min(optional, limit_ - required);
      int64 binomial = 1;

      for (int chosen = 0; chosen <= maximum_chosen; ++chosen) {
        int period = required + chosen;
        represented[period] += binomial;
        if (represented[period] >= MODULUS) {
          represented[period] -= MODULUS;
        }

        if (chosen < maximum_chosen) {
          binomial =
              binomial * (optional - chosen) % MODULUS
              * inverse[chosen + 1] % MODULUS;
        }
      }
    }

    // A(p) = sum_{d|p} B(d), where B(d) has minimal period d.
    std::vector<int64> minimal = represented;
    for (int divisor = 1; divisor <= limit_; ++divisor) {
      for (
          int multiple = 2 * divisor;
          multiple <= limit_;
          multiple += divisor
      ) {
        minimal[multiple] -= minimal[divisor];
        if (minimal[multiple] < 0) {
          minimal[multiple] += MODULUS;
        }
      }
    }

    int64 answer = 0;
    for (int period = 1; period <= limit_; ++period) {
      answer += minimal[period];
      if (answer >= MODULUS) {
        answer -= MODULUS;
      }
    }
    return answer;
  }

 private:
  int limit_;
  std::vector<int> odd_primes_;
  std::vector<std::pair<int, int>> moduli_;

  void build_primes() {
    const int maximum = 2 * limit_;
    std::vector<bool> is_prime(maximum, true);
    is_prime[0] = is_prime[1] = false;

    for (int value = 2; value < maximum; ++value) {
      if (!is_prime[value]) {
        continue;
      }
      if (value != 2) {
        odd_primes_.push_back(value);
      }
      if (static_cast<int64>(value) * value < maximum) {
        for (
            int multiple = value * value;
            multiple < maximum;
            multiple += value
        ) {
          is_prime[multiple] = false;
        }
      }
    }
  }

  void generate_moduli(
      int first_prime,
      int odd_part,
      int odd_residue_count
  ) {
    // Triangular numbers cover every residue modulo a power of two.
    for (
        int power_of_two = 1;
        power_of_two * odd_residue_count <= limit_;
        power_of_two *= 2
    ) {
      moduli_.emplace_back(
          odd_part * power_of_two,
          odd_residue_count * power_of_two
      );
    }

    const int residue_budget = limit_ / odd_residue_count;
    for (
        int prime_index = first_prime;
        prime_index < static_cast<int>(odd_primes_.size());
        ++prime_index
    ) {
      const int64 prime = odd_primes_[prime_index];
      if ((prime + 1) / 2 > residue_budget) {
        break;
      }

      int64 prime_power = 1;
      int64 two_ago = 1;
      int64 previous = (prime + 1) / 2;

      for (int exponent = 1;; ++exponent) {
        prime_power *= prime;
        int64 residue_count;
        if (exponent == 1) {
          residue_count = previous;
        } else {
          const int64 totient =
              prime_power / prime * (prime - 1);
          residue_count = two_ago + totient / 2;
          two_ago = previous;
          previous = residue_count;
        }

        if (residue_count > residue_budget) {
          break;
        }

        generate_moduli(
            prime_index + 1,
            static_cast<int>(odd_part * prime_power),
            static_cast<int>(
                odd_residue_count * residue_count
            )
        );
      }
    }
  }
};

int main(int argc, char** argv) {
  const int limit = argc > 1 ? std::stoi(argv[1]) : 10000;
  std::cout << ClockCounter(limit).count() << '\n';
}
