#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>

static constexpr int MOD = 1'000'000'007;

static int mod_pow(long long base, long long exponent) {
  long long result = 1;
  while (exponent > 0) {
    if (exponent & 1) result = result * base % MOD;
    base = base * base % MOD;
    exponent >>= 1;
  }
  return static_cast<int>(result);
}

static std::vector<int> mertens_prefix(int limit) {
  std::vector<int> least_prime(limit + 1, 0);
  std::vector<int> primes;
  std::vector<signed char> mu(limit + 1, 0);
  std::vector<int> prefix(limit + 1, 0);

  mu[1] = 1;
  for (int n = 2; n <= limit; ++n) {
    if (least_prime[n] == 0) {
      least_prime[n] = n;
      primes.push_back(n);
      mu[n] = -1;
    }
    for (int p : primes) {
      long long next = 1LL * n * p;
      if (next > limit) break;
      least_prime[static_cast<int>(next)] = p;
      if (p == least_prime[n]) {
        mu[static_cast<int>(next)] = 0;
        break;
      }
      mu[static_cast<int>(next)] = -mu[n];
    }
  }

  for (int n = 1; n <= limit; ++n) {
    prefix[n] = prefix[n - 1] + mu[n];
  }
  return prefix;
}

static int solve(int limit) {
  std::vector<int> phi_value(limit + 1, 0);
  std::vector<int> divisor_product(limit + 1, 1);

  int power = 1;
  for (int n = 1; n <= limit; ++n) {
    power += power;
    if (power >= MOD) power -= MOD;
    phi_value[n] = power - 1;
  }

  for (int d = 1; d <= limit; ++d) {
    int phi = phi_value[d];
    int factor = phi + 1;
    if (factor == MOD) factor = 0;

    for (int multiple = d; multiple <= limit; multiple += d) {
      divisor_product[multiple] =
          static_cast<int>(1LL * divisor_product[multiple] * factor % MOD);
    }

    int inverse = mod_pow(phi, MOD - 2);
    for (int multiple = d + d; multiple <= limit; multiple += d) {
      phi_value[multiple] =
          static_cast<int>(1LL * phi_value[multiple] * inverse % MOD);
    }
  }

  std::vector<int> mertens = mertens_prefix(limit);
  long long answer = 0;
  for (int d = 1; d <= limit; ++d) {
    answer += 1LL * divisor_product[d] * mertens[limit / d];
    answer %= MOD;
  }
  if (answer < 0) answer += MOD;
  return static_cast<int>(answer);
}

int main(int argc, char** argv) {
  int limit = 10'000'000;
  if (argc > 1) {
    limit = std::atoi(argv[1]);
  }
  std::cout << solve(limit) << '\n';
  return 0;
}
