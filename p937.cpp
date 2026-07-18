#include <cstdint>
#include <iostream>
#include <vector>

using u64 = std::uint64_t;
using i64 = std::int64_t;

constexpr int MODULUS = 1'000'000'007;

std::vector<int> sign_relevant_primes(int limit) {
  // Only odd numbers are represented: index k stores 2k+1.
  std::vector<unsigned char> composite(limit / 2 + 1);
  for (int prime = 3; 1LL * prime * prime <= limit; prime += 2) {
    if (composite[prime / 2]) {
      continue;
    }
    for (
        i64 multiple = 1LL * prime * prime;
        multiple <= limit;
        multiple += 2LL * prime
    ) {
      composite[multiple / 2] = 1;
    }
  }

  std::vector<int> primes{2};
  for (int prime = 3; prime <= limit; prime += 2) {
    if (
        !composite[prime / 2]
        && (prime % 8 == 5 || prime % 8 == 7)
    ) {
      primes.push_back(prime);
    }
  }
  return primes;
}

int factorial_partition_sum(int limit) {
  std::vector<unsigned char> sign_change(limit + 1);

  for (const int prime : sign_relevant_primes(limit)) {
    std::uint32_t factorial_valuation = 0;
    int multiplier = 1;
    for (
        int value = prime;
        value <= limit;
        value += prime, ++multiplier
    ) {
      int increment = 1;
      int remaining = multiplier;
      while (remaining >= prime && remaining % prime == 0) {
        ++increment;
        remaining /= prime;
      }

      const std::uint32_t next_valuation =
          factorial_valuation + increment;
      sign_change[value] ^=
          __builtin_parity(factorial_valuation)
          ^ __builtin_parity(next_valuation);
      factorial_valuation = next_valuation;
    }
  }

  int factorial = 1;
  int result = 0;
  int negative = 0;
  for (int value = 1; value <= limit; ++value) {
    negative ^= sign_change[value];
    factorial = static_cast<int>(
        static_cast<u64>(factorial) * value % MODULUS
    );
    if (negative == 0) {
      result += factorial;
      if (result >= MODULUS) {
        result -= MODULUS;
      }
    }
  }
  return result;
}

int main(int argc, char** argv) {
  const int limit =
      argc > 1 ? std::stoi(argv[1]) : 100'000'000;

  if (
      factorial_partition_sum(4) != 25
      || factorial_partition_sum(7) != 745
      || factorial_partition_sum(100) != 709'772'949
  ) {
    std::cerr << "sample self-check failed\n";
    return 1;
  }
  std::cout << factorial_partition_sum(limit) << '\n';
}
