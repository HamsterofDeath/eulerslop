#include <algorithm>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <utility>
#include <vector>

using u64 = std::uint64_t;
using u128 = unsigned __int128;

constexpr int TARGET = 1'000'000;
constexpr u64 MODULUS = 999'999'893;

struct Matrix {
  u64 a;
  u64 b;
  u64 c;
  u64 d;
};

Matrix multiply(Matrix left, Matrix right, u64 modulus) {
  return {
      static_cast<u64>(
          (static_cast<u128>(left.a) * right.a
           + static_cast<u128>(left.b) * right.c) % modulus
      ),
      static_cast<u64>(
          (static_cast<u128>(left.a) * right.b
           + static_cast<u128>(left.b) * right.d) % modulus
      ),
      static_cast<u64>(
          (static_cast<u128>(left.c) * right.a
           + static_cast<u128>(left.d) * right.c) % modulus
      ),
      static_cast<u64>(
          (static_cast<u128>(left.c) * right.b
           + static_cast<u128>(left.d) * right.d) % modulus
      )
  };
}

Matrix matrix_power(u64 exponent, u64 modulus) {
  Matrix result{1, 0, 0, 1};
  Matrix base{0, 1, 1, 1};
  while (exponent != 0) {
    if (exponent & 1) {
      result = multiply(result, base, modulus);
    }
    base = multiply(base, base, modulus);
    exponent >>= 1;
  }
  return result;
}

bool is_identity(u64 exponent, u64 modulus) {
  const Matrix value = matrix_power(exponent, modulus);
  return value.a == 1 && value.b == 0
         && value.c == 0 && value.d == 1;
}

