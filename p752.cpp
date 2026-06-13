#include <algorithm>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <string>
#include <unordered_map>
#include <vector>

static constexpr int LIMIT = 1'000'000;

struct Pair {
  long long a;
  long long b;

  bool operator==(const Pair &other) const {
    return a == other.a && b == other.b;
  }
};

static Pair multiply(Pair x, Pair y, long long mod) {
  return {
      (x.a * y.a + 7 * x.b % mod * y.b) % mod,
      (x.a * y.b + x.b * y.a) % mod,
  };
}

static Pair power_pair(long long exponent, long long mod) {
  Pair result{1, 0};
  Pair base{1, 1};
  while (exponent > 0) {
    if (exponent & 1) result = multiply(result, base, mod);
    base = multiply(base, base, mod);
    exponent >>= 1;
  }
  return result;
}

static long long mod_pow(long long base, long long exponent, long long mod) {
  long long result = 1 % mod;
  while (exponent > 0) {
    if (exponent & 1) result = (__int128)result * base % mod;
    base = (__int128)base * base % mod;
    exponent >>= 1;
  }
  return result;
}

class Solver {
 public:
  Solver() {
    build_sieve();
  }

  unsigned long long sum(int limit) {
    unsigned long long total = 0;
    for (int x = 2; x <= limit; ++x) {
      int y = x;
      unsigned long long value = 1;
      bool ok = true;
      while (y > 1) {
        int p = spf_[y];
        int prime_power = 1;
        int exponent = 0;
        while (y % p == 0) {
          y /= p;
          prime_power *= p;
          ++exponent;
        }
        long long order = order_cache_[prime_power];
        if (order == -1) {
          order = prime_power_order(p, exponent, prime_power);
          order_cache_[prime_power] = order;
        }
        if (order == 0) {
          ok = false;
          break;
        }
        value = std::lcm(value, static_cast<unsigned long long>(order));
      }
      if (ok) total += value;
    }
    return total;
  }

 private:
  std::vector<int> spf_;
  std::vector<int> primes_;
  std::vector<long long> order_cache_;

  void build_sieve() {
    spf_.assign(LIMIT + 1, 0);
    order_cache_.assign(LIMIT + 1, -1);
    for (int i = 2; i <= LIMIT; ++i) {
      if (spf_[i] == 0) {
        spf_[i] = i;
        primes_.push_back(i);
      }
      for (int p : primes_) {
        long long v = 1LL * i * p;
        if (v > LIMIT || p > spf_[i]) break;
        spf_[static_cast<std::size_t>(v)] = p;
      }
    }
  }

  std::vector<long long> distinct_prime_factors(long long n) const {
    std::vector<long long> factors;
    for (int p : primes_) {
      if (1LL * p * p > n) break;
      if (n % p == 0) {
        factors.push_back(p);
        while (n % p == 0) n /= p;
      }
    }
    if (n > 1) factors.push_back(n);
    return factors;
  }

  long long prime_power_order(int p, int exponent, int prime_power) const {
    if (p == 2 || p == 3) return 0;

    long long candidate;
    if (p == 7) {
      candidate = prime_power;
    } else {
      bool split = mod_pow(7, (p - 1) / 2, p) == 1;
      candidate = (split ? p - 1LL : 1LL * p * p - 1);
      for (int i = 1; i < exponent; ++i) candidate *= p;
    }

    long long order = candidate;
    for (long long factor : distinct_prime_factors(candidate)) {
      while (order % factor == 0 && power_pair(order / factor, prime_power) == Pair{1, 0}) {
        order /= factor;
      }
    }
    return order;
  }
};

int main(int argc, char **argv) {
  int limit = LIMIT;
  if (argc > 1) {
    limit = std::stoi(argv[1]);
  }
  Solver solver;
  std::cout << solver.sum(limit) << '\n';
  return 0;
}
