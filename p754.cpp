#include <algorithm>
#include <cstdint>
#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>

static constexpr int MOD = 1'000'000'007;
static constexpr int TARGET = 100'000'000;

static long long mod_pow(long long base, long long exponent) {
  long long result = 1;
  while (exponent > 0) {
    if (exponent & 1) result = result * base % MOD;
    base = base * base % MOD;
    exponent >>= 1;
  }
  return result;
}

static int inverse(int value) {
  return static_cast<int>(mod_pow(value, MOD - 2));
}

class Solver {
 public:
  explicit Solver(int n) : n_(n) {}

  int solve() {
    build_mobius();
    build_prefixes();
    auto h_values = needed_h_values();

    long long answer = 1;
    for (int left = 1; left <= n_;) {
      int q = n_ / left;
      int right = n_ / q;

      int mu_sum = mertens_[right] - mertens_[left - 1];
      long long plus_range = pref_plus_[right] * 1LL * inverse(pref_plus_[left - 1]) % MOD;
      long long minus_range = pref_minus_[right] * 1LL * inverse(pref_minus_[left - 1]) % MOD;
      long long d_product = plus_range * inverse(static_cast<int>(minus_range)) % MOD;

      long long triangle = 1LL * q * (q + 1) / 2;
      answer = answer * mod_pow(d_product, triangle) % MOD;

      int h = h_values[q];
      if (mu_sum > 0) {
        answer = answer * mod_pow(h, mu_sum) % MOD;
      } else if (mu_sum < 0) {
        answer = answer * mod_pow(inverse(h), -1LL * mu_sum) % MOD;
      }

      left = right + 1;
    }

    return static_cast<int>(answer);
  }

 private:
  int n_;
  std::vector<signed char> mu_;
  std::vector<int> mertens_;
  std::vector<int> pref_plus_;
  std::vector<int> pref_minus_;

  void build_mobius() {
    std::vector<int> least_prime(n_ + 1, 0);
    std::vector<int> primes;
    primes.reserve(n_ / 10);
    mu_.assign(n_ + 1, 0);
    mu_[1] = 1;

    for (int i = 2; i <= n_; ++i) {
      if (least_prime[i] == 0) {
        least_prime[i] = i;
        primes.push_back(i);
        mu_[i] = -1;
      }
      for (int p : primes) {
        long long v = 1LL * i * p;
        if (v > n_ || p > least_prime[i]) break;
        least_prime[static_cast<std::size_t>(v)] = p;
        if (i % p == 0) {
          mu_[static_cast<std::size_t>(v)] = 0;
          break;
        }
        mu_[static_cast<std::size_t>(v)] = -mu_[i];
      }
    }
  }

  void build_prefixes() {
    mertens_.assign(n_ + 1, 0);
    pref_plus_.assign(n_ + 1, 1);
    pref_minus_.assign(n_ + 1, 1);

    for (int i = 1; i <= n_; ++i) {
      mertens_[i] = mertens_[i - 1] + mu_[i];
      pref_plus_[i] = pref_plus_[i - 1];
      pref_minus_[i] = pref_minus_[i - 1];
      if (mu_[i] == 1) {
        pref_plus_[i] = static_cast<int>(1LL * pref_plus_[i] * i % MOD);
      } else if (mu_[i] == -1) {
        pref_minus_[i] = static_cast<int>(1LL * pref_minus_[i] * i % MOD);
      }
    }
    mu_.clear();
    mu_.shrink_to_fit();
  }

  std::unordered_map<int, int> needed_h_values() const {
    std::vector<int> needed;
    for (int left = 1; left <= n_;) {
      int q = n_ / left;
      int right = n_ / q;
      needed.push_back(q);
      left = right + 1;
    }
    std::sort(needed.begin(), needed.end());
    needed.erase(std::unique(needed.begin(), needed.end()), needed.end());

    std::unordered_map<int, int> values;
    values.reserve(needed.size() * 2);
    long long factorial = 1;
    long long superfactorial = 1;
    std::size_t index = 0;
    for (int i = 1; i <= n_; ++i) {
      factorial = factorial * i % MOD;
      superfactorial = superfactorial * factorial % MOD;
      if (index < needed.size() && needed[index] == i) {
        values[i] = static_cast<int>(superfactorial);
        ++index;
      }
    }
    return values;
  }
};

int main(int argc, char **argv) {
  int n = TARGET;
  if (argc > 1) {
    n = std::stoi(argv[1]);
  }
  Solver solver(n);
  std::cout << solver.solve() << '\n';
  return 0;
}
