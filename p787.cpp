#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <unordered_map>
#include <vector>

class Mertens {
 public:
  explicit Mertens(int limit) : limit_(limit), prefix_(limit + 1, 0) {
    std::vector<int> least_prime(limit + 1, 0);
    std::vector<int> primes;
    std::vector<signed char> mu(limit + 1, 0);
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

    prefix_[1] = 1;
    for (int n = 2; n <= limit; ++n) {
      prefix_[n] = prefix_[n - 1] + mu[n];
    }
  }

  long long total(long long n) {
    if (n <= 0) return 0;
    if (n <= limit_) return prefix_[static_cast<int>(n)];
    auto it = cache_.find(n);
    if (it != cache_.end()) return it->second;

    long long answer = 1;
    for (long long left = 2; left <= n;) {
      long long quotient = n / left;
      long long right = n / quotient;
      answer -= (right - left + 1) * total(quotient);
      left = right + 1;
    }
    cache_[n] = answer;
    return answer;
  }

  long long odd_total(long long n) {
    long long answer = 0;
    while (n > 0) {
      answer += total(n);
      n /= 2;
    }
    return answer;
  }

 private:
  int limit_;
  std::vector<int> prefix_;
  std::unordered_map<long long, long long> cache_;
};

static long long ordered_coprime_pairs(long long m) {
  return m * (m - 1) / 2;
}

static long long losing_half_region(long long m) {
  long long limit = (m - 1) / 4;
  return limit * ((m + 1) / 2 - limit - 1);
}

static long long solve(long long n) {
  Mertens mertens(5'000'000);
  __int128 total = 0;
  __int128 losing_half = 0;

  for (long long left = 1; left <= n;) {
    long long quotient = n / left;
    long long right = n / quotient;

    long long mu_sum = mertens.total(right) - mertens.total(left - 1);
    total += static_cast<__int128>(mu_sum) * ordered_coprime_pairs(quotient);

    long long odd_mu_sum =
        mertens.odd_total(right) - mertens.odd_total(left - 1);
    losing_half +=
        static_cast<__int128>(odd_mu_sum) * losing_half_region(quotient);

    left = right + 1;
  }

  return static_cast<long long>(total - 2 * losing_half);
}

int main(int argc, char** argv) {
  long long n = 1'000'000'000LL;
  if (argc > 1) n = std::atoll(argv[1]);
  std::cout << solve(n) << '\n';
  return 0;
}
