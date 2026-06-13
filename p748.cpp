#include <algorithm>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <string>

static constexpr long long TARGET = 10'000'000'000'000'000LL;
static constexpr long long MOD = 1'000'000'000LL;

static long long isqrtll(long long n) {
  long long r = static_cast<long long>(std::sqrt(static_cast<long double>(n)));
  while ((__int128)(r + 1) * (r + 1) <= n) ++r;
  while ((__int128)r * r > n) --r;
  return r;
}

static long long solve_for(long long limit) {
  long long c_limit = isqrtll(limit);
  int parameter_limit = static_cast<int>(isqrtll(c_limit)) + 2;
  long long answer = 0;

  for (int m = 1; m <= parameter_limit; ++m) {
    for (int n = 0; n < m; ++n) {
      if (((m + n) & 1) == 0 || std::gcd(m, n) != 1) continue;
      long long c = 1LL * m * m + 1LL * n * n;
      if (c > c_limit) continue;

      int first_sign = 1;
      int last_sign = (n == 0 ? 1 : -1);
      for (int sign = first_sign; sign >= last_sign; sign -= 2) {
        long long real = 1LL * m * m - 1LL * n * n;
        long long imag = 2LL * m * n;
        long long a = std::llabs(3 * real - 2LL * sign * imag);
        long long b = std::llabs(2LL * sign * real + 3 * imag);
        if (a == 0 || b == 0) continue;
        if (a > b) std::swap(a, b);

        long long x = a * c;
        long long y = b * c;
        long long z = a * b;
        if (x > limit || y > limit || z > limit) continue;
        if (std::gcd(std::gcd(x, y), z) != 1) continue;

        answer = (answer + x % MOD + y % MOD + z % MOD) % MOD;
      }
    }
  }

  return answer;
}

int main(int argc, char **argv) {
  long long limit = TARGET;
  if (argc > 1) {
    limit = std::stoll(argv[1]);
  }
  std::cout << solve_for(limit) << '\n';
  return 0;
}
