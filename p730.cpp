#include <algorithm>
#include <atomic>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <thread>
#include <vector>

using i64 = long long;

static std::vector<int> smallest_prime_factor;
static std::vector<int> primes;
static i64 sieve_limit = 0;

static i64 gcd_i64(i64 a, i64 b) {
  while (b != 0) {
    i64 t = a % b;
    a = b;
    b = t;
  }
  return a < 0 ? -a : a;
}

static i64 ipow(i64 base, int exp) {
  i64 result = 1;
  while (exp-- > 0) result *= base;
  return result;
}

static i64 egcd(i64 a, i64 b, i64 &x, i64 &y) {
  if (b == 0) {
    x = 1;
    y = 0;
    return a;
  }
  i64 x1, y1;
  i64 g = egcd(b, a % b, x1, y1);
  x = y1;
  y = x1 - (a / b) * y1;
  return g;
}

static i64 mod_inverse(i64 a, i64 mod) {
  a %= mod;
  if (a < 0) a += mod;
  i64 x, y;
  egcd(a, mod, x, y);
  x %= mod;
  if (x < 0) x += mod;
  return x;
}

static i64 mod_pow(i64 base, i64 exp, i64 mod) {
  i64 result = 1;
  base %= mod;
  if (base < 0) base += mod;
  while (exp > 0) {
    if (exp & 1) result = result * base % mod;
    base = base * base % mod;
    exp >>= 1;
  }
  return result;
}

static i64 isqrt_i64(i64 n) {
  i64 r = static_cast<i64>(std::sqrt(static_cast<long double>(n)));
  while (r > 0 && r * r > n) --r;
  while ((r + 1) * (r + 1) <= n) ++r;
  return r;
}

static i64 tonelli(i64 n, i64 p) {
  if (n % p == 0) return 0;
  i64 q = p - 1;
  int s = 0;
  while ((q & 1) == 0) {
    q >>= 1;
    ++s;
  }
  if (s == 1) return mod_pow(n, (p + 1) / 4, p);

  i64 z = 2;
  while (mod_pow(z, (p - 1) / 2, p) != p - 1) ++z;

  i64 c = mod_pow(z, q, p);
  i64 r = mod_pow(n, (q + 1) / 2, p);
  i64 t = mod_pow(n, q, p);
  int m = s;
  while (t != 1) {
    int i = 0;
    i64 tt = t;
    while (tt != 1) {
      tt = tt * tt % p;
      ++i;
      if (i == m) return -1;
    }
    i64 b = mod_pow(c, 1LL << (m - i - 1), p);
    r = r * b % p;
    c = b * b % p;
    t = t * c % p;
    m = i;
  }
  return r;
}

static i64 sqrt_mod_prime(i64 a, i64 p) {
  a %= p;
  if (a < 0) a += p;
  if (a == 0) return 0;

  i64 root;
  if (p % 4 == 3) {
    root = mod_pow(a, (p + 1) / 4, p);
  } else if (p % 8 == 5) {
    i64 test = mod_pow(a, (p - 1) / 4, p);
    if (test == 1) {
      root = mod_pow(a, (p + 3) / 8, p);
    } else {
      root = mod_pow(a, (p + 3) / 8, p) * mod_pow(2, (p - 1) / 4, p) % p;
    }
  } else {
    if (mod_pow(a, (p - 1) / 2, p) != 1) return -1;
    root = tonelli(a, p);
    if (root < 0) return -1;
  }
  return root * root % p == a ? root : -1;
}

static i64 hensel_odd(i64 root, i64 a, i64 p, int exp) {
  i64 mod = p;
  i64 y = root % p;
  for (int k = 1; k < exp; ++k) {
    i64 next_mod = mod * p;
    i64 f = (y * y - a) % next_mod;
    if (f < 0) f += next_mod;
    y = (y - f * mod_inverse(2 * y, next_mod)) % next_mod;
    if (y < 0) y += next_mod;
    mod = next_mod;
  }
  return y;
}

