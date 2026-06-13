#include <cmath>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>

static constexpr int LIMIT = 6'000'000;

static std::vector<char> prime_sieve(int limit) {
  std::vector<char> is_prime(limit + 1, 1);
  is_prime[0] = is_prime[1] = 0;
  for (int p = 2; 1LL * p * p <= limit; ++p) {
    if (!is_prime[p]) continue;
    for (long long q = 1LL * p * p; q <= limit; q += p) {
      is_prime[static_cast<std::size_t>(q)] = 0;
    }
  }
  return is_prime;
}

static long long solve_for(int limit) {
  std::vector<char> is_prime = prime_sieve(limit);
  std::vector<int> representation_l(limit + 1, 0);

  int max_l = static_cast<int>(std::sqrt(4.0 * limit)) + 2;
  int max_b = static_cast<int>(std::sqrt(4.0 * limit / 27.0)) + 2;
  for (int b = 0; b <= max_b; ++b) {
    int b_part = 27 * b * b;
    for (int l = -max_l; l <= max_l; ++l) {
      if ((l % 3 + 3) % 3 != 1) continue;
      int value = l * l + b_part;
      if (value % 4 != 0) continue;
      int p = value / 4;
      if (p > 0 && p <= limit && is_prime[p] && p % 3 == 1) {
        representation_l[p] = l;
      }
    }
  }

  long long total = 0;
  for (int p = 2; p < limit; ++p) {
    if (!is_prime[p]) continue;
    if (p == 3) {
      total += 2;
    } else if (p % 3 == 2) {
      total += 1LL * (p - 1) * (p - 2);
    } else {
      int l = representation_l[p];
      total += 1LL * (p - 1) * (p - 8 + l);
    }
  }
  return total;
}

int main(int argc, char **argv) {
  int limit = LIMIT;
  if (argc > 1) {
    limit = std::stoi(argv[1]);
  }
  std::cout << solve_for(limit) << '\n';
  return 0;
}
