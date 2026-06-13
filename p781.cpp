#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>

static constexpr std::int64_t MOD = 1000000007LL;

static std::int64_t mod_pow(std::int64_t a, std::int64_t e) {
  std::int64_t r = 1;
  while (e > 0) {
    if (e & 1) r = r * a % MOD;
    a = a * a % MOD;
    e >>= 1;
  }
  return r;
}

static std::int64_t solve(int n) {
  const int m = n / 2;
  std::vector<std::int64_t> fact(n + 1), inv_fact(n + 1), der(n + 1);
  fact[0] = 1;
  for (int i = 1; i <= n; ++i) fact[i] = fact[i - 1] * i % MOD;
  inv_fact[n] = mod_pow(fact[n], MOD - 2);
  for (int i = n; i > 0; --i) inv_fact[i - 1] = inv_fact[i] * i % MOD;

  der[0] = 1;
  if (n >= 1) der[1] = 0;
  for (int i = 2; i <= n; ++i) {
    der[i] = (i - 1LL) * (der[i - 1] + der[i - 2]) % MOD;
  }

  std::vector<std::int64_t> reciprocal_pow2(m + 1), inv_fact_m(m + 1);
  const std::int64_t inv2 = (MOD + 1) / 2;
  reciprocal_pow2[0] = 1;
  inv_fact_m[0] = 1;
  for (int i = 1; i <= m; ++i) {
    reciprocal_pow2[i] = reciprocal_pow2[i - 1] * inv2 % MOD;
    inv_fact_m[i] = inv_fact_m[i - 1] * mod_pow(i, MOD - 2) % MOD;
  }

  std::vector<std::int64_t> e_prefix(n + 1);
  for (int i = 0; i <= n; ++i) {
    e_prefix[i] = (i == 0 ? 0 : e_prefix[i - 1]);
    e_prefix[i] = (e_prefix[i] + der[i] * inv_fact[i]) % MOD;
  }

  std::vector<std::int64_t> a(m + 1), b(m + 1), d(m + 1);
  for (int i = 0; i <= m; ++i) {
    const int vertices = 2 * i;
    const std::int64_t matching =
        fact[vertices] * reciprocal_pow2[i] % MOD * inv_fact_m[i] % MOD;
    a[i] = der[vertices] * reciprocal_pow2[i] % MOD * inv_fact_m[i] % MOD;
    b[i] = matching * e_prefix[vertices] % MOD;
  }

  for (int i = 0; i <= m; ++i) {
    std::int64_t value = b[i];
    for (int j = 0; j < i; ++j) {
      value -= d[j] * a[i - j] % MOD;
      if (value < 0) value += MOD;
    }
    d[i] = value;
  }
  return d[m];
}

int main(int argc, char** argv) {
  int n = 50000;
  if (argc > 1) n = std::atoi(argv[1]);
  std::cout << solve(n) << '\n';
  return 0;
}
