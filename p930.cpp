#include <array>
#include <cmath>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <vector>

using u64 = std::uint64_t;

class CompensatedSum {
 public:
  void add(long double value) {
    const long double adjusted = value - correction_;
    const long double next = value_ + adjusted;
    correction_ = (next - value_) - adjusted;
    value_ = next;
  }

  long double value() const {
    return value_;
  }

 private:
  long double value_ = 0;
  long double correction_ = 0;
};

class FourierModeCounter {
 public:
  FourierModeCounter(int bowls, int balls)
      : bowls_(bowls), balls_(balls), cosines_(bowls) {
    const long double pi = std::acos(-1.0L);
    for (int frequency = 0; frequency < bowls_; ++frequency) {
      cosines_[frequency] = std::cos(
          2 * pi * frequency / bowls_
      );
    }

    for (int n = 0; n <= balls_; ++n) {
      binomial_[n][0] = binomial_[n][n] = 1;
      for (int k = 1; k < n; ++k) {
        binomial_[n][k] =
            binomial_[n - 1][k - 1]
            + binomial_[n - 1][k];
      }
    }
  }

  long double expectation() {
    enumerate(
        0,
        balls_,
        0,
        0,
        0,
        1
    );
    return sum_.value();
  }

 private:
  int bowls_;
  int balls_;
  std::vector<long double> cosines_;
  std::array<std::array<u64, 13>, 13> binomial_{};
  CompensatedSum sum_;

  void enumerate(
      int frequency,
      int remaining,
      int frequency_sum,
      int nonzero_count,
      long double cosine_sum,
      u64 multiplicity
  ) {
    if (frequency == bowls_ - 1) {
      const int final_frequency_sum =
          (
              frequency_sum
              + frequency * remaining
          ) % bowls_;
      if (final_frequency_sum != 0) {
        return;
      }

      const int final_nonzero_count =
          nonzero_count
          + (frequency == 0 ? 0 : remaining);
      if (final_nonzero_count == 0) {
        return;
      }

      const long double final_cosine_sum =
          cosine_sum + remaining * cosines_[frequency];
      const long double eigenvalue =
          final_cosine_sum / balls_;
      sum_.add(
          multiplicity / (1 - eigenvalue)
      );
      return;
    }

    for (int count = 0; count <= remaining; ++count) {
      enumerate(
          frequency + 1,
          remaining - count,
          (
              frequency_sum + frequency * count
          ) % bowls_,
          nonzero_count
              + (frequency == 0 ? 0 : count),
          cosine_sum + count * cosines_[frequency],
          multiplicity * binomial_[remaining][count]
      );
    }
  }
};

long double expected_moves(int bowls, int balls) {
  return FourierModeCounter(bowls, balls).expectation();
}

long double summed_expectations(
    int maximum_bowls,
    int maximum_balls
) {
  CompensatedSum result;
  for (int bowls = 2; bowls <= maximum_bowls; ++bowls) {
    for (int balls = 2; balls <= maximum_balls; ++balls) {
      result.add(expected_moves(bowls, balls));
    }
  }
  return result.value();
}

bool approximately_equal(
    long double left,
    long double right,
    long double tolerance
) {
  return std::abs(left - right) <= tolerance;
}

int main() {
  if (
      !approximately_equal(expected_moves(2, 2), 0.5L, 1e-18L)
      || !approximately_equal(
          expected_moves(3, 2), 4.0L / 3, 1e-18L
      )
      || !approximately_equal(
          expected_moves(2, 3), 9.0L / 4, 1e-18L
      )
      || !approximately_equal(
          expected_moves(4, 5), 6875.0L / 24, 1e-15L
      )
      || !approximately_equal(
          summed_expectations(3, 3),
          137.0L / 12,
          1e-15L
      )
      || !approximately_equal(
          summed_expectations(4, 5),
          6277.0L / 12,
          1e-14L
      )
      || !approximately_equal(
          summed_expectations(6, 6),
          1.681521567954e4L,
          5e-9L
      )
  ) {
    std::cerr << "sample self-check failed\n";
    return 1;
  }

  std::cout
      << std::scientific
      << std::setprecision(12)
      << summed_expectations(12, 12)
      << '\n';
}
