#include <algorithm>
#include <atomic>
#include <cassert>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <thread>
#include <vector>

using u32 = std::uint32_t;
using u64 = std::uint64_t;

constexpr u64 MODULUS = 1'000'000'009;
constexpr u64 TARGET = 100'000'000'000'000;
constexpr u64 SQRT_FIVE = 383'008'016;
constexpr u64 PHI = 691'504'013;
constexpr u64 PSI = 308'495'997;

u64 multiply_mod(u64 first, u64 second) {
  return first * second % MODULUS;
}

u64 add_mod(u64 first, u64 second) {
  const u64 sum = first + second;
  return sum >= MODULUS ? sum - MODULUS : sum;
}

u64 subtract_mod(u64 first, u64 second) {
  return first >= second ? first - second
                         : first + MODULUS - second;
}

u64 negate_mod(u64 value) {
  return value == 0 ? 0 : MODULUS - value;
}

u64 power_mod(u64 base, u64 exponent) {
  u64 result = 1;
  while (exponent > 0) {
    if (exponent & 1) {
      result = multiply_mod(result, base);
    }
    base = multiply_mod(base, base);
    exponent >>= 1;
  }
  return result;
}

u64 integer_square_root(u64 value) {
  u64 root = static_cast<u64>(
      std::sqrt(static_cast<long double>(value)));
  while (root + 1 <= value / (root + 1)) {
    ++root;
  }
  while (root > value / root) {
    --root;
  }
  return root;
}

std::vector<std::int8_t> mobius_sieve(int limit) {
  std::vector<std::int8_t> mobius(limit + 1);
  std::vector<int> least_prime(limit + 1);
  std::vector<int> primes;
  mobius[1] = 1;

  for (int value = 2; value <= limit; ++value) {
    if (least_prime[value] == 0) {
      least_prime[value] = value;
      primes.push_back(value);
      mobius[value] = -1;
    }
    for (int prime : primes) {
      const std::int64_t product =
          static_cast<std::int64_t>(value) * prime;
      if (product > limit || prime > least_prime[value]) {
        break;
      }
      least_prime[product] = prime;
      if (prime == least_prime[value]) {
        mobius[product] = 0;
        break;
      }
      mobius[product] = -mobius[value];
    }
  }
  return mobius;
}

struct PowerSequence {
  u64 index;
  u64 term;
  u64 ratio;
  u64 ratio_step;

  static PowerSequence squares(u64 base) {
    return {0, 1, base, multiply_mod(base, base)};
  }

  static PowerSequence triangular(u64 base) {
    const u64 base_squared = multiply_mod(base, base);
    return {0, 1, base_squared, base_squared};
  }

  void advance() {
    term = multiply_mod(term, ratio);
    ratio = multiply_mod(ratio, ratio_step);
    ++index;
  }

  void extend_through(u64 target, u64& window) {
    while (index <= target) {
      window = add_mod(window, term);
      advance();
    }
  }

  void trim_before(u64 target, u64& window) {
    while (index < target) {
      window = subtract_mod(window, term);
      advance();
    }
  }
};

u64 nonprimitive_sum(u64 limit, u64 weight, u64 inverse_weight) {
  if (limit == 0) {
    return 0;
  }

  const u64 square_root = integer_square_root(limit);
  const u64 inverse_fifth = power_mod(inverse_weight, 5);
  const u64 inverse_tenth =
      multiply_mod(inverse_fifth, inverse_fifth);
  u64 answer = 0;

  const u64 even_max = square_root / 2;
  if (even_max > 0) {
    PowerSequence add_sequence = PowerSequence::squares(weight);
    PowerSequence trim_sequence = PowerSequence::squares(weight);
    u64 window = 0;
    u64 factor = 1;
    u64 factor_ratio = inverse_fifth;

    for (u64 t = 1; t <= even_max; ++t) {
      factor = multiply_mod(factor, factor_ratio);
      factor_ratio = multiply_mod(factor_ratio, inverse_tenth);
      const u64 upper =
          integer_square_root(limit + 5 * t * t);
      add_sequence.extend_through(upper, window);
      trim_sequence.trim_before(3 * t, window);
      answer = add_mod(answer, multiply_mod(factor, window));
    }
  }

  const u64 odd_max = (square_root - 1) / 2;
  PowerSequence add_sequence = PowerSequence::triangular(weight);
  PowerSequence trim_sequence = PowerSequence::triangular(weight);
  u64 window = 0;
  u64 factor = inverse_weight;
  u64 factor_ratio = inverse_tenth;

  for (u64 t = 0; t <= odd_max; ++t) {
    const u64 discriminant =
        4 * limit + 20 * t * t + 20 * t + 5;
    const u64 upper =
        (integer_square_root(discriminant) - 1) / 2;
    add_sequence.extend_through(upper, window);
    trim_sequence.trim_before(3 * t + 1, window);
    answer = add_mod(answer, multiply_mod(factor, window));
    factor = multiply_mod(factor, factor_ratio);
    factor_ratio = multiply_mod(factor_ratio, inverse_tenth);
  }

  return answer;
}

