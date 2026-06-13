#include <algorithm>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>

static constexpr int MOD = 1'000'000'007;
static constexpr int TARGET = 10'000'000;

static long long mod_pow(long long base, long long exp) {
  long long result = 1;
  while (exp > 0) {
    if (exp & 1) result = result * base % MOD;
    base = base * base % MOD;
    exp >>= 1;
  }
  return result;
}

static std::vector<int> totients(int n) {
  std::vector<int> phi(n + 1);
  std::vector<int> primes;
  std::vector<char> composite(n + 1, 0);
  phi[1] = 1;
  for (int i = 2; i <= n; ++i) {
    if (!composite[i]) {
      primes.push_back(i);
      phi[i] = i - 1;
    }
    for (int p : primes) {
      long long v = 1LL * i * p;
      if (v > n) break;
      composite[static_cast<std::size_t>(v)] = 1;
      if (i % p == 0) {
        phi[static_cast<std::size_t>(v)] = phi[i] * p;
        break;
      }
      phi[static_cast<std::size_t>(v)] = phi[i] * (p - 1);
    }
  }
  return phi;
}

static int solve_for(int n) {
  std::vector<int> phi = totients(n);
  std::vector<int> pow2(n + 1, 1);
  for (int i = 1; i <= n; ++i) {
    pow2[i] = static_cast<int>(2LL * pow2[i - 1] % MOD);
  }

  std::vector<int> prefix(n + 1, 1);
  for (int q = 2; q <= n; ++q) {
    int value = pow2[q - 1] - 1;
    if (value < 0) value += MOD;
    prefix[q] = static_cast<int>(1LL * prefix[q - 1] * value % MOD);
  }

  long long inverse_suffix = mod_pow(prefix[n], MOD - 2);
  long long answer = 2LL * n % MOD;  // q=1 contributes F(n,n)=2 for every n.
  const long long inv2 = (MOD + 1LL) / 2;

  for (int q = n; q >= 2; --q) {
    int value = pow2[q - 1] - 1;
    if (value < 0) value += MOD;
    long long inverse_value = inverse_suffix * prefix[q - 1] % MOD;
    inverse_suffix = inverse_suffix * value % MOD;

    int m = n / q;
    long long ratio = pow2[q - 1];
    long long ratio_to_m = pow2[static_cast<std::size_t>((q - 1LL) * m)];
    long long geometric = ratio * ((ratio_to_m - 1 + MOD) % MOD) % MOD * inverse_value % MOD;

    long long coefficient;
    if (q & 1) {
      coefficient = 3LL * phi[q] % MOD * inv2 % MOD;
    } else {
      coefficient = 2LL * phi[q] % MOD;
    }
    answer += coefficient * geometric % MOD;
    if (answer >= MOD) answer -= MOD;
  }

  return static_cast<int>(answer % MOD);
}

int main(int argc, char **argv) {
  int n = TARGET;
  if (argc > 1) {
    n = std::stoi(argv[1]);
  }
  std::cout << solve_for(n) << '\n';
  return 0;
}
