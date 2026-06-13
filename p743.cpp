#include <iostream>
#include <string>
#include <vector>

static constexpr int MOD = 1'000'000'007;
static constexpr int TARGET_K = 100'000'000;
static constexpr long long TARGET_N = 10'000'000'000'000'000LL;

static long long mod_pow(long long base, long long exp) {
  long long result = 1;
  while (exp > 0) {
    if (exp & 1) result = result * base % MOD;
    base = base * base % MOD;
    exp >>= 1;
  }
  return result;
}

static int coefficient(int k, long long n) {
  long long periods = n / k;
  int middle = k / 2;
  long long a = mod_pow(2, periods);
  long long term = mod_pow(a, k);
  long long answer = term;
  long long inv_a2 = mod_pow(a * a % MOD, MOD - 2);

  std::vector<int> inverses(middle + 2);
  inverses[1] = 1;
  for (int i = 2; i <= middle + 1; ++i) {
    inverses[i] = static_cast<int>(MOD - (MOD / i) * 1LL * inverses[MOD % i] % MOD);
  }

  for (int t = 0; t < middle; ++t) {
    long long remaining = k - 2LL * t;
    long long ratio = remaining % MOD * ((remaining - 1) % MOD) % MOD;
    ratio = ratio * inverses[t + 1] % MOD * inverses[t + 1] % MOD * inv_a2 % MOD;
    term = term * ratio % MOD;
    answer += term;
    if (answer >= MOD) answer -= MOD;
  }

  return static_cast<int>(answer);
}

int main(int argc, char **argv) {
  int k = TARGET_K;
  long long n = TARGET_N;
  if (argc > 2) {
    k = std::stoi(argv[1]);
    n = std::stoll(argv[2]);
  }
  std::cout << coefficient(k, n) << '\n';
  return 0;
}
