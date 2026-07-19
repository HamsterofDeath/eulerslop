#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <unordered_map>
#include <vector>

using u32 = std::uint32_t;
using u64 = std::uint64_t;

constexpr int MODULUS = 1'000'000'007;
constexpr int MAX_LENGTH = 50;
constexpr int MAX_TERMS = 25;

using Polynomial = std::vector<int>;
using DigitWays =
    std::array<std::array<Polynomial, MAX_TERMS + 1>, MAX_TERMS + 1>;

int add_mod(int first, int second) {
  const int sum = first + second;
  return sum >= MODULUS ? sum - MODULUS : sum;
}

int multiply_mod(int first, int second) {
  return static_cast<int>(static_cast<u64>(first) * second % MODULUS);
}

Polynomial multiply_by_digit_range(const Polynomial& polynomial,
                                   int first_digit) {
  Polynomial result(polynomial.size() + 9);
  for (int degree = 0; degree < static_cast<int>(polynomial.size());
       ++degree) {
    for (int digit = first_digit; digit <= 9; ++digit) {
      result[degree + digit] =
          add_mod(result[degree + digit], polynomial[degree]);
    }
  }
  return result;
}

DigitWays make_digit_ways() {
  std::array<std::array<int, MAX_TERMS + 1>, MAX_TERMS + 1>
      binomial{};
  binomial[0][0] = 1;
  for (int n = 1; n <= MAX_TERMS; ++n) {
    binomial[n][0] = binomial[n][n] = 1;
    for (int k = 1; k < n; ++k) {
      binomial[n][k] =
          add_mod(binomial[n - 1][k - 1], binomial[n - 1][k]);
    }
  }

  DigitWays ways;
  for (int active = 0; active <= MAX_TERMS; ++active) {
    for (int ending = 0; ending <= active; ++ending) {
      Polynomial polynomial(1, 1);
      for (int index = 0; index < ending; ++index) {
        polynomial = multiply_by_digit_range(polynomial, 1);
      }
      for (int index = ending; index < active; ++index) {
        polynomial = multiply_by_digit_range(polynomial, 0);
      }
      for (int& coefficient : polynomial) {
        coefficient = multiply_mod(coefficient,
                                   binomial[active][ending]);
      }
      ways[active][ending] = std::move(polynomial);
    }
  }
  return ways;
}

u32 difference_key(int left_active, int left_ending,
                   int right_active, int right_ending) {
  return static_cast<u32>(left_active)
         | static_cast<u32>(left_ending) << 5
         | static_cast<u32>(right_active) << 10
         | static_cast<u32>(right_ending) << 15;
}

class DifferenceCache {
 public:
  explicit DifferenceCache(const DigitWays& digit_ways)
      : digit_ways_(digit_ways) {}

  const Polynomial& get(int left_active, int left_ending,
                        int right_active, int right_ending) {
    const u32 key = difference_key(left_active, left_ending,
                                   right_active, right_ending);
    const auto found = cache_.find(key);
    if (found != cache_.end()) {
      return found->second;
    }

    const Polynomial& left = digit_ways_[left_active][left_ending];
    const Polynomial& right = digit_ways_[right_active][right_ending];
    Polynomial difference(9 * (left_active + right_active) + 1);
    const int right_offset = 9 * right_active;

    for (int left_sum = 0;
         left_sum < static_cast<int>(left.size()); ++left_sum) {
      if (left[left_sum] == 0) {
        continue;
      }
      for (int right_sum = 0;
           right_sum < static_cast<int>(right.size()); ++right_sum) {
        if (right[right_sum] == 0) {
          continue;
        }
        const int index = left_sum - right_sum + right_offset;
        difference[index] =
            add_mod(difference[index],
                    multiply_mod(left[left_sum], right[right_sum]));
      }
    }

    return cache_.emplace(key, std::move(difference)).first->second;
  }

 private:
  const DigitWays& digit_ways_;
  std::unordered_map<u32, Polynomial> cache_;
};

u32 state_key(int left_active, int right_active, int carry) {
  assert(carry >= -32 && carry < 32);
  return static_cast<u32>(left_active)
         | static_cast<u32>(right_active) << 5
         | static_cast<u32>(carry + 32) << 10;
}

void unpack_state(u32 key, int& left_active, int& right_active,
                  int& carry) {
  left_active = key & 31;
  right_active = (key >> 5) & 31;
  carry = static_cast<int>((key >> 10) & 63) - 32;
}

void add_to_state(std::unordered_map<u32, int>& layer, u32 key,
                  int value) {
  auto [entry, inserted] = layer.emplace(key, value);
  if (!inserted) {
    entry->second = add_mod(entry->second, value);
  }
}

int count_equations(int length_limit) {
  const DigitWays digit_ways = make_digit_ways();
  DifferenceCache differences(digit_ways);
  std::array<std::unordered_map<u32, int>, MAX_LENGTH + 1> layers;
  std::array<int, MAX_LENGTH + 1> exact{};

  const int term_limit = (length_limit + 1) / 2;
  for (int left_terms = 1; left_terms <= term_limit; ++left_terms) {
    for (int right_terms = 1;
         left_terms + right_terms <= term_limit; ++right_terms) {
      const int operator_length = left_terms + right_terms - 1;
      add_to_state(layers[operator_length],
                   state_key(left_terms, right_terms, 0), 1);
    }
  }

  for (int length = 1; length <= length_limit; ++length) {
    for (const auto& [key, state_ways] : layers[length]) {
      int left_active;
      int right_active;
      int carry;
      unpack_state(key, left_active, right_active, carry);

      const int next_length = length + left_active + right_active;
      if (next_length > length_limit) {
        continue;
      }

      for (int left_ending = 0; left_ending <= left_active;
           ++left_ending) {
        const int next_left = left_active - left_ending;
        for (int right_ending = 0; right_ending <= right_active;
             ++right_ending) {
          const int next_right = right_active - right_ending;
          const Polynomial& difference =
              differences.get(left_active, left_ending,
                              right_active, right_ending);
          const int offset = 9 * right_active;
          const int minimum = -offset;
          const int maximum = 9 * left_active;

          int digit_difference = minimum;
          const int remainder =
              ((-carry - digit_difference) % 10 + 10) % 10;
          digit_difference += remainder;
          for (; digit_difference <= maximum;
               digit_difference += 10) {
            const int coefficient =
                difference[digit_difference + offset];
            if (coefficient == 0) {
              continue;
            }
            const int next_carry =
                (carry + digit_difference) / 10;
            const int contribution =
                multiply_mod(state_ways, coefficient);

            if (next_left == 0 && next_right == 0) {
              if (next_carry == 0) {
                exact[next_length] =
                    add_mod(exact[next_length], contribution);
              }
            } else {
              add_to_state(layers[next_length],
                           state_key(next_left, next_right,
                                     next_carry),
                           contribution);
            }
          }
        }
      }
    }
  }

  int answer = 0;
  for (int length = 1; length <= length_limit; ++length) {
    answer = add_mod(answer, exact[length]);
  }
  return answer;
}

int main() {
  assert(count_equations(3) == 9);
  assert(count_equations(5) == 171);
  assert(count_equations(7) == 4878);
  std::cout << count_equations(50) << '\n';
}