u64 scalar_power(u64 base, u64 exponent, u64 modulus) {
  u64 result = 1;
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

std::vector<int> distinct_factors(int value, const std::vector<int>& spf) {
  std::vector<int> factors;
  while (value > 1) {
    const int prime = spf[value];
    factors.push_back(prime);
    while (value % prime == 0) {
      value /= prime;
    }
  }
  return factors;
}

u64 matrix_order_prime(int prime, const std::vector<int>& spf) {
  if (prime == 2) {
    return 3;
  }
  if (prime == 5) {
    return 20;
  }
  u64 order = prime % 5 == 1 || prime % 5 == 4
      ? static_cast<u64>(prime - 1)
      : 2ULL * (prime + 1);
  for (int factor : distinct_factors(static_cast<int>(order), spf)) {
    while (
        order % factor == 0
        && is_identity(order / factor, prime)
    ) {
      order /= factor;
    }
  }
  return order;
}

u64 square_root_mod_prime(u64 value, u64 prime) {
  if (prime % 4 == 3) {
    return scalar_power(value, (prime + 1) / 4, prime);
  }

  u64 odd = prime - 1;
  int twos = 0;
  while ((odd & 1) == 0) {
    odd >>= 1;
    ++twos;
  }
  u64 nonresidue = 2;
  while (
      scalar_power(nonresidue, (prime - 1) / 2, prime) != prime - 1
  ) {
    ++nonresidue;
  }

  u64 c = scalar_power(nonresidue, odd, prime);
  u64 x = scalar_power(value, (odd + 1) / 2, prime);
  u64 t = scalar_power(value, odd, prime);
  int power = twos;
  while (t != 1) {
    int least = 1;
    u64 squared = t * t % prime;
    while (squared != 1) {
      squared = squared * squared % prime;
      ++least;
    }
    const u64 adjustment =
        scalar_power(c, u64{1} << (power - least - 1), prime);
    x = x * adjustment % prime;
    const u64 adjustment_squared =
        adjustment * adjustment % prime;
    t = t * adjustment_squared % prime;
    c = adjustment_squared;
    power = least;
  }
  return x;
}

u64 scalar_order(
    u64 value, int prime, const std::vector<int>& spf
) {
  u64 order = prime - 1;
  for (int factor : distinct_factors(prime - 1, spf)) {
    while (
        order % factor == 0
        && scalar_power(value, order / factor, prime) == 1
    ) {
      order /= factor;
    }
  }
  return order;
}

u64 integer_power(u64 base, int exponent) {
  u64 result = 1;
  while (exponent-- != 0) {
    result *= base;
  }
  return result;
}

int valuation(u64 value, int prime, int cap) {
  if (value == 0) {
    return cap;
  }
  int result = 0;
  while (result < cap && value % prime == 0) {
    value /= prime;
    ++result;
  }
  return result;
}

u64 fixed_vectors(
    const Matrix& power, int prime, int level, int precision
) {
  if (level == 0) {
    return 1;
  }
  const u64 high_modulus = integer_power(prime, precision);
  const u64 e00 = (power.a + high_modulus - 1) % high_modulus;
  const u64 e01 = power.b;
  const u64 e10 = power.c;
  const u64 e11 = (power.d + high_modulus - 1) % high_modulus;

  const int first_invariant = std::min({
      valuation(e00, prime, precision),
      valuation(e01, prime, precision),
      valuation(e10, prime, precision),
      valuation(e11, prime, precision)
  });
  if (first_invariant >= level) {
    return integer_power(prime, 2 * level);
  }

  const u64 product_one = static_cast<u64>(
      static_cast<u128>(e00) * e11 % high_modulus
  );
  const u64 product_two = static_cast<u64>(
      static_cast<u128>(e01) * e10 % high_modulus
  );
  const u64 determinant =
      (product_one + high_modulus - product_two) % high_modulus;
  const int determinant_valuation =
      valuation(determinant, prime, precision);
  const int second_invariant =
      determinant_valuation - first_invariant;
  const int kernel_exponent =
      std::min(level, first_invariant)
      + std::min(level, second_invariant);
  return integer_power(prime, kernel_exponent);
}

struct PeriodCount {
  u64 period;
  u64 count;
};

std::vector<u64> divisors(u64 value, const std::vector<int>& spf) {
  std::vector<u64> result{1};
  int remaining = static_cast<int>(value);
  while (remaining > 1) {
    const int prime = spf[remaining];
    int exponent = 0;
    while (remaining % prime == 0) {
      remaining /= prime;
      ++exponent;
    }
    const std::size_t old_size = result.size();
    u64 factor = 1;
    for (int power = 1; power <= exponent; ++power) {
      factor *= prime;
      for (std::size_t i = 0; i < old_size; ++i) {
        result.push_back(result[i] * factor);
      }
    }
  }
  std::sort(result.begin(), result.end());
  return result;
}

std::vector<PeriodCount> generic_prime_power_distribution(
    int prime, int exponent, u64 order,
    const std::vector<int>& spf
) {
  const u64 modulus = integer_power(prime, exponent);
  const u64 high_modulus = modulus * modulus;
  const std::vector<u64> candidates = divisors(order, spf);
  std::vector<u64> exact(candidates.size());
  std::vector<PeriodCount> result;

  for (std::size_t i = 0; i < candidates.size(); ++i) {
    const Matrix powered =
        matrix_power(candidates[i], high_modulus);
    u64 count =
        fixed_vectors(powered, prime, exponent, 2 * exponent)
        - fixed_vectors(powered, prime, exponent - 1, 2 * exponent);
    for (std::size_t j = 0; j < i; ++j) {
      if (candidates[i] % candidates[j] == 0) {
        count -= exact[j];
      }
    }
    exact[i] = count;
    if (count != 0) {
      result.push_back({candidates[i], count});
    }
  }
  return result;
}

std::vector<PeriodCount> prime_distribution(
    int prime, u64 matrix_order, const std::vector<int>& spf
) {
  if (prime == 5) {
    return {{4, 4}, {20, 20}};
  }
  if (prime == 2 || (prime % 5 != 1 && prime % 5 != 4)) {
    return {
        {matrix_order, static_cast<u64>(prime) * prime - 1}
    };
  }

  const u64 root = square_root_mod_prime(5, prime);
  const u64 inverse_two = (prime + 1) / 2;
  const u64 eigenvalue_one = (1 + root) * inverse_two % prime;
  const u64 eigenvalue_two =
      (1 + prime - root) * inverse_two % prime;
  const u64 order_one = scalar_order(eigenvalue_one, prime, spf);
  const u64 order_two = scalar_order(eigenvalue_two, prime, spf);

  std::vector<PeriodCount> result;
  auto add = [&](u64 period, u64 count) {
    for (PeriodCount& entry : result) {
      if (entry.period == period) {
        entry.count += count;
        return;
      }
    }
    result.push_back({period, count});
  };
  add(order_one, prime - 1);
  add(order_two, prime - 1);
  add(
      std::lcm(order_one, order_two),
      static_cast<u64>(prime - 1) * (prime - 1)
  );
  return result;
}

std::vector<int> smallest_prime_factors(int limit) {
  std::vector<int> spf(limit + 1);
  for (int value = 2; value <= limit; ++value) {
    if (spf[value] != 0) {
      continue;
    }
    spf[value] = value;
    if (static_cast<u64>(value) * value <= limit) {
      for (int multiple = value * value;
           multiple <= limit; multiple += value) {
        if (spf[multiple] == 0) {
          spf[multiple] = value;
        }
      }
    }
  }
  return spf;
}

u64 solve(int limit) {
  const std::vector<int> spf =
      smallest_prime_factors(2 * limit + 10);
  std::vector<std::vector<PeriodCount>> local_cache(limit + 1);
  std::vector<u64> prime_order(limit + 1);
  u64 answer = 0;

  for (int modulus = 1; modulus <= limit; ++modulus) {
    std::vector<PeriodCount> distribution{{1, 1}};
    int remaining = modulus;
    while (remaining > 1) {
      const int prime = spf[remaining];
      int prime_power = 1;
      int exponent = 0;
      while (remaining % prime == 0) {
        remaining /= prime;
        prime_power *= prime;
        ++exponent;
      }

      if (local_cache[prime_power].empty()) {
        if (prime_order[prime] == 0) {
          prime_order[prime] = matrix_order_prime(prime, spf);
        }
        u64 order = prime_order[prime];
        u64 lifted_modulus = prime;
        for (int level = 2; level <= exponent; ++level) {
          lifted_modulus *= prime;
          if (!is_identity(order, lifted_modulus)) {
            order *= prime;
          }
        }
        local_cache[prime_power] = exponent == 1
            ? prime_distribution(prime, order, spf)
            : generic_prime_power_distribution(
                prime, exponent, order, spf
              );
      }

      std::vector<PeriodCount> combined;
      for (const PeriodCount& left : distribution) {
        for (const PeriodCount& right : local_cache[prime_power]) {
          const u64 period = std::lcm(left.period, right.period);
          const u64 count =
              left.count * (right.count % MODULUS) % MODULUS;
          auto same = std::find_if(
              combined.begin(), combined.end(),
              [&](const PeriodCount& entry) {
                return entry.period == period;
              }
          );
          if (same == combined.end()) {
            combined.push_back({period, count});
          } else {
            same->count = (same->count + count) % MODULUS;
          }
        }
      }
      distribution = std::move(combined);
    }

    u64 primitive_sum = 0;
    for (const PeriodCount& entry : distribution) {
      const u64 period = entry.period % MODULUS;
      primitive_sum = (
          primitive_sum
          + entry.count * period % MODULUS * period
      ) % MODULUS;
    }
    answer = (
        answer
        + static_cast<u64>(limit / modulus) * primitive_sum
    ) % MODULUS;
  }
  return answer;
}

int main() {
  if (solve(3) != 542 || solve(10) != 310'897) {
    std::cerr << "sample self-check failed\n";
    return 1;
  }
  std::cout << solve(TARGET) << '\n';
}