static void solve_prime_power(i64 a, i64 p, int exp, std::vector<i64> &roots) {
  roots.clear();
  i64 pe = ipow(p, exp);
  a %= pe;
  if (a < 0) a += pe;

  if (a == 0) {
    i64 step = ipow(p, (exp + 1) / 2);
    for (i64 x = 0; x < pe; x += step) roots.push_back(x);
    return;
  }

  int valuation = 0;
  i64 unit = a;
  while (unit % p == 0) {
    unit /= p;
    ++valuation;
  }
  if (valuation & 1) return;

  int reduced_exp = exp - valuation;
  i64 reduced_mod = ipow(p, reduced_exp);
  unit %= reduced_mod;
  if (unit < 0) unit += reduced_mod;

  std::vector<i64> reduced_roots;
  if (p == 2) {
    if (reduced_exp == 1) {
      reduced_roots.push_back(1 % reduced_mod);
    } else if (reduced_exp == 2) {
      if (unit % 4 == 1) {
        reduced_roots.push_back(1);
        reduced_roots.push_back(3);
      }
    } else if (unit % 8 == 1) {
      i64 y = 1;
      for (int k = 3; k < reduced_exp; ++k) {
        i64 mod = ipow(2, k + 1);
        i64 f = (y * y - unit) % mod;
        if (f < 0) f += mod;
        if (f != 0) y += ipow(2, k - 1);
      }
      y %= reduced_mod;
      i64 half = reduced_mod / 2;
      i64 candidates[4] = {
          y,
          (reduced_mod - y) % reduced_mod,
          (half + y) % reduced_mod,
          (half - y + reduced_mod) % reduced_mod,
      };
      for (i64 candidate : candidates) {
        if ((candidate * candidate - unit) % reduced_mod != 0) continue;
        bool seen = false;
        for (i64 old : reduced_roots) {
          if (old == candidate) {
            seen = true;
            break;
          }
        }
        if (!seen) reduced_roots.push_back(candidate);
      }
    }
  } else {
    i64 root = sqrt_mod_prime(unit % p, p);
    if (root < 0) return;
    i64 lifted = reduced_exp == 1 ? root : hensel_odd(root, unit, p, reduced_exp);
    lifted %= reduced_mod;
    reduced_roots.push_back(lifted);
    i64 other = (reduced_mod - lifted) % reduced_mod;
    if (other != lifted) reduced_roots.push_back(other);
  }

  if (reduced_roots.empty()) return;
  i64 scale = ipow(p, valuation / 2);
  for (i64 y : reduced_roots) {
    for (i64 k = 0; k < scale; ++k) {
      roots.push_back(scale * (y + k * reduced_mod) % pe);
    }
  }
}

static void build_sieve(i64 limit) {
  sieve_limit = limit;
  smallest_prime_factor.assign(static_cast<std::size_t>(limit + 1), 0);
  primes.clear();
  for (i64 i = 2; i <= limit; ++i) {
    if (smallest_prime_factor[static_cast<std::size_t>(i)] == 0) {
      smallest_prime_factor[static_cast<std::size_t>(i)] = static_cast<int>(i);
      primes.push_back(static_cast<int>(i));
    }
    for (int p : primes) {
      i64 v = i * p;
      if (v > limit || p > smallest_prime_factor[static_cast<std::size_t>(i)]) break;
      smallest_prime_factor[static_cast<std::size_t>(v)] = p;
    }
  }
}

static bool roots_negative_shift(
    i64 shift,
    i64 modulus,
    const int *sqrt_cache,
    std::vector<i64> &roots,
    std::vector<i64> &prime_power_roots,
    std::vector<i64> &merged) {
  roots.assign(1, 0);
  i64 current_mod = 1;
  i64 remaining = modulus;

  while (remaining > 1) {
    i64 p = smallest_prime_factor[static_cast<std::size_t>(remaining)];
    int exp = 0;
    i64 pe = 1;
    while (remaining % p == 0) {
      remaining /= p;
      ++exp;
      pe *= p;
    }

    i64 residue = (-shift) % pe;
    if (residue < 0) residue += pe;
    if (p == 2 || shift % p == 0) {
      solve_prime_power(residue, p, exp, prime_power_roots);
    } else {
      int base = sqrt_cache[p];
      if (base < 0) return false;
      prime_power_roots.clear();
      if (exp == 1) {
        prime_power_roots.push_back(base);
        prime_power_roots.push_back(p - base);
      } else {
        i64 lifted = hensel_odd(base, residue, p, exp);
        prime_power_roots.push_back(lifted % pe);
        prime_power_roots.push_back((pe - lifted % pe) % pe);
      }
    }

    if (prime_power_roots.empty()) return false;
    i64 inverse = mod_inverse(current_mod % pe, pe);
    i64 next_mod = current_mod * pe;
    merged.clear();
    merged.reserve(roots.size() * prime_power_roots.size());
    for (i64 old_root : roots) {
      for (i64 new_root : prime_power_roots) {
        i64 diff = (new_root - old_root) % pe;
        if (diff < 0) diff += pe;
        i64 t = diff * inverse % pe;
        merged.push_back((old_root + current_mod * t) % next_mod);
      }
    }
    roots.swap(merged);
    current_mod = next_mod;
  }

  return true;
}

static i64 pmax_for(i64 u, i64 shift, i64 perimeter_limit) {
  long double disc = static_cast<long double>(u) * u -
                     4.0L * (static_cast<long double>(shift) -
                             static_cast<long double>(u) * perimeter_limit);
  if (disc < 0) return 0;
  i64 p = static_cast<i64>((-static_cast<long double>(u) + std::sqrt(disc)) / 2.0L) + 2;
  auto eval = [&](i64 x) { return x * x + u * x + shift - u * perimeter_limit; };
  while (p >= 1 && eval(p) > 0) --p;
  return p;
}

static i64 count_residue(i64 low, i64 high, i64 residue, i64 modulus) {
  if (high < low) return 0;
  i64 first = low + (residue - low) % modulus;
  if (first < low) first += modulus;
  if (first > high) return 0;
  return (high - first) / modulus + 1;
}

