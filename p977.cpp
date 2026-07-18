#include <cassert>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>

using i64 = std::int64_t;

constexpr int LIMIT = 1'000'000;
constexpr i64 MODULUS = 1'000'000'007;

i64 modular_power(i64 base, int exponent) {
  i64 result = 1;
  while (exponent != 0) {
    if ((exponent & 1) != 0) {
      result = result * base % MODULUS;
    }
    base = base * base % MODULUS;
    exponent >>= 1;
  }
  return result;
}

i64 function_count(int size) {
  std::vector<i64> inverses(size + 1);
  inverses[1] = 1;
  for (int value = 2; value <= size; ++value) {
    inverses[value] = MODULUS - (
        (MODULUS / value) * inverses[MODULUS % value]
        % MODULUS
    );
  }

  i64 result = 0;

  // Tail lengths t >= 2.  Put M=n-t+1=qL+r and sum over
  // q,L.  Complete remainder ranges are updated in O(1).
  const int maximum_m = size - 1;
  for (int quotient = 1;
       quotient <= maximum_m;
       ++quotient) {
    const int maximum_length = maximum_m / quotient;
    const int full_length = size / (quotient + 1);
    const i64 q = quotient;
    const i64 q_plus_one = quotient + 1;
    const i64 ratio =
        q_plus_one * inverses[quotient] % MODULUS;

    i64 q_power = q;
    i64 q_plus_one_power = q_plus_one;
    i64 positive_remainders = 0;

    for (int length = 1;
         length <= maximum_length;
         ++length) {
      i64 contribution = q_power * (q - 1) % MODULUS;
      if (length <= full_length) {
        contribution += positive_remainders;
      } else {
        const int final_remainder =
            maximum_m - quotient * length;
        if (final_remainder > 0) {
          const i64 geometric = (
              modular_power(ratio, final_remainder)
              + MODULUS - 1
          ) % MODULUS;
          contribution += q_power * q % MODULUS
              * q_plus_one % MODULUS * geometric
              % MODULUS;
        }
      }
      result = (result + contribution) % MODULUS;

      positive_remainders = (
          q * positive_remainders
          + q * q % MODULUS * q_plus_one_power
      ) % MODULUS;
      q_power = q_power * q % MODULUS;
      q_plus_one_power =
          q_plus_one_power * q_plus_one % MODULUS;
    }
  }

  // The t=0 and t=1 boundary cases share nearly all factors.
  for (int cycle_length = 1;
       cycle_length <= size;
       ++cycle_length) {
    const int quotient = size / cycle_length;
    const int remainder = size % cycle_length;
    i64 first_boundary;
    i64 second_boundary = 0;

    if (remainder == 0) {
      const i64 common =
          modular_power(quotient, cycle_length - 1);
      first_boundary = common;
      if (cycle_length < size) {
        second_boundary =
            common * (quotient - 1) % MODULUS;
      }
    } else {
      const i64 common =
          modular_power(quotient + 1, remainder - 1)
          * modular_power(
              quotient, cycle_length - remainder
          ) % MODULUS;
      first_boundary = common;
      if (cycle_length < size) {
        second_boundary = common * quotient % MODULUS;
      }
    }
    result = (
        result + first_boundary + second_boundary
    ) % MODULUS;
  }
  return result;
}

int main(int argc, char** argv) {
  assert(function_count(3) == 8);
  assert(function_count(7) == 174);
  assert(function_count(100) == 570271270297640131ULL % MODULUS);

  const int size = argc > 1 ? std::stoi(argv[1]) : LIMIT;
  std::cout << function_count(size) << '\n';
}
