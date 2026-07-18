#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>

using i64 = std::int64_t;
using i128 = __int128_t;

constexpr int MODULUS = 1'111'124'111;

template <int Modulus>
int modular_power(i64 base, i64 exponent) {
  i64 result = 1;
  while (exponent != 0) {
    if (exponent & 1) {
      result = result * base % Modulus;
    }
    base = base * base % Modulus;
    exponent >>= 1;
  }
  return static_cast<int>(result);
}

template <int Prime, int PrimitiveRoot>
void number_theoretic_transform(
    std::vector<int>& values,
    bool inverse
) {
  const int size = static_cast<int>(values.size());
  for (int index = 1, reverse = 0; index < size; ++index) {
    int bit = size >> 1;
    while (reverse & bit) {
      reverse ^= bit;
      bit >>= 1;
    }
    reverse ^= bit;
    if (index < reverse) {
      std::swap(values[index], values[reverse]);
    }
  }

  for (int length = 2; length <= size; length <<= 1) {
    int root = modular_power<Prime>(
        PrimitiveRoot,
        (Prime - 1) / length
    );
    if (inverse) {
      root = modular_power<Prime>(root, Prime - 2);
    }

    for (int start = 0; start < size; start += length) {
      i64 power = 1;
      for (int offset = 0; offset < length / 2; ++offset) {
        const int left = values[start + offset];
        const int right = static_cast<int>(
            power
            * values[start + offset + length / 2]
            % Prime
        );

        int sum = left + right;
        if (sum >= Prime) {
          sum -= Prime;
        }
        int difference = left - right;
        if (difference < 0) {
          difference += Prime;
        }
        values[start + offset] = sum;
        values[start + offset + length / 2] =
            difference;
        power = power * root % Prime;
      }
    }
  }

  if (inverse) {
    const int inverse_size =
        modular_power<Prime>(size, Prime - 2);
    for (int& value : values) {
      value = static_cast<int>(
          static_cast<i64>(value) * inverse_size % Prime
      );
    }
  }
}

template <int Prime, int PrimitiveRoot>
std::vector<int> convolution_prime(
    const std::vector<int>& left,
    const std::vector<int>& right,
    int needed
) {
  const int left_size =
      std::min(static_cast<int>(left.size()), needed);
  const int right_size =
      std::min(static_cast<int>(right.size()), needed);
  const int result_size = std::min(
      needed,
      left_size + right_size - 1
  );

  int transform_size = 1;
  while (
      transform_size < left_size + right_size - 1
  ) {
    transform_size <<= 1;
  }

  std::vector<int> transformed_left(transform_size);
  std::vector<int> transformed_right(transform_size);
  for (int index = 0; index < left_size; ++index) {
    transformed_left[index] = left[index] % Prime;
  }
  for (int index = 0; index < right_size; ++index) {
    transformed_right[index] = right[index] % Prime;
  }

  number_theoretic_transform<Prime, PrimitiveRoot>(
      transformed_left, false
  );
  number_theoretic_transform<Prime, PrimitiveRoot>(
      transformed_right, false
  );
  for (int index = 0; index < transform_size; ++index) {
    transformed_left[index] = static_cast<int>(
        static_cast<i64>(transformed_left[index])
        * transformed_right[index]
        % Prime
    );
  }
  number_theoretic_transform<Prime, PrimitiveRoot>(
      transformed_left, true
  );
  transformed_left.resize(result_size);
  return transformed_left;
}

