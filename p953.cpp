#include <cmath>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using u64 = std::uint64_t;
using u128 = unsigned __int128;

constexpr u64 TARGET_LIMIT = 100'000'000'000'000ULL;
constexpr u64 MODULUS = 1'000'000'007ULL;
constexpr u64 INVERSE_SIX = 166'666'668ULL;

u64 integer_sqrt(u64 value) {
  u64 root = static_cast<u64>(std::sqrt(
      static_cast<long double>(value)
  ));
  while (static_cast<u128>(root + 1) * (root + 1) <= value) {
    ++root;
  }
  while (static_cast<u128>(root) * root > value) {
    --root;
  }
  return root;
}

u64 sum_of_squares(u64 maximum) {
  const u64 first = maximum % MODULUS;
  const u64 second = (maximum + 1) % MODULUS;
  const u64 third = (2 * maximum + 1) % MODULUS;
  return first * second % MODULUS
         * third % MODULUS
         * INVERSE_SIX % MODULUS;
}

struct PrimeTable {
  std::vector<unsigned char> is_prime;
  std::vector<int> primes;
};

PrimeTable prime_table(int limit) {
  PrimeTable table;
  table.is_prime.assign(limit + 1, 1);
  table.is_prime[0] = table.is_prime[1] = 0;

  for (
      int prime = 2;
      static_cast<std::int64_t>(prime) * prime <= limit;
      ++prime
  ) {
    if (!table.is_prime[prime]) {
      continue;
    }
    for (
        std::int64_t multiple =
            static_cast<std::int64_t>(prime) * prime;
        multiple <= limit;
        multiple += prime
    ) {
      table.is_prime[multiple] = 0;
    }
  }

  for (int value = 2; value <= limit; ++value) {
    if (table.is_prime[value]) {
      table.primes.push_back(value);
    }
  }
  return table;
}

class KernelEnumerator {
 public:
  KernelEnumerator(
      u64 limit,
      const std::vector<int>& primes,
      const std::vector<unsigned char>& is_prime
  )
      : limit_(limit), primes_(primes), is_prime_(is_prime) {}

  u64 sum() {
    // d=1 represents all perfect squares.
    answer_ = sum_of_squares(integer_sqrt(limit_));
    search(0, 1, 0, 0);
    return answer_;
  }

 private:
  u64 limit_;
  const std::vector<int>& primes_;
  const std::vector<unsigned char>& is_prime_;
  u64 answer_ = 0;

  void add_kernel(u64 kernel) {
    const u64 maximum_square = integer_sqrt(limit_ / kernel);
    const u64 contribution =
        kernel % MODULUS * sum_of_squares(maximum_square)
        % MODULUS;
    answer_ += contribution;
    if (answer_ >= MODULUS) {
      answer_ -= MODULUS;
    }
  }

  void search(
      std::size_t start,
      u64 product,
      int xor_value,
      int depth
  ) {
    for (std::size_t index = start; index < primes_.size(); ++index) {
      const int prime = primes_[index];
      if (
          static_cast<u128>(product) * prime * prime
          > limit_
      ) {
        break;
      }

      const u64 next_product = product * prime;
      const int next_xor = xor_value ^ prime;
      if (
          depth >= 1
          && next_xor > prime
          && is_prime_[next_xor]
          && static_cast<u128>(next_product) * next_xor
                 <= limit_
      ) {
        add_kernel(next_product * next_xor);
      }

      search(index + 1, next_product, next_xor, depth + 1);
    }
  }
};

u64 factorisation_nim_sum(u64 limit) {
  const u64 root = integer_sqrt(limit);
  int xor_limit = 1;
  while (xor_limit <= static_cast<int>(root)) {
    xor_limit *= 2;
  }

  const PrimeTable table = prime_table(xor_limit - 1);
  return KernelEnumerator(
      limit, table.primes, table.is_prime
  ).sum();
}

int main(int argc, char** argv) {
  const u64 limit =
      argc > 1 ? std::stoull(argv[1]) : TARGET_LIMIT;

  if (
      factorisation_nim_sum(10) != 14
      || factorisation_nim_sum(100) != 455
  ) {
    throw std::runtime_error("sample self-check failed");
  }

  std::cout << factorisation_nim_sum(limit) << '\n';
}
