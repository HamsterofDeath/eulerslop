#include <cstdint>
#include <iostream>
#include <numeric>
#include <vector>

using int64 = std::int64_t;

constexpr int OUTER_ITERATIONS = 12;
constexpr int64 MIDDLE_ITERATIONS = 345678;
constexpr int64 EXPONENT = 9012345;
constexpr int STARTING_NUMERAL = 678;
constexpr int STARTING_VALUE = 90;

constexpr int FIVE_POWER = 1953125;  // 5^9
constexpr int TWO_POWER = 512;       // 2^9

int64 modular_power(int64 base, int64 exponent) {
  int64 result = 1;
  while (exponent != 0) {
    if (exponent & 1) {
      result = result * base % FIVE_POWER;
    }
    base = base * base % FIVE_POWER;
    exponent >>= 1;
  }
  return result;
}

std::vector<int> mapping_power(
    const std::vector<int>& mapping,
    int64 exponent
) {
  const int size = static_cast<int>(mapping.size());
  std::vector<int> result(size);
  std::vector<int> power = mapping;
  std::vector<int> temporary(size);
  std::iota(result.begin(), result.end(), 0);

  while (exponent != 0) {
    if (exponent & 1) {
      for (int value = 0; value < size; ++value) {
        temporary[value] = power[result[value]];
      }
      result.swap(temporary);
    }

    exponent >>= 1;
    if (exponent != 0) {
      for (int value = 0; value < size; ++value) {
        temporary[value] = power[power[value]];
      }
      power.swap(temporary);
    }
  }
  return result;
}

int modular_inverse(int value, int modulus) {
  int old_remainder = value;
  int remainder = modulus;
  int old_coefficient = 1;
  int coefficient = 0;

  while (remainder != 0) {
    int quotient = old_remainder / remainder;

    int next_remainder =
        old_remainder - quotient * remainder;
    old_remainder = remainder;
    remainder = next_remainder;

    int next_coefficient =
        old_coefficient - quotient * coefficient;
    old_coefficient = coefficient;
    coefficient = next_coefficient;
  }

  old_coefficient %= modulus;
  if (old_coefficient < 0) {
    old_coefficient += modulus;
  }
  return old_coefficient;
}

int main() {
  // P(n)=n^c(n+1), the action of D_c on Church numeral n.
  std::vector<int> p(FIVE_POWER);
  std::vector<int> p_next(FIVE_POWER);
  for (int value = 0; value < FIVE_POWER; ++value) {
    p[value] =
        modular_power(value, EXPONENT)
        * (value + 1) % FIVE_POWER;
    // P_{c+1}(n) = n P_c(n).
    p_next[value] =
        static_cast<int64>(value) * p[value] % FIVE_POWER;
  }

  // f_0 = P_c^(b+1) composed with P_{c+1}.
  std::vector<int> jump =
      mapping_power(p, MIDDLE_ITERATIONS + 1);
  std::vector<int> function(FIVE_POWER);
  std::vector<int> next_function(FIVE_POWER);
  for (int value = 0; value < FIVE_POWER; ++value) {
    function[value] = jump[p_next[value]];
  }

  // If f is the action of a numeral transformer T, then
  //
  //   D_b(T)(n) = f^b(n f(n)).
  for (int level = 0; level < OUTER_ITERATIONS; ++level) {
    jump = mapping_power(function, MIDDLE_ITERATIONS);
    for (int value = 0; value < FIVE_POWER; ++value) {
      int starting_point =
          static_cast<int64>(value) * function[value]
          % FIVE_POWER;
      next_function[value] = jump[starting_point];
    }
    function.swap(next_function);
  }

  int residue_five =
      (function[STARTING_NUMERAL] + STARTING_VALUE)
      % FIVE_POWER;

  // P_{c+1}(678) is already zero modulo 2^9.  Every subsequent
  // mapping fixes zero, so only the final starting value remains.
  int residue_two = STARTING_VALUE % TWO_POWER;

  const int inverse = modular_inverse(
      FIVE_POWER % TWO_POWER,
      TWO_POWER
  );
  int difference =
      (residue_two - residue_five) % TWO_POWER;
  if (difference < 0) {
    difference += TWO_POWER;
  }
  int multiplier =
      static_cast<int64>(difference) * inverse % TWO_POWER;
  int64 answer =
      residue_five
      + static_cast<int64>(FIVE_POWER) * multiplier;

  std::cout << answer << '\n';
}