static i64 count_all_for_shift(i64 shift, i64 perimeter_limit, int *sqrt_cache) {
  if (perimeter_limit < 3) return 0;

  i64 u_limit = static_cast<i64>(0.123L * perimeter_limit) + 50;
  if (u_limit > sieve_limit) u_limit = sieve_limit;

  for (int p : primes) {
    if (p > u_limit) break;
    if (p == 2 || shift % p == 0) continue;
    sqrt_cache[p] = static_cast<int>(sqrt_mod_prime((-shift % p + p) % p, p));
  }

  std::vector<i64> roots;
  std::vector<i64> prime_power_roots;
  std::vector<i64> merged;
  roots.reserve(64);
  prime_power_roots.reserve(64);
  merged.reserve(64);

  i64 count = 0;
  for (i64 u = 1; u <= u_limit; ++u) {
    i64 pmax = pmax_for(u, shift, perimeter_limit);
    if (pmax < 1) continue;

    auto q_minus_p_twice = [&](i64 p) { return p * p - 2 * u * p + shift - u * u; };
    i64 bad_low = 1;
    i64 bad_high = 0;
    long double disc = 2.0L * u * u - static_cast<long double>(shift);
    if (disc > 0) {
      i64 p = static_cast<i64>(u - std::sqrt(disc));
      while (q_minus_p_twice(p) < 0) --p;
      while (q_minus_p_twice(p + 1) >= 0) ++p;
      bad_low = p + 1;

      i64 q = static_cast<i64>(u + std::sqrt(disc));
      while (q_minus_p_twice(q) < 0) ++q;
      while (q > 1 && q_minus_p_twice(q - 1) >= 0) --q;
      bad_high = q - 1;
    }

    if (!roots_negative_shift(shift, u, sqrt_cache, roots, prime_power_roots, merged)) {
      continue;
    }

    i64 two_u = 2 * u;
    i64 clipped_bad_low = std::max<i64>(bad_low, 1);
    i64 clipped_bad_high = std::min<i64>(bad_high, pmax);
    for (i64 root : roots) {
      for (int lift = 0; lift < 2; ++lift) {
        i64 residue = root + lift * u;
        i64 c = (residue * residue + shift) / u;
        if ((c & 1) != (u & 1)) continue;
        i64 total = count_residue(1, pmax, residue, two_u);
        if (bad_high >= bad_low) {
          total -= count_residue(clipped_bad_low, clipped_bad_high, residue, two_u);
        }
        count += total;
      }
    }
  }
  return count;
}

static i64 primitive_pythagorean_count(i64 perimeter_limit) {
  i64 count = 0;
  for (i64 s = 2; 2 * s * (s + 1) <= perimeter_limit; ++s) {
    i64 tmax = perimeter_limit / (2 * s) - s;
    if (tmax > s - 1) tmax = s - 1;
    for (i64 t = 1; t <= tmax; ++t) {
      if (((s - t) & 1) == 0) continue;
      if (gcd_i64(s, t) != 1) continue;
      ++count;
    }
  }
  return count;
}

static int mobius_small(int n) {
  static constexpr int mu[11] = {0, 1, -1, -1, 0, -1, 1, -1, 0, 0, 1};
  return 1 <= n && n <= 10 ? mu[n] : 0;
}

static i64 solve_for(i64 n, i64 m, int thread_count) {
  i64 sieve_bound = static_cast<i64>(0.123L * n) + 60;
  build_sieve(sieve_bound);

  struct Term {
    int coefficient;
    i64 shift;
    i64 perimeter_limit;
  };

  std::vector<Term> terms;
  for (i64 shift = 1; shift <= m; ++shift) {
    for (i64 divisor = 1; divisor * divisor <= shift; ++divisor) {
      if (shift % (divisor * divisor) != 0) continue;
      int mu = mobius_small(static_cast<int>(divisor));
      if (mu == 0) continue;
      terms.push_back({mu, shift / (divisor * divisor), n / divisor});
    }
  }

  std::atomic<std::size_t> next_index{0};
  std::atomic<i64> total{0};
  std::vector<std::thread> threads;
  for (int t = 0; t < thread_count; ++t) {
    threads.emplace_back([&]() {
      std::vector<int> sqrt_cache(static_cast<std::size_t>(sieve_limit + 1));
      i64 local = 0;
      while (true) {
        std::size_t index = next_index.fetch_add(1);
        if (index >= terms.size()) break;
        Term term = terms[index];
        local += term.coefficient *
                 count_all_for_shift(term.shift, term.perimeter_limit, sqrt_cache.data());
      }
      total.fetch_add(local);
    });
  }
  for (std::thread &thread : threads) thread.join();

  return primitive_pythagorean_count(n) + total.load();
}

int main(int argc, char **argv) {
  i64 n = argc > 1 ? std::atoll(argv[1]) : 100000000LL;
  i64 m = argc > 2 ? std::atoll(argv[2]) : 100;
  int thread_count = argc > 3 ? std::atoi(argv[3]) : 8;
  if (thread_count < 1) thread_count = 1;

  std::cout << solve_for(n, m, thread_count) << '\n';
  return 0;
}
