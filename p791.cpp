#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iostream>

static constexpr long long MOD = 433'494'437LL;

static long long isqrt_floor(long long value) {
  if (value <= 0) return 0;
  long long root = static_cast<long long>(std::sqrt(static_cast<long double>(value)));
  while ((__int128)(root + 1) * (root + 1) <= value) ++root;
  while ((__int128)root * root > value) --root;
  return root;
}

static long long first_even_at_least(long long value) {
  return (value & 1LL) ? value + 1 : value;
}

static long long last_even_at_most(long long value) {
  return (value & 1LL) ? value - 1 : value;
}

static long long square_sum_even_range(long long first, long long last) {
  if (first > last) return 0;
  long long count = (last - first) / 2 + 1;
  long long first_half = first / 2;
  long long last_half = last / 2;
  auto sum_squares = [](long long n) -> __int128 {
    return (__int128)n * (n + 1) * (2 * n + 1) / 6;
  };

  __int128 total;
  if (first_half >= 0) {
    total = sum_squares(last_half) - sum_squares(first_half - 1);
  } else if (last_half <= 0) {
    long long a = -last_half;
    long long b = -first_half;
    total = sum_squares(b) - sum_squares(a - 1);
  } else {
    total = sum_squares(-first_half) + sum_squares(last_half);
  }
  return static_cast<long long>((4 * (total % MOD)) % MOD);
}

static long long contribution(long long r, long long u, long long first_v,
                              long long last_v) {
  if (first_v > last_v) return 0;
  long long count = (last_v - first_v) / 2 + 1;
  long long base = ((r % MOD) * (r % MOD) + (u % MOD) * (u % MOD)) % MOD;
  long long sum_v2 = square_sum_even_range(first_v, last_v);
  long long total = (count % MOD) * base % MOD;
  total = (total + sum_v2) % MOD;
  // r, u and v are even, so the numerator is always divisible by 2.
  return total / 2 + (total & 1LL ? (MOD + 1) / 2 : 0);
}

static long long solve(long long n) {
  const long long limit = 8 * n;
  const long long max_r = isqrt_floor(limit) + 2;
  long long answer = 0;

  for (long long r = 0; r <= max_r; r += 2) {
    const long long rr = r * r;
    for (long long u = 0; u <= r; u += 2) {
      const long long base = rr + u * u + 2 * (r + u);
      const long long rem = limit - base + 1;
      if (rem < 0) continue;

      const long long radius = isqrt_floor(rem);
      long long lo = first_even_at_least(std::max(-u, 1 - radius));
      long long hi = last_even_at_most(std::min(u, 1 + radius));
      if (lo > hi) continue;

      long long add = contribution(r, u, lo, hi);

      // The a >= 1 constraint only removes values near the origin.
      if (r <= 2 && u <= 2) {
        for (long long v = lo; v <= hi; v += 2) {
          long long p = rr + u * u + v * v;
          if (p - 2 * (r + u + v) < 8) {
            add -= (p / 2) % MOD;
          }
        }
      }

      answer += add;
      answer %= MOD;
      if (answer < 0) answer += MOD;
    }
  }

  return answer;
}

int main(int argc, char** argv) {
  long long n = 100'000'000LL;
  if (argc > 1) n = std::atoll(argv[1]);
  std::cout << solve(n) << '\n';
  return 0;
}
