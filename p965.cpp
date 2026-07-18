#include <algorithm>
#include <cassert>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <string>

constexpr int LIMIT = 10'000;

long double expected_minimum(int limit) {
  long double result = 0;

  // Consecutive Farey denominators b,d are precisely the ordered
  // coprime pairs at most N for which b+d>N.  Combining (b,d) and
  // (d,b) halves the enumeration.
  for (int d = 2; d <= limit; ++d) {
    const int first_b = std::max(1, limit - d + 1);
    for (int b = first_b; b < d; ++b) {
      if (std::gcd(b, d) != 1) {
        continue;
      }
      const long double bd =
          static_cast<long double>(b) * d;
      result += static_cast<long double>(b + d)
          / (2 * bd * bd);
    }
  }

  // The only diagonal coprime pair is (1,1), relevant for N=1.
  if (limit == 1) {
    result += 0.5L;
  }
  return result;
}

int main(int argc, char** argv) {
  const int limit = argc > 1 ? std::stoi(argv[1]) : LIMIT;
  assert(expected_minimum(1) == 0.5L);
  assert(expected_minimum(4) == 0.25L);
  std::cout << std::fixed << std::setprecision(13)
            << expected_minimum(limit) << '\n';
}
