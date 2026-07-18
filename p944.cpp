#include <cmath>
#include <cstdint>
#include <iostream>
#include <vector>

using u64 = std::uint64_t;
using u128 = unsigned __int128;

constexpr u64 TARGET = 100'000'000'000'000ULL;
constexpr u64 MODULUS = 1'234'567'891ULL;

u64 power_mod(u64 base, u64 exponent, u64 modulus) {
  u64 result = 1;
  while (exponent != 0) {
    if (exponent & 1) {
      result = result * base % modulus;
    }
    base = base * base % modulus;
    exponent >>= 1;
  }
  return result;
}

u64 triangular_interval(u64 left, u64 right, u64 modulus) {
  const u128 count = right - left + 1;
  return static_cast<u64>(
      (static_cast<u128>(left + right) * count / 2) % modulus
  );
}

u64 sum_of_elevisors(u64 n, u64 modulus) {
  u64 split = static_cast<u64>(std::sqrt(static_cast<long double>(n)));
  while ((split + 1) * (split + 1) <= n) {
    ++split;
  }
  while (split * split > n) {
    --split;
  }

  // powers[d] permits O(1) updates when floor(n/x) changes by d.
  std::vector<u64> powers(split + 1);
  powers[0] = 1;
  for (u64 exponent = 1; exponent <= split; ++exponent) {
    powers[exponent] = 2 * powers[exponent - 1] % modulus;
  }

  // A = sum_x x * 2^(n-floor(n/x)).
  u64 weighted = 0;
  u64 quotient = n;
  u64 power = 1;
  for (u64 x = 1; x <= split; ++x) {
    weighted = (
        weighted + (x % modulus) * power
    ) % modulus;
    if (x != split) {
      const u64 next_quotient = n / (x + 1);
      const u64 difference = quotient - next_quotient;
      const u64 factor = difference <= split
          ? powers[difference]
          : power_mod(2, difference, modulus);
      power = power * factor % modulus;
      quotient = next_quotient;
    }
  }

  // The remaining x values occur in whole intervals with quotient q.
  const u64 last_quotient = n / (split + 1);
  power = power_mod(2, n - 1, modulus);
  const u64 inverse_two = (modulus + 1) / 2;
  for (u64 q = 1; q <= last_quotient; ++q) {
    const u64 left = n / (q + 1) + 1;
    const u64 right = n / q;
    const u64 interval_sum =
        triangular_interval(left, right, modulus);
    weighted = (weighted + interval_sum * power) % modulus;
    power = power * inverse_two % modulus;
  }

  const u64 all_x =
      static_cast<u64>(
          (static_cast<u128>(n) * (n + 1) / 2) % modulus
      );
  const u64 positive_term =
      power_mod(2, n - 1, modulus) * all_x % modulus;
  return (positive_term + modulus - weighted) % modulus;
}

int main() {
  if (sum_of_elevisors(10, MODULUS) != 4'927) {
    std::cerr << "sample self-check failed\n";
    return 1;
  }
  std::cout << sum_of_elevisors(TARGET, MODULUS) << '\n';
}
