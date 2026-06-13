#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>

static constexpr long long MOD = 1'000'000'000LL;

static __int128 fourth(long long value) {
  __int128 square = static_cast<__int128>(value) * value;
  return square * square;
}

static long long fourth_root_floor(__int128 value) {
  long long lo = 0;
  long long hi = 1;
  while (fourth(hi) <= value) hi *= 2;
  while (lo + 1 < hi) {
    long long mid = lo + (hi - lo) / 2;
    if (fourth(mid) <= value) {
      lo = mid;
    } else {
      hi = mid;
    }
  }
  return lo;
}

static void add_mod(long long& total, __int128 value) {
  total = (total + static_cast<long long>(value % MOD)) % MOD;
}

static long long solve(long long limit) {
  const __int128 n = limit;
  long long total = 0;

  // Odd y: z-4x = a^4, z+4x = b^4 with odd coprime a < b.
  long long max_odd = fourth_root_floor(2 * n) + 2;
  for (long long b = 3; b <= max_odd; b += 2) {
    __int128 b4 = fourth(b);
    for (long long a = 1; a < b; a += 2) {
      if (std::gcd(a, b) != 1) continue;
      __int128 a4 = fourth(a);
      __int128 z = (a4 + b4) / 2;
      if (z > n) break;
      __int128 x = (b4 - a4) / 8;
      __int128 y = static_cast<__int128>(a) * b;
      if (x <= n && y <= n) {
        add_mod(total, x + y + z);
      }
    }
  }

  // Even y: the primitive 2-adic split has valuations (3, 4e-3).
  for (int e = 2; e < 64; ++e) {
    __int128 c = static_cast<__int128>(1) << (4 * e - 6);
    __int128 zcoef = static_cast<__int128>(1) << (4 * e - 4);
    if (zcoef > 4 * n) break;

    long long max_high = fourth_root_floor(n / zcoef) + 2;
    bool any = false;
    for (long long high = 1; high <= max_high; high += 2) {
      __int128 high4 = fourth(high);
      if (zcoef * high4 > n) break;
      long long max_low = fourth_root_floor((n - zcoef * high4) / 4);
      for (long long low = 1; low <= max_low; low += 2) {
        if (std::gcd(low, high) != 1) continue;
        __int128 low4 = fourth(low);
        __int128 x = c * high4 - low4;
        if (x < 0) x = -x;
        __int128 y = (static_cast<__int128>(1) << e) * low * high;
        __int128 z = 4 * low4 + zcoef * high4;
        if (x > 0 && x <= n && y <= n && z <= n) {
          add_mod(total, x + y + z);
          any = true;
        }
      }
    }
    if (!any && zcoef > n) break;
  }

  return total;
}

int main(int argc, char** argv) {
  long long limit = 10'000'000'000'000'000LL;
  if (argc > 1) limit = std::atoll(argv[1]);
  std::cout << solve(limit) << '\n';
  return 0;
}
