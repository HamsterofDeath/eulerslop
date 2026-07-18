#include <algorithm>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <vector>

using u64 = std::uint64_t;
using i64 = std::int64_t;

constexpr int MODULUS = 715'827'883;

int modular_difference(int left, int right) {
  int result = left - right;
  if (result < 0) {
    result += MODULUS;
  }
  return result;
}

int triangular(u64 value) {
  u64 left = value;
  u64 right = value + 1;
  if ((left & 1) == 0) {
    left /= 2;
  } else {
    right /= 2;
  }
  return static_cast<int>(
      (left % MODULUS) * (right % MODULUS) % MODULUS
  );
}

class PrimeSummatorySieve {
 public:
  explicit PrimeSummatorySieve(u64 limit)
      : limit_(limit), root_(integer_square_root(limit)) {
    values_.reserve(2 * root_);
    for (u64 left = 1; left <= limit_;) {
      const u64 quotient = limit_ / left;
      const u64 right = limit_ / quotient;
      values_.push_back(quotient);
      left = right + 1;
    }

    prime_counts_.resize(values_.size());
    prime_sums_.resize(values_.size());
    for (std::size_t index = 0; index < values_.size(); ++index) {
      prime_counts_[index] = values_[index] - 1;
      prime_sums_[index] =
          modular_difference(triangular(values_[index]), 1);
    }

    sieve();
  }

  u64 prime_count(u64 value) const {
    if (value < 2) {
      return 0;
    }
    return prime_counts_[index_of(value)];
  }

  int prime_sum(u64 value) const {
    if (value < 2) {
      return 0;
    }
    return prime_sums_[index_of(value)];
  }

  const std::vector<int>& small_primes() const {
    return primes_;
  }

 private:
  u64 limit_;
  u64 root_;
  std::vector<u64> values_;
  std::vector<u64> prime_counts_;
  std::vector<int> prime_sums_;
  std::vector<int> primes_;

  static u64 integer_square_root(u64 value) {
    u64 root = static_cast<u64>(
        std::sqrt(static_cast<long double>(value))
    );
    while ((root + 1) <= value / (root + 1)) {
      ++root;
    }
    while (root > value / root) {
      --root;
    }
    return root;
  }

  std::size_t index_of(u64 value) const {
    if (value <= root_) {
      return values_.size() - value;
    }
    return limit_ / value - 1;
  }

  void sieve() {
    for (u64 prime = 2; prime <= root_; ++prime) {
      const std::size_t prime_index = index_of(prime);
      const std::size_t previous_index =
          index_of(prime - 1);
      if (
          prime_counts_[prime_index]
          == prime_counts_[previous_index]
      ) {
        continue;
      }
      primes_.push_back(static_cast<int>(prime));

      const u64 count_before =
          prime_counts_[previous_index];
      const int sum_before = prime_sums_[previous_index];
      const u64 square = prime * prime;
      const std::size_t end =
          square <= root_
              ? values_.size() - square + 1
              : limit_ / square;

      for (std::size_t index = 0; index < end; ++index) {
        const u64 rank = index + 1;
        std::size_t quotient_index;
        if (rank * prime <= root_) {
          // floor(floor(N/rank)/p)
          // = floor(N/(rank*p)).
          quotient_index = rank * prime - 1;
        } else {
          const u64 quotient = values_[index] / prime;
          quotient_index = values_.size() - quotient;
        }

        prime_counts_[index] -=
            prime_counts_[quotient_index] - count_before;

        const int sum_difference = modular_difference(
            prime_sums_[quotient_index],
            sum_before
        );
        const int removed = static_cast<int>(
            (prime % MODULUS)
            * static_cast<i64>(sum_difference)
            % MODULUS
        );
        prime_sums_[index] = modular_difference(
            prime_sums_[index],
            removed
        );
      }
    }
  }
};

int total_graph_weight(u64 limit) {
  const PrimeSummatorySieve prime_sums(limit);
  i64 result = 0;

  // The k=1 contribution, grouped by floor(N/p).
  for (u64 left = 2; left <= limit;) {
    const u64 quotient = limit / left;
    const u64 right = limit / quotient;

    const u64 count =
        prime_sums.prime_count(right)
        - prime_sums.prime_count(left - 1);
    const int sum = modular_difference(
        prime_sums.prime_sum(right),
        prime_sums.prime_sum(left - 1)
    );
    const int weighted_sum = modular_difference(
        sum,
        static_cast<int>(2 * (count % MODULUS) % MODULUS)
    );
    result += static_cast<i64>(triangular(quotient))
        * weighted_sum % MODULUS;
    if (result >= MODULUS) {
      result -= MODULUS;
    }
    left = right + 1;
  }

  // Repeated occurrences of p in the lower endpoint contribute the
  // correction for p^2, p^3, ...
  for (const u64 prime : prime_sums.small_primes()) {
    u64 prime_power = prime * prime;
    while (prime_power <= limit) {
      result += (prime - 1)
          * triangular(limit / prime_power)
          % MODULUS;
      if (result >= MODULUS) {
        result -= MODULUS;
      }
      if (prime_power > limit / prime) {
        break;
      }
      prime_power *= prime;
    }
  }

  return static_cast<int>(result);
}

int main(int argc, char** argv) {
  const u64 limit =
      argc > 1 ? std::stoull(argv[1]) : 1'000'000'000'000ULL;

  if (
      total_graph_weight(10) != 26
      || total_graph_weight(100) != 5282
  ) {
    std::cerr << "sample self-check failed\n";
    return 1;
  }
  std::cout << total_graph_weight(limit) << '\n';
}
