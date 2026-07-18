#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <vector>

using i64 = std::int64_t;
using u64 = std::uint64_t;

constexpr u64 TARGET_COEFFICIENTS = 100'000'000;

struct Matrix {
  i64 a;
  i64 b;
  i64 c;
  i64 d;

  bool operator==(const Matrix& other) const {
    return a == other.a && b == other.b
           && c == other.c && d == other.d;
  }
};

void normalize(Matrix& matrix) {
  i64 common = 0;
  common = std::gcd(common, std::abs(matrix.a));
  common = std::gcd(common, std::abs(matrix.b));
  common = std::gcd(common, std::abs(matrix.c));
  common = std::gcd(common, std::abs(matrix.d));
  matrix.a /= common;
  matrix.b /= common;
  matrix.c /= common;
  matrix.d /= common;
}

std::vector<i64> consume_digit(Matrix& matrix, i64 digit) {
  matrix = {
      matrix.a * digit + matrix.b, matrix.a,
      matrix.c * digit + matrix.d, matrix.c
  };

  std::vector<i64> output;
  while (
      matrix.c != 0 && matrix.d != 0
      && matrix.a / matrix.c == matrix.b / matrix.d
  ) {
    const i64 coefficient = matrix.a / matrix.c;
    output.push_back(coefficient);
    matrix = {
        matrix.c, matrix.d,
        matrix.a - coefficient * matrix.c,
        matrix.b - coefficient * matrix.d
    };
    normalize(matrix);
  }
  return output;
}

struct Accumulator {
  u64 target;
  u64 count = 0;
  u64 sum = 0;

  bool add(const std::vector<i64>& coefficients) {
    for (i64 coefficient : coefficients) {
      if (count == target) {
        break;
      }
      ++count;
      sum += coefficient;
    }
    return count == target;
  }
};

struct Snapshot {
  Matrix state;
  u64 position;
  u64 count;
  u64 sum;
};

void consume_ones(Matrix& matrix, u64 run_length, Accumulator& result) {
  std::vector<Snapshot> seen;
  u64 position = 0;

  while (position < run_length && result.count < result.target) {
    const auto repeated = std::find_if(
        seen.begin(), seen.end(),
        [&](const Snapshot& snapshot) {
          return snapshot.state == matrix;
        }
    );
    if (repeated != seen.end()) {
      const u64 cycle_input = position - repeated->position;
      const u64 cycle_output = result.count - repeated->count;
      const u64 cycle_sum = result.sum - repeated->sum;
      u64 repetitions = (run_length - position) / cycle_input;
      if (cycle_output != 0) {
        repetitions = std::min(
            repetitions,
            (result.target - result.count) / cycle_output
        );
      }
      if (repetitions != 0) {
        position += repetitions * cycle_input;
        result.count += repetitions * cycle_output;
        result.sum += repetitions * cycle_sum;
        seen.clear();
        continue;
      }
    } else {
      seen.push_back({matrix, position, result.count, result.sum});
    }

    result.add(consume_digit(matrix, 1));
    ++position;
  }
}

bool is_prime(int candidate, const std::vector<int>& primes) {
  for (int prime : primes) {
    if (prime * prime > candidate) {
      break;
    }
    if (candidate % prime == 0) {
      return false;
    }
  }
  return true;
}

u64 coefficient_sum(u64 wanted) {
  Matrix transform{2, 3, 3, 2};
  Accumulator result{wanted};

  // The first coefficient of alpha is 2.
  result.add(consume_digit(transform, 2));

  std::vector<int> primes;
  for (int candidate = 2; result.count < wanted;
       candidate += candidate == 2 ? 1 : 2) {
    if (!is_prime(candidate, primes)) {
      continue;
    }
    primes.push_back(candidate);
    consume_ones(transform, candidate, result);
    if (result.count < wanted) {
      result.add(consume_digit(transform, 2));
    }
  }
  return result.sum;
}

int main() {
  if (coefficient_sum(10) != 75) {
    std::cerr << "sample self-check failed\n";
    return 1;
  }
  std::cout << coefficient_sum(TARGET_COEFFICIENTS) << '\n';
}
