#include <algorithm>
#include <atomic>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <thread>
#include <vector>

using u64 = std::uint64_t;
using u128 = __uint128_t;

u64 modular_power(u64 base, u64 exponent, u64 modulus) {
  u64 result = 1;
  while (exponent != 0) {
    if (exponent & 1) {
      result = static_cast<u128>(result) * base % modulus;
    }
    base = static_cast<u128>(base) * base % modulus;
    exponent >>= 1;
  }
  return result;
}

bool orbit_hits_zero(u64 modulus, u64 exponent) {
  const auto next = [=](u64 value) {
    const u64 power =
        exponent == 2
            ? static_cast<u128>(value) * value % modulus
            : modular_power(value, exponent, modulus);
    return power == modulus - 1 ? 0 : power + 1;
  };

  // Brent cycle detection proves failure without storing the orbit.
  u64 power = 1;
  u64 length = 1;
  u64 tortoise = 1;
  u64 hare = next(1);
  while (hare != 0 && tortoise != hare) {
    if (power == length) {
      tortoise = hare;
      power <<= 1;
      length = 0;
    }
    hare = next(hare);
    ++length;
  }
  return hare == 0;
}

std::vector<int> smallest_prime_factors(int limit) {
  std::vector<int> smallest_factor(limit + 1);
  for (int prime = 2; 1LL * prime * prime <= limit; ++prime) {
    if (smallest_factor[prime] != 0) {
      continue;
    }
    for (
        int multiple = prime * prime;
        multiple <= limit;
        multiple += prime
    ) {
      if (smallest_factor[multiple] == 0) {
        smallest_factor[multiple] = prime;
      }
    }
  }
  return smallest_factor;
}

std::vector<int> distinct_prime_factors(
    int value,
    const std::vector<int>& smallest_factor
) {
  std::vector<int> factors;
  while (value > 1) {
    const int factor =
        smallest_factor[value] == 0
            ? value
            : smallest_factor[value];
    factors.push_back(factor);
    do {
      value /= factor;
    } while (value % factor == 0);
  }
  // Large factors give shorter functional graphs on average, so test
  // them before the relatively expensive exponent-two orbit.
  std::sort(factors.rbegin(), factors.rend());
  return factors;
}

u64 prime_tree_sum(int limit) {
  const std::vector<int> smallest_factor =
      smallest_prime_factors(limit);

  std::vector<int> primes;
  for (int value = 2; value <= limit; ++value) {
    if (smallest_factor[value] == 0) {
      primes.push_back(value);
    }
  }

  std::vector<unsigned char> keep(primes.size());
  std::atomic<std::size_t> next_index{0};
  const unsigned int thread_count = std::max(
      1U,
      std::min(32U, std::thread::hardware_concurrency())
  );
  std::vector<std::thread> workers;
  workers.reserve(thread_count);

  for (unsigned int worker = 0; worker < thread_count; ++worker) {
    workers.emplace_back([&] {
      constexpr std::size_t block_size = 64;
      while (true) {
        const std::size_t first =
            next_index.fetch_add(block_size);
        if (first >= primes.size()) {
          break;
        }
        const std::size_t last =
            std::min(first + block_size, primes.size());

        for (std::size_t index = first; index < last; ++index) {
          const int prime = primes[index];
          bool admissible = true;

          // Over F_q, x -> x^p + 1 is a permutation whenever
          // gcd(p, q-1)=1. Since 0 maps to 1, that permutation's
          // orbit from 1 necessarily reaches 0. Thus only prime
          // divisors p of q-1 require an explicit orbit test.
          for (
              const int exponent :
              distinct_prime_factors(
                  prime - 1,
                  smallest_factor
              )
          ) {
            if (!orbit_hits_zero(prime, exponent)) {
              admissible = false;
              break;
            }
          }
          keep[index] = admissible;
        }
      }
    });
  }
  for (std::thread& worker : workers) {
    worker.join();
  }

  std::vector<int> admissible_primes;
  for (std::size_t index = 0; index < primes.size(); ++index) {
    if (keep[index]) {
      admissible_primes.push_back(primes[index]);
    }
  }

  // Any repeated prime factor would require q^2 to divide a term for
  // every exponent. The exponent-two orbit directly rules this out
  // for every admissible q with q^2 <= the requested limit.
  for (const int prime : admissible_primes) {
    const u64 square = static_cast<u64>(prime) * prime;
    if (
        square <= static_cast<u64>(limit)
        && orbit_hits_zero(square, 2)
    ) {
      throw std::logic_error(
          "unexpected admissible prime square"
      );
    }
  }

  // For a fixed exponent, every admissible prime orbit has 0
  // immediately before its return to 1. Their zero indices therefore
  // synchronize at one less than the lcm of the orbit periods.
  // Hence every squarefree product, and only such a product here,
  // belongs to S.
  std::vector<int> values{1};
  for (const int prime : admissible_primes) {
    const std::size_t old_size = values.size();
    for (std::size_t index = 0; index < old_size; ++index) {
      if (values[index] <= limit / prime) {
        values.push_back(values[index] * prime);
      }
    }
  }

  u64 result = 0;
  for (const int value : values) {
    result += value;
  }
  return result;
}

int main(int argc, char** argv) {
  const int limit =
      argc > 1 ? std::stoi(argv[1]) : 10'000'000;
  std::cout << prime_tree_sum(limit) << '\n';
}
