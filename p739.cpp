#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <utility>
#include <vector>

static constexpr int MOD = 1'000'000'007;

static std::pair<int, int> fib_pair(long long n) {
  if (n == 0) return {0, 1};
  auto [a, b] = fib_pair(n / 2);
  long long c = 1LL * a * ((2LL * b - a + MOD) % MOD) % MOD;
  long long d = (1LL * a * a + 1LL * b * b) % MOD;
  if (n & 1) return {static_cast<int>(d), static_cast<int>((c + d) % MOD)};
  return {static_cast<int>(c), static_cast<int>(d)};
}

static int lucas(long long n) {
  auto [fn, fn1] = fib_pair(n);
  return static_cast<int>((2LL * fn1 - fn + MOD) % MOD);
}

static int solve(int n) {
  if (n == 1) return 1;

  std::vector<int> inverse(n + 1);
  inverse[1] = 1;
  for (int i = 2; i <= n; ++i) {
    inverse[i] = static_cast<int>(MOD - 1LL * (MOD / i) * inverse[MOD % i] % MOD);
  }

  long long weight = 1;
  long long current_lucas = lucas(n);
  long long previous_lucas = lucas(n - 1);
  long long answer = 0;

  for (int k = n; k >= 2; --k) {
    answer = (answer + weight * current_lucas) % MOD;

    if (k > 2) {
      weight = weight * (k - 2) % MOD;
      weight = weight * inverse[k - 1] % MOD;
      weight = weight * (2LL * n - k - 1) % MOD;
      weight = weight * inverse[n - k + 1] % MOD;

      long long next_lucas = (current_lucas - previous_lucas + MOD) % MOD;
      current_lucas = previous_lucas;
      previous_lucas = next_lucas;
    }
  }

  return static_cast<int>(answer);
}

int main(int argc, char** argv) {
  int n = 100'000'000;
  if (argc > 1) n = std::atoi(argv[1]);
  std::cout << solve(n) << '\n';
  return 0;
}