std::vector<u32> square_powers(u64 base, int limit) {
  std::vector<u32> powers(limit + 1);
  powers[0] = 1;
  const u64 base_squared = multiply_mod(base, base);
  u64 value = 1;
  u64 ratio = base;
  for (int index = 1; index <= limit; ++index) {
    value = multiply_mod(value, ratio);
    powers[index] = static_cast<u32>(value);
    ratio = multiply_mod(ratio, base_squared);
  }
  return powers;
}

u64 fibonacci_root_sum(u64 limit) {
  const int maximum_divisor =
      static_cast<int>(integer_square_root(limit));
  const std::vector<std::int8_t> mobius =
      mobius_sieve(maximum_divisor);
  const u64 inverse_phi = power_mod(PHI, MODULUS - 2);
  const std::vector<u32> phi_squares =
      square_powers(PHI, maximum_divisor);
  const std::vector<u32> inverse_phi_squares =
      square_powers(inverse_phi, maximum_divisor);

  const unsigned int thread_count = std::max(
      1U, std::min<unsigned int>(
              std::thread::hardware_concurrency(),
              static_cast<unsigned int>(maximum_divisor)));
  std::atomic<int> next_divisor{1};
  std::vector<u64> phi_subtotals(thread_count);
  std::vector<u64> psi_subtotals(thread_count);
  std::vector<std::thread> workers;

  for (unsigned int worker = 0; worker < thread_count; ++worker) {
    workers.emplace_back([&, worker]() {
      u64 phi_total = 0;
      u64 psi_total = 0;
      constexpr int CHUNK_SIZE = 32;

      while (true) {
        const int start = next_divisor.fetch_add(CHUNK_SIZE);
        if (start > maximum_divisor) {
          break;
        }
        const int end =
            std::min(maximum_divisor + 1, start + CHUNK_SIZE);
        for (int divisor = start; divisor < end; ++divisor) {
          const int sign = mobius[divisor];
          if (sign == 0) {
            continue;
          }

          const u64 divisor_squared =
              static_cast<u64>(divisor) * divisor;
          const u64 scaled_limit = limit / divisor_squared;
          const u64 phi_weight = phi_squares[divisor];
          const u64 phi_inverse = inverse_phi_squares[divisor];
          const bool odd = divisor & 1;
          const u64 psi_weight =
              odd ? negate_mod(phi_inverse) : phi_inverse;
          const u64 psi_inverse =
              odd ? negate_mod(phi_weight) : phi_weight;

          const u64 phi_value = nonprimitive_sum(
              scaled_limit, phi_weight, phi_inverse);
          const u64 psi_value = nonprimitive_sum(
              scaled_limit, psi_weight, psi_inverse);
          if (sign > 0) {
            phi_total = add_mod(phi_total, phi_value);
            psi_total = add_mod(psi_total, psi_value);
          } else {
            phi_total = subtract_mod(phi_total, phi_value);
            psi_total = subtract_mod(psi_total, psi_value);
          }
        }
      }
      phi_subtotals[worker] = phi_total;
      psi_subtotals[worker] = psi_total;
    });
  }

  for (std::thread& worker : workers) {
    worker.join();
  }

  u64 phi_total = 0;
  u64 psi_total = 0;
  for (unsigned int worker = 0; worker < thread_count; ++worker) {
    phi_total = add_mod(phi_total, phi_subtotals[worker]);
    psi_total = add_mod(psi_total, psi_subtotals[worker]);
  }

  const u64 inverse_sqrt_five =
      power_mod(SQRT_FIVE, MODULUS - 2);
  return multiply_mod(
      subtract_mod(phi_total, psi_total), inverse_sqrt_five);
}

int main(int argc, char** argv) {
  assert(multiply_mod(SQRT_FIVE, SQRT_FIVE) == 5);
  assert(subtract_mod(multiply_mod(PHI, PHI), PHI) == 1);
  assert(subtract_mod(multiply_mod(PSI, PSI), PSI) == 1);
  assert(fibonacci_root_sum(1'000) == 190'950'976);

  const u64 limit =
      argc > 1 ? std::stoull(argv[1]) : TARGET;
  std::cout << fibonacci_root_sum(limit) << '\n';
}