std::vector<int> convolution(
    const std::vector<int>& left,
    const std::vector<int>& right,
    int needed
) {
  constexpr int PRIME_1 = 998'244'353;
  constexpr int PRIME_2 = 469'762'049;
  constexpr int PRIME_3 = 167'772'161;
  constexpr int ROOT = 3;

  if (left.empty() || right.empty() || needed <= 0) {
    return {};
  }

  const std::vector<int> residue_1 =
      convolution_prime<PRIME_1, ROOT>(
          left, right, needed
      );
  const std::vector<int> residue_2 =
      convolution_prime<PRIME_2, ROOT>(
          left, right, needed
      );
  const std::vector<int> residue_3 =
      convolution_prime<PRIME_3, ROOT>(
          left, right, needed
      );

  const i64 inverse_1_mod_2 =
      modular_power<PRIME_2>(
          PRIME_1 % PRIME_2,
          PRIME_2 - 2
      );
  const i64 prime_1_mod_3 = PRIME_1 % PRIME_3;
  const i64 prime_12_mod_3 =
      prime_1_mod_3 * (PRIME_2 % PRIME_3) % PRIME_3;
  const i64 inverse_12_mod_3 =
      modular_power<PRIME_3>(
          prime_12_mod_3,
          PRIME_3 - 2
      );
  const i64 prime_1_mod_target = PRIME_1 % MODULUS;
  const i64 prime_12_mod_target =
      prime_1_mod_target * (PRIME_2 % MODULUS)
      % MODULUS;

  std::vector<int> result(residue_1.size());
  for (std::size_t index = 0; index < result.size(); ++index) {
    i64 second_digit =
        (residue_2[index] - residue_1[index])
        % PRIME_2;
    if (second_digit < 0) {
      second_digit += PRIME_2;
    }
    second_digit =
        second_digit * inverse_1_mod_2 % PRIME_2;

    const i64 first_two_mod_3 =
        (
            residue_1[index]
            + prime_1_mod_3
                * (second_digit % PRIME_3)
        ) % PRIME_3;
    i64 third_digit =
        (residue_3[index] - first_two_mod_3)
        % PRIME_3;
    if (third_digit < 0) {
      third_digit += PRIME_3;
    }
    third_digit =
        third_digit * inverse_12_mod_3 % PRIME_3;

    result[index] = static_cast<int>(
        (
            residue_1[index] % MODULUS
            + static_cast<i128>(prime_1_mod_target)
                * second_digit % MODULUS
            + static_cast<i128>(prime_12_mod_target)
                * third_digit % MODULUS
        ) % MODULUS
    );
  }
  return result;
}

std::vector<int> inverse_series(
    const std::vector<int>& series
) {
  const int needed = static_cast<int>(series.size());
  std::vector<int> inverse{
      modular_power<MODULUS>(
          series[0],
          MODULUS - 2
      )
  };

  while (static_cast<int>(inverse.size()) < needed) {
    const int next_size = std::min(
        2 * static_cast<int>(inverse.size()),
        needed
    );
    const std::vector<int> prefix(
        series.begin(),
        series.begin() + next_size
    );
    std::vector<int> correction =
        convolution(prefix, inverse, next_size);
    correction.resize(next_size);

    correction[0] = (2 - correction[0]) % MODULUS;
    if (correction[0] < 0) {
      correction[0] += MODULUS;
    }
    for (int index = 1; index < next_size; ++index) {
      if (correction[index] != 0) {
        correction[index] =
            MODULUS - correction[index];
      }
    }

    inverse = convolution(
        inverse, correction, next_size
    );
    inverse.resize(next_size);
  }
  return inverse;
}

int odd_run_compositions(int target) {
  // x/(1+x-x^2) has coefficients
  // 1,-1,2,-3,5,...: signed Fibonacci numbers.
  std::vector<int> fibonacci(target + 1);
  if (target >= 1) {
    fibonacci[1] = 1;
  }
  for (int index = 2; index <= target; ++index) {
    fibonacci[index] = static_cast<int>(
        (
            static_cast<i64>(fibonacci[index - 1])
            + fibonacci[index - 2]
        ) % MODULUS
    );
  }

  std::vector<int> denominator(target + 1);
  denominator[0] = 1;
  for (int quotient = 1; quotient <= target; ++quotient) {
    const int coefficient =
        quotient & 1
            ? fibonacci[quotient]
            : (
                fibonacci[quotient] == 0
                    ? 0
                    : MODULUS - fibonacci[quotient]
            );
    for (
        int degree = quotient;
        degree <= target;
        degree += quotient
    ) {
      // The denominator is 1 minus the Lambert series.
      denominator[degree] -= coefficient;
      if (denominator[degree] < 0) {
        denominator[degree] += MODULUS;
      }
    }
  }

  const std::vector<int> generating_function =
      inverse_series(denominator);
  assert(
      target < 5 || generating_function[5] == 10
  );
  return generating_function[target];
}

int main(int argc, char** argv) {
  const int target =
      argc > 1 ? std::stoi(argv[1]) : 100'000;
  std::cout << odd_run_compositions(target) << '\n';
}
