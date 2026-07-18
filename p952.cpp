#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using u64 = std::uint64_t;
using u128 = unsigned __int128;

constexpr int TARGET_LIMIT = 10'000'000;
constexpr u64 TARGET_PRIME = 1'000'000'007ULL;

u64 power_mod(u64 base, u64 exponent, u64 modulus) {
  u64 result = 1 % modulus;
  base %= modulus;
  while (exponent != 0) {
    if (exponent & 1) {
      result = static_cast<u64>(
          static_cast<u128>(result) * base % modulus
      );
    }
    base = static_cast<u64>(
        static_cast<u128>(base) * base % modulus
    );
    exponent >>= 1;
  }
  return result;
}

u128 add_mod_wide(u128 left, u128 right, u128 modulus) {
  return left >= modulus - right
             ? left - (modulus - right)
             : left + right;
}

u128 multiply_mod_wide(u128 left, u128 right, u128 modulus) {
  u128 result = 0;
  while (right != 0) {
    if (right & 1) {
      result = add_mod_wide(result, left, modulus);
    }
    left = add_mod_wide(left, left, modulus);
    right >>= 1;
  }
  return result;
}

u128 power_mod_wide(u64 base, u64 exponent, u128 modulus) {
  u128 result = 1;
  u128 power = static_cast<u128>(base) % modulus;
  while (exponent != 0) {
    if (exponent & 1) {
      result = multiply_mod_wide(result, power, modulus);
    }
    power = multiply_mod_wide(power, power, modulus);
    exponent >>= 1;
  }
  return result;
}

struct Sieve {
  std::vector<int> smallest_prime;
  std::vector<int> primes;
};

Sieve linear_sieve(int limit) {
  Sieve sieve;
  sieve.smallest_prime.resize(limit + 1);
  sieve.primes.reserve(limit / 10);

  for (int value = 2; value <= limit; ++value) {
    if (sieve.smallest_prime[value] == 0) {
      sieve.smallest_prime[value] = value;
      sieve.primes.push_back(value);
    }
    for (const int prime : sieve.primes) {
      const std::int64_t composite =
          static_cast<std::int64_t>(prime) * value;
      if (
          composite > limit
          || prime > sieve.smallest_prime[value]
      ) {
        break;
      }
      sieve.smallest_prime[composite] = prime;
    }
  }
  return sieve;
}

int factorial_valuation(int limit, int prime) {
  int valuation = 0;
  while (limit != 0) {
    limit /= prime;
    valuation += limit;
  }
  return valuation;
}

int valuation_of_power_minus_one(
    u64 base,
    u64 exponent,
    int prime,
    int maximum_needed
) {
  if (maximum_needed <= 1) {
    return maximum_needed;
  }

  const u64 prime_squared =
      static_cast<u64>(prime) * static_cast<u64>(prime);
  if (power_mod(base, exponent, prime_squared) != 1) {
    return 1;
  }
  if (maximum_needed == 2) {
    return 2;
  }

  int valuation = 2;
  u128 modulus = prime_squared;
  constexpr u128 MAXIMUM_U128 = ~static_cast<u128>(0);
  while (valuation < maximum_needed) {
    if (modulus > MAXIMUM_U128 / prime) {
      throw std::overflow_error(
          "q-adic lift exceeded 128-bit modulus"
      );
    }
    modulus *= prime;
    if (power_mod_wide(base, exponent, modulus) != 1) {
      break;
    }
    ++valuation;
  }
  return valuation;
}

void record_factorization(
    int value,
    const std::vector<int>& smallest_prime,
    std::vector<int>& maximum_exponent
) {
  while (value > 1) {
    const int prime = smallest_prime[value];
    int exponent = 0;
    do {
      value /= prime;
      ++exponent;
    } while (value > 1 && smallest_prime[value] == prime);
    maximum_exponent[prime] =
        std::max(maximum_exponent[prime], exponent);
  }
}

int order_mod_prime(
    u64 base,
    int prime,
    const std::vector<int>& smallest_prime
) {
  int order = prime - 1;
  int remaining = order;
  std::array<int, 9> factors{};
  int factor_count = 0;

  while (remaining > 1) {
    const int factor = smallest_prime[remaining];
    factors[factor_count++] = factor;
    do {
      remaining /= factor;
    } while (
        remaining > 1
        && smallest_prime[remaining] == factor
    );
  }

  for (int index = 0; index < factor_count; ++index) {
    const int factor = factors[index];
    while (
        order % factor == 0
        && power_mod(base, order / factor, prime) == 1
    ) {
      order /= factor;
    }
  }
  return order;
}

int two_adic_order_exponent(u64 base, int modulus_exponent) {
  if (modulus_exponent <= 1) {
    return 0;
  }

  if (base % 4 == 1) {
    const int valuation = __builtin_ctzll(base - 1);
    return std::max(0, modulus_exponent - valuation);
  }

  const int valuation = __builtin_ctzll(base + 1);
  return std::max(1, modulus_exponent - valuation);
}

u64 order_mod_factorial(u64 base, int limit, u64 output_modulus) {
  const Sieve sieve = linear_sieve(limit);
  std::vector<int> maximum_exponent(limit + 1);

  maximum_exponent[2] = two_adic_order_exponent(
      base, factorial_valuation(limit, 2)
  );

  for (const int prime : sieve.primes) {
    if (prime == 2) {
      continue;
    }

    const int order = order_mod_prime(
        base, prime, sieve.smallest_prime
    );
    record_factorization(
        order, sieve.smallest_prime, maximum_exponent
    );

    const int modulus_exponent =
        factorial_valuation(limit, prime);
    if (modulus_exponent > 1) {
      const int initial_valuation =
          valuation_of_power_minus_one(
              base, order, prime, modulus_exponent
          );
      maximum_exponent[prime] = std::max(
          maximum_exponent[prime],
          modulus_exponent - initial_valuation
      );
    }
  }

  u64 result = 1;
  for (const int prime : sieve.primes) {
    if (maximum_exponent[prime] != 0) {
      result = static_cast<u64>(
          static_cast<u128>(result)
          * power_mod(
              prime, maximum_exponent[prime], output_modulus
          )
          % output_modulus
      );
    }
  }
  return result;
}

int main(int argc, char** argv) {
  if (argc == 3) {
    const u64 base = std::stoull(argv[1]);
    const int limit = std::stoi(argv[2]);
    std::cout
        << order_mod_factorial(base, limit, TARGET_PRIME)
        << '\n';
    return 0;
  }

  if (
      order_mod_factorial(7, 4, TARGET_PRIME) != 2
      || order_mod_factorial(TARGET_PRIME, 12, TARGET_PRIME)
          != 17'280
  ) {
    throw std::runtime_error("sample self-check failed");
  }

  std::cout
      << order_mod_factorial(
             TARGET_PRIME, TARGET_LIMIT, TARGET_PRIME
         )
      << '\n';
}
