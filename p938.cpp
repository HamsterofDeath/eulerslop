#include <cmath>
#include <iomanip>
#include <iostream>

long double black_probability(int red, int black) {
  if (red == 0) {
    return 1;
  }
  if (black == 0 || (red & 1)) {
    return 0;
  }

  const int red_pairs = red / 2;
  long double logarithm = 0;
  for (int index = 0; index < black; ++index) {
    logarithm -= std::log1p(
        0.5L / (red_pairs + index)
    );
  }
  return 1 - std::exp(logarithm);
}

bool approximately_equal(
    long double left,
    long double right
) {
  return std::abs(left - right) < 5e-11L;
}

int main() {
  if (
      !approximately_equal(
          black_probability(2, 2),
          0.4666666667L
      )
      || !approximately_equal(
          black_probability(10, 9),
          0.4118903397L
      )
      || !approximately_equal(
          black_probability(34, 25),
          0.3665688069L
      )
  ) {
    std::cerr << "sample self-check failed\n";
    return 1;
  }

  std::cout
      << std::fixed
      << std::setprecision(10)
      << black_probability(24'690, 12'345)
      << '\n';
}
