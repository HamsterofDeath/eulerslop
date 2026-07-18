#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <string>

using u64 = std::uint64_t;

constexpr int LIMIT = 1'000'000;
constexpr u64 SEQUENCE_MODULUS = 888'888'883;
constexpr u64 MULTIPLIER = 8'888;
constexpr u64 INITIAL_VALUE = 88'888'888;

// Codes are basis + 4*sign, with bases 1,x,y,z and sign 0
// positive, 1 negative.
int multiply(int first, int second) {
  static constexpr int basis_product[4][4] = {
      {0, 1, 2, 3},
      {1, 0, 3, 2},
      {2, 3, 0, 1},
      {3, 2, 1, 0},
  };
  static constexpr int negative[4][4] = {
      {0, 0, 0, 0},
      {0, 1, 0, 1},
      {0, 1, 1, 0},
      {0, 0, 1, 1},
  };

  const int first_basis = first & 3;
  const int second_basis = second & 3;
  const int sign = (first >> 2) ^ (second >> 2)
      ^ negative[first_basis][second_basis];
  return basis_product[first_basis][second_basis] + 4 * sign;
}

int inverse(int value) {
  if ((value & 3) == 0) {
    return value;
  }
  return value ^ 4;
}

u64 neutral_pairs(int block_count) {
  std::array<u64, 8> counts{};
  u64 sequence_value = INITIAL_VALUE;

  for (int block = 0; block < block_count; ++block) {
    int product = 0;
    for (int index = 0; index < 50; ++index) {
      const int generator = 1 + sequence_value % 3;
      product = multiply(product, generator);
      sequence_value =
          MULTIPLIER * sequence_value % SEQUENCE_MODULUS;
    }
    ++counts[product];
  }

  u64 result = 0;
  for (int value = 0; value < 8; ++value) {
    result += counts[value] * counts[inverse(value)];
  }
  return result;
}

int main(int argc, char** argv) {
  assert(neutral_pairs(10) == 13);
  assert(neutral_pairs(100) == 1224);
  const int limit = argc > 1 ? std::stoi(argv[1]) : LIMIT;
  std::cout << neutral_pairs(limit) << '\n';
}
