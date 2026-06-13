#include <algorithm>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <vector>

static constexpr long long MOD = 1'000'000'007LL;
static constexpr long double LOG2 = 0.693147180559945309417232121458176568L;

static long long mod_pow(long long base, long long exponent) {
  long long result = 1;
  while (exponent > 0) {
    if (exponent & 1) result = static_cast<__int128>(result) * base % MOD;
    base = static_cast<__int128>(base) * base % MOD;
    exponent >>= 1;
  }
  return result;
}

static long long inverse(long long value) { return mod_pow(value, MOD - 2); }

static long long pow2_mod(long long exponent) { return mod_pow(2, exponent); }

static long long mersenne_mod(long long exponent) {
  long long value = pow2_mod(exponent) - 1;
  return value < 0 ? value + MOD : value;
}

static long long quotient_mod(long long m, long long n) {
  long long quotient = m / n;
  long long remainder = m % n;
  long long ratio = pow2_mod(n);
  long long geometric;
  if (ratio == 1) {
    geometric = quotient % MOD;
  } else {
    geometric = (mod_pow(ratio, quotient) - 1 + MOD) % MOD;
    geometric = geometric * inverse((ratio - 1 + MOD) % MOD) % MOD;
  }
  return pow2_mod(remainder) * geometric % MOD;
}

static long double log_add(long double a, long double b) {
  if (a == -INFINITY) return b;
  if (b == -INFINITY) return a;
  if (a < b) std::swap(a, b);
  return a + std::log1p(std::exp(b - a));
}

struct Coefficient {
  long long mod;
  int sign;
  long double log_abs;
};

static long long pair_value(long long small_exp, long long large_exp) {
  long long r0 = large_exp;
  long long r1 = small_exp;
  Coefficient t0{0, 0, -INFINITY};
  Coefficient t1{1, 1, 0.0L};

  while (r1 != 1) {
    long long qmod = quotient_mod(r0, r1);
    long double qlog = static_cast<long double>(r0 - r1) * LOG2;
    Coefficient t2;
    t2.mod = (t0.mod - qmod * t1.mod) % MOD;
    if (t2.mod < 0) t2.mod += MOD;
    t2.sign = -t1.sign;
    t2.log_abs = log_add(t0.log_abs, qlog + t1.log_abs);
    long long r2 = r0 % r1;
    r0 = r1;
    r1 = r2;
    t0 = t1;
    t1 = t2;
  }

  long long a = mersenne_mod(small_exp);
  long long b = mersenne_mod(large_exp);
  long long x_plus = t1.mod;
  if (t1.sign < 0) x_plus = (x_plus + b) % MOD;
  long long y_plus = (static_cast<__int128>(a) * x_plus % MOD - 1 + MOD) % MOD;
  y_plus = y_plus * inverse(b) % MOD;
  long long sum_plus = (x_plus + y_plus) % MOD;
  long long sum_minus = (a + b - sum_plus) % MOD;
  if (sum_minus < 0) sum_minus += MOD;

  long double log_b_half = static_cast<long double>(large_exp) * LOG2 - LOG2;
  bool abs_less_half = t1.log_abs < log_b_half;
  bool plus_has_smaller_sum = t1.sign > 0 ? abs_less_half : !abs_less_half;
  long long chosen = plus_has_smaller_sum ? sum_plus : sum_minus;
  return (2 * ((chosen - 1 + MOD) % MOD)) % MOD;
}

static std::vector<int> primes_below(int limit) {
  std::vector<int> primes;
  for (int n = 2; n < limit; ++n) {
    bool prime = true;
    for (int d = 2; d * d <= n; ++d) {
      if (n % d == 0) {
        prime = false;
        break;
      }
    }
    if (prime) primes.push_back(n);
  }
  return primes;
}

int main() {
  auto primes = primes_below(1000);
  std::vector<long long> exponents;
  for (int p : primes) {
    long long p2 = 1LL * p * p;
    exponents.push_back(p2 * p2 * p);
  }

  long long answer = 0;
  for (std::size_t i = 0; i < exponents.size(); ++i) {
    for (std::size_t j = i + 1; j < exponents.size(); ++j) {
      answer += pair_value(exponents[i], exponents[j]);
      answer %= MOD;
    }
  }
  std::cout << answer << '\n';
  return 0;
}
