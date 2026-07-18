#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>

using u64 = std::uint64_t;
using i128 = __int128;
using u128 = unsigned __int128;

constexpr u64 LIMIT = 1'000'000'000'000'000'000ULL;
constexpr int PRIME_BOUND = 120;

struct Counter {
  u64 limit;
  std::vector<int> primes;
  i128 result = 0;

  void visit(
      int first_prime,
      u64 product,
      const std::array<int, 3>& coefficients
  ) {
    result += static_cast<i128>(limit / product)
        * coefficients[0];

    for (int index = first_prime;
         index < static_cast<int>(primes.size());
         ++index) {
      const int prime = primes[index];
      if (static_cast<u128>(product) * prime > limit) {
        break;
      }

      const int shift = prime % 3;
      std::array<int, 3> next{};
      for (int residue = 0; residue < 3; ++residue) {
        next[residue] =
            coefficients[(residue - shift + 3) % 3]
            - coefficients[residue];
      }
      visit(index + 1, product * prime, next);
    }
  }
};

std::vector<int> primes_up_to(int bound) {
  std::vector<int> primes;
  for (int candidate = 2; candidate <= bound; ++candidate) {
    bool is_prime = true;
    for (int divisor = 2;
         divisor * divisor <= candidate;
         ++divisor) {
      if (candidate % divisor == 0) {
        is_prime = false;
        break;
      }
    }
    if (is_prime && candidate != 3) {
      primes.push_back(candidate);
    }
  }
  return primes;
}

i128 trivisible_count(u64 limit, int prime_bound) {
  Counter counter{limit, primes_up_to(prime_bound)};
  counter.visit(0, 1, {1, 0, 0});
  return counter.result;
}

std::string decimal(i128 value) {
  assert(value >= 0);
  std::string result;
  do {
    result.push_back(static_cast<char>('0' + value % 10));
    value /= 10;
  } while (value != 0);
  std::reverse(result.begin(), result.end());
  return result;
}

int main(int argc, char** argv) {
  assert(trivisible_count(10, 4) == 5);
  assert(trivisible_count(10, 10) == 3);
  assert(trivisible_count(100, 10) == 41);

  const u64 limit =
      argc > 1 ? std::stoull(argv[1]) : LIMIT;
  const int bound =
      argc > 2 ? std::stoi(argv[2]) : PRIME_BOUND;
  std::cout << decimal(trivisible_count(limit, bound)) << '\n';
}
