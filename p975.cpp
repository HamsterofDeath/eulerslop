#include <algorithm>
#include <array>
#include <cassert>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>

constexpr long double PI =
    3.141592653589793238462643383279502884L;
constexpr long double HEIGHT_TOLERANCE = 1e-14L;

struct Landscape {
  std::vector<long double> values;
  std::vector<int> slopes;
};

long double height(int a, int b, long double x) {
  if (x == 0) {
    return 0;
  }
  if (x == 1) {
    return 1;
  }
  return 0.5L - (
      b * std::cos(a * PI * x)
      + a * std::cos(b * PI * x)
  ) / (2.0L * (a + b));
}

Landscape make_landscape(int a, int b) {
  const int sum_frequency = (a + b) / 2;
  const int difference_frequency = std::abs(a - b) / 2;
  std::vector<long double> candidates{0, 1};

  for (int index = 1; index < sum_frequency; ++index) {
    candidates.push_back(
        static_cast<long double>(index) / sum_frequency
    );
  }
  for (int index = 0;
       index < difference_frequency;
       ++index) {
    candidates.push_back(
        static_cast<long double>(2 * index + 1)
        / (2 * difference_frequency)
    );
  }
  std::sort(candidates.begin(), candidates.end());

  std::vector<long double> distinct;
  for (const long double candidate : candidates) {
    if (
        distinct.empty()
        || std::abs(candidate - distinct.back()) > 1e-18L
    ) {
      distinct.push_back(candidate);
    }
  }

  std::vector<int> interval_signs;
  for (std::size_t index = 1; index < distinct.size(); ++index) {
    const long double middle =
        (distinct[index - 1] + distinct[index]) / 2;
    const long double derivative_sign =
        std::sin(sum_frequency * PI * middle)
        * std::cos(difference_frequency * PI * middle);
    assert(std::abs(derivative_sign) > 1e-16L);
    interval_signs.push_back(derivative_sign > 0 ? 1 : -1);
  }

  std::vector<long double> turning_points{0};
  for (std::size_t index = 1;
       index + 1 < distinct.size();
       ++index) {
    if (interval_signs[index - 1] != interval_signs[index]) {
      turning_points.push_back(distinct[index]);
    }
  }
  turning_points.push_back(1);

  Landscape landscape;
  for (const long double point : turning_points) {
    landscape.values.push_back(height(a, b, point));
  }
  for (std::size_t index = 1;
       index < landscape.values.size();
       ++index) {
    landscape.slopes.push_back(
        landscape.values[index]
                > landscape.values[index - 1]
            ? 1
            : -1
    );
  }
  return landscape;
}

long double lower_height(
    const Landscape& landscape,
    int segment
) {
  return std::min(
      landscape.values[segment],
      landscape.values[segment + 1]
  );
}

long double upper_height(
    const Landscape& landscape,
    int segment
) {
  return std::max(
      landscape.values[segment],
      landscape.values[segment + 1]
  );
}

long double path_variation(
    int a,
    int b,
    int c,
    int d
) {
  const Landscape first = make_landscape(a, b);
  const Landscape second = make_landscape(c, d);

  int first_segment = 0;
  int second_segment = 0;
  int first_direction = 1;
  int second_direction = 1;
  long double current_height = 0;
  long double variation = 0;

  const int maximum_steps = static_cast<int>(
      4 * first.slopes.size() * second.slopes.size() + 10
  );
  for (int step = 0; step < maximum_steps; ++step) {
    const int height_direction =
        first.slopes[first_segment] * first_direction;
    assert(
        height_direction
        == second.slopes[second_segment] * second_direction
    );

    long double next_height;
    if (height_direction > 0) {
      next_height = std::min(
          upper_height(first, first_segment),
          upper_height(second, second_segment)
      );
    } else {
      next_height = std::max(
          lower_height(first, first_segment),
          lower_height(second, second_segment)
      );
    }
    variation += std::abs(next_height - current_height);
    current_height = next_height;

    const long double first_boundary = height_direction > 0
        ? upper_height(first, first_segment)
        : lower_height(first, first_segment);
    const long double second_boundary = height_direction > 0
        ? upper_height(second, second_segment)
        : lower_height(second, second_segment);
    const bool hits_first =
        std::abs(next_height - first_boundary) < HEIGHT_TOLERANCE;
    const bool hits_second =
        std::abs(next_height - second_boundary) < HEIGHT_TOLERANCE;
    assert(hits_first || hits_second);

    const int next_first =
        first_segment + first_direction;
    const int next_second =
        second_segment + second_direction;
    if (
        (hits_first && (
            next_first < 0
            || next_first >= static_cast<int>(first.slopes.size())
        ))
        || (hits_second && (
            next_second < 0
            || next_second >= static_cast<int>(second.slopes.size())
        ))
    ) {
      assert(hits_first && hits_second);
      assert(std::abs(current_height - 1) < HEIGHT_TOLERANCE);
      return variation;
    }

    if (hits_first) {
      first_segment = next_first;
    }
    if (hits_second) {
      second_segment = next_second;
    }
    if (hits_first != hits_second) {
      if (hits_first) {
        second_direction = -second_direction;
      } else {
        first_direction = -first_direction;
      }
    }
  }
  assert(false && "path trace did not terminate");
  return 0;
}

std::vector<int> primes_in_range(int minimum, int maximum) {
  std::vector<bool> is_prime(maximum + 1, true);
  is_prime[0] = is_prime[1] = false;
  for (int prime = 2; prime * prime <= maximum; ++prime) {
    if (is_prime[prime]) {
      for (int multiple = prime * prime;
           multiple <= maximum;
           multiple += prime) {
        is_prime[multiple] = false;
      }
    }
  }

  std::vector<int> primes;
  for (int value = minimum; value <= maximum; ++value) {
    if (is_prime[value]) {
      primes.push_back(value);
    }
  }
  return primes;
}

long double sum_variations(int minimum, int maximum) {
  const std::vector<int> primes =
      primes_in_range(minimum, maximum);
  long double result = 0;
  for (std::size_t first = 0; first < primes.size(); ++first) {
    for (std::size_t second = first + 1;
         second < primes.size();
         ++second) {
      const int p = primes[first];
      const int q = primes[second];
      result += path_variation(p, q, p, 2 * q - p);
    }
  }
  return result;
}

int main(int argc, char** argv) {
  assert(
      std::abs(path_variation(3, 5, 3, 7) - 7.01772L)
      < 5e-6L
  );
  assert(
      std::abs(path_variation(7, 17, 9, 19) - 26.79578L)
      < 5e-6L
  );
  assert(
      std::abs(sum_variations(3, 20) - 463.80866L)
      < 5e-6L
  );

  if (argc == 5) {
    std::cout << std::fixed << std::setprecision(10)
              << path_variation(
                     std::stoi(argv[1]),
                     std::stoi(argv[2]),
                     std::stoi(argv[3]),
                     std::stoi(argv[4])
                 )
              << '\n';
  } else {
    std::cout << std::fixed << std::setprecision(5)
              << sum_variations(500, 1000) << '\n';
  }
}
