#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <limits>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

using u64 = std::uint64_t;
using u128 = unsigned __int128;

constexpr int LIMIT = 100'000;
constexpr int SCALE_EXPONENT = 16;
constexpr int SCALE = 1 << SCALE_EXPONENT;
constexpr int MAX_COEFFICIENTS = 10;

struct ComponentKey {
  int number;
  u64 coefficients;
  unsigned char nimber;

  bool operator==(const ComponentKey& other) const {
    return number == other.number
        && coefficients == other.coefficients
        && nimber == other.nimber;
  }
};

struct SumKey {
  int number;
  u64 coefficients;
  unsigned char nimber;

  bool operator==(const SumKey& other) const {
    return number == other.number
        && coefficients == other.coefficients
        && nimber == other.nimber;
  }
};

u64 mix(u64 value) {
  value ^= value >> 30;
  value *= 0xbf58476d1ce4e5b9ULL;
  value ^= value >> 27;
  value *= 0x94d049bb133111ebULL;
  return value ^ (value >> 31);
}

struct ComponentHash {
  std::size_t operator()(const ComponentKey& key) const {
    return mix(
        static_cast<std::uint32_t>(key.number)
        ^ (key.coefficients * 0x9e3779b97f4a7c15ULL)
        ^ key.nimber
    );
  }
};

struct SumHash {
  std::size_t operator()(const SumKey& key) const {
    return mix(
        static_cast<std::uint32_t>(key.number)
        ^ (key.coefficients * 0x9e3779b97f4a7c15ULL)
        ^ key.nimber
    );
  }
};

long long floor_div(long long numerator, long long denominator) {
  if (numerator >= 0) {
    return numerator / denominator;
  }
  return -((-numerator + denominator - 1) / denominator);
}

std::vector<int> binary_game_values(int maximum_digits) {
  const int maximum = (1 << maximum_digits) - 1;
  std::vector<int> values(maximum + 1);

  for (int number = 1; number <= maximum; ++number) {
    const std::string word = [] (int value) {
      std::string result;
      while (value != 0) {
        result.push_back(static_cast<char>('0' + (value & 1)));
        value >>= 1;
      }
      std::reverse(result.begin(), result.end());
      return result;
    }(number);

    int best_left = std::numeric_limits<int>::min();
    int best_right = std::numeric_limits<int>::max();
    int left_count = 0;
    int right_count = 0;

    for (int deleted = 0;
         deleted < static_cast<int>(word.size());
         ++deleted) {
      int follower = 0;
      for (int index = 0;
           index < static_cast<int>(word.size());
           ++index) {
        if (index != deleted) {
          follower = 2 * follower + word[index] - '0';
        }
      }

      if (word[deleted] == '0') {
        best_left = std::max(best_left, values[follower]);
        ++left_count;
      } else {
        best_right = std::min(best_right, values[follower]);
        ++right_count;
      }
    }

    if (left_count == 0) {
      values[number] = static_cast<int>(
          (floor_div(best_right + SCALE - 1, SCALE) - 1) * SCALE
      );
      continue;
    }
    if (right_count == 0) {
      values[number] = static_cast<int>(
          (floor_div(best_left, SCALE) + 1) * SCALE
      );
      continue;
    }

    bool found = false;
    for (int exponent = 0; exponent <= SCALE_EXPONENT; ++exponent) {
      const int step = 1 << (SCALE_EXPONENT - exponent);
      const long long candidate =
          (floor_div(best_left, step) + 1) * step;
      if (candidate < best_right) {
        values[number] = static_cast<int>(candidate);
        found = true;
        break;
      }
    }
    assert(found);
  }
  return values;
}

std::string ternary(int number) {
  std::string result;
  while (number != 0) {
    result.push_back(static_cast<char>('0' + number % 3));
    number /= 3;
  }
  std::reverse(result.begin(), result.end());
  return result;
}

ComponentKey component_signature(
    int number,
    const std::vector<int>& binary_values
) {
  const std::string word = ternary(number);
  int binary_projection = 0;
  int twos = 0;
  bool before_first_one = true;
  std::vector<int> coefficients;

  for (const char trit : word) {
    if (trit == '2') {
      ++twos;
    } else {
      binary_projection = 2 * binary_projection + trit - '0';
      if (trit == '1') {
        before_first_one = false;
      } else if (before_first_one) {
        coefficients.push_back(twos);
      }
    }
  }

  assert(coefficients.size() <= MAX_COEFFICIENTS);
  u64 packed_coefficients = 0;
  for (int index = 0;
       index < static_cast<int>(coefficients.size());
       ++index) {
    const int coefficient =
        coefficients[coefficients.size() - index - 1];
    assert(coefficient < 16);
    packed_coefficients |=
        static_cast<u64>(coefficient) << (4 * index);
  }

  return {
      binary_values[binary_projection],
      packed_coefficients,
      static_cast<unsigned char>(twos & 1),
  };
}

SumKey add_signatures(
    const ComponentKey& first,
    const ComponentKey& second
) {
  u64 coefficients = 0;
  for (int index = 0; index < MAX_COEFFICIENTS; ++index) {
    const int sum =
        ((first.coefficients >> (4 * index)) & 15)
        + ((second.coefficients >> (4 * index)) & 15);
    assert(sum < 32);
    coefficients |= static_cast<u64>(sum) << (5 * index);
  }
  return {
      first.number + second.number,
      coefficients,
      static_cast<unsigned char>(first.nimber ^ second.nimber),
  };
}

struct ComponentClass {
  ComponentKey signature;
  u64 count;
};

u128 fair_settings(int limit) {
  const int maximum_digits = ternary(limit).size();
  assert(maximum_digits <= MAX_COEFFICIENTS + 1);
  const std::vector<int> binary_values =
      binary_game_values(maximum_digits);

  std::unordered_map<ComponentKey, u64, ComponentHash>
      component_counts;
  component_counts.reserve(limit / 16);
  for (int number = 1; number <= limit; ++number) {
    ++component_counts[
        component_signature(number, binary_values)
    ];
  }

  std::vector<ComponentClass> components;
  components.reserve(component_counts.size());
  for (const auto& [signature, count] : component_counts) {
    components.push_back({signature, count});
  }

  std::unordered_map<SumKey, u64, SumHash> paper_counts;
  paper_counts.reserve(1'000'000);
  for (std::size_t first = 0; first < components.size(); ++first) {
    for (std::size_t second = first;
         second < components.size();
         ++second) {
      const u64 count = first == second
          ? components[first].count
              * (components[first].count + 1) / 2
          : components[first].count * components[second].count;
      paper_counts[add_signatures(
          components[first].signature,
          components[second].signature
      )] += count;
    }
  }

  u128 result = 0;
  for (const auto& [signature, count] : paper_counts) {
    static_cast<void>(signature);
    result += static_cast<u128>(count) * count;
  }
  return result;
}

std::string decimal(u128 value) {
  std::string result;
  do {
    result.push_back(static_cast<char>('0' + value % 10));
    value /= 10;
  } while (value != 0);
  std::reverse(result.begin(), result.end());
  return result;
}

int main(int argc, char** argv) {
  const int limit = argc > 1 ? std::stoi(argv[1]) : LIMIT;
  assert(fair_settings(5) == 21);
  std::cout << decimal(fair_settings(limit)) << '\n';
}
