#include <cmath>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>

static constexpr int MOD = 1'000'000'007;
static constexpr long long TARGET = 100'000'000'000'000LL;

static int solve_for(long long n) {
  int limit = static_cast<int>(std::sqrt(static_cast<long double>(n)));
  while (1LL * (limit + 1) * (limit + 1) <= n) ++limit;
  while (1LL * limit * limit > n) --limit;

  std::vector<int> jordan(limit + 1, 0);
  std::vector<int> primes;
  std::vector<char> composite(limit + 1, 0);
  jordan[1] = 1;

  for (int i = 2; i <= limit; ++i) {
    if (!composite[i]) {
      primes.push_back(i);
      jordan[i] = static_cast<int>((1LL * i * i - 1) % MOD);
    }
    for (int p : primes) {
      long long v = 1LL * i * p;
      if (v > limit) break;
      composite[static_cast<std::size_t>(v)] = 1;
      if (i % p == 0) {
        jordan[static_cast<std::size_t>(v)] = static_cast<int>(1LL * jordan[i] * p % MOD * p % MOD);
        break;
      }
      jordan[static_cast<std::size_t>(v)] = static_cast<int>(1LL * jordan[i] * ((1LL * p * p - 1) % MOD) % MOD);
    }
  }

  long long answer = n % MOD;  // m=1
  for (int m = 2; m <= limit; ++m) {
    answer += 1LL * jordan[m] * (n / (1LL * m * m) % MOD) % MOD;
    if (answer >= MOD) answer -= MOD;
  }
  return static_cast<int>(answer);
}

int main(int argc, char **argv) {
  long long n = TARGET;
  if (argc > 1) {
    n = std::stoll(argv[1]);
  }
  std::cout << solve_for(n) << '\n';
  return 0;
}
