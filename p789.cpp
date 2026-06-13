#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <string>
#include <unordered_map>
#include <vector>

struct Entry {
  std::uint32_t residue;
  int weight;
  unsigned __int128 product;
};

struct Best {
  int weight;
  unsigned __int128 product;
};

static constexpr int HALF_WEIGHT = 120;
static constexpr int MAX_WEIGHT = 240;

static std::vector<int> primes_up_to(int limit) {
  std::vector<int> primes;
  for (int n = 2; n <= limit; ++n) {
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

static long long mod_pow(long long base, long long exponent, long long mod) {
  long long result = 1 % mod;
  while (exponent > 0) {
    if (exponent & 1) result = static_cast<__int128>(result) * base % mod;
    base = static_cast<__int128>(base) * base % mod;
    exponent >>= 1;
  }
  return result;
}

static void generate_entries(
    const std::vector<int>& primes, int index, int remaining, int weight,
    long long residue, unsigned __int128 product, long long modulus,
    std::vector<Entry>& entries) {
  entries.push_back({static_cast<std::uint32_t>(residue), weight, product});
  for (int i = index; i < static_cast<int>(primes.size()); ++i) {
    int prime = primes[i];
    int cost = prime - 1;
    if (cost > remaining) break;
    generate_entries(primes, i, remaining - cost, weight + cost,
                     static_cast<__int128>(residue) * prime % modulus,
                     product * static_cast<unsigned>(prime), modulus, entries);
  }
}

static std::string to_string_u128(unsigned __int128 value) {
  if (value == 0) return "0";
  std::string out;
  while (value > 0) {
    out.push_back(static_cast<char>('0' + value % 10));
    value /= 10;
  }
  std::reverse(out.begin(), out.end());
  return out;
}

static std::string brute_small(int prime) {
  int count = prime - 1;
  int full_mask = (1 << count) - 1;
  std::vector<std::pair<int, unsigned __int128>> dp(1 << count, {1'000'000, 0});
  dp[0] = {0, 1};
  for (int mask = 1; mask <= full_mask; ++mask) {
    int first = __builtin_ctz(mask);
    int a = first + 1;
    int rest = mask & ~(1 << first);
    for (int m = rest; m; m &= m - 1) {
      int second = __builtin_ctz(m);
      int b = second + 1;
      int cost = a * b % prime;
      auto sub = dp[rest & ~(1 << second)];
      int sum = sub.first + cost;
      unsigned __int128 product = sub.second * static_cast<unsigned>(cost);
      if (sum < dp[mask].first ||
          (sum == dp[mask].first && product < dp[mask].second)) {
        dp[mask] = {sum, product};
      }
    }
  }
  return to_string_u128(dp[full_mask].second);
}

static std::string solve(long long modulus) {
  if (modulus < 31) return brute_small(static_cast<int>(modulus));

  auto primes = primes_up_to(MAX_WEIGHT + 1);
  std::vector<Entry> entries;
  entries.reserve(12'000'000);
  generate_entries(primes, 0, HALF_WEIGHT, 0, 1, 1, modulus, entries);

  std::unordered_map<std::uint32_t, Best> best_by_residue;
  best_by_residue.reserve(entries.size() * 2 + 1);
  for (const Entry& entry : entries) {
    auto [it, inserted] =
        best_by_residue.emplace(entry.residue, Best{entry.weight, entry.product});
    if (!inserted &&
        (entry.weight < it->second.weight ||
         (entry.weight == it->second.weight && entry.product < it->second.product))) {
      it->second = {entry.weight, entry.product};
    }
  }

  const long long target = modulus - 1;
  const unsigned __int128 max_value = std::numeric_limits<unsigned __int128>::max();

  bool found = false;
  int best_weight = MAX_WEIGHT + 1;
  unsigned __int128 best_product = 0;
  for (const Entry& left : entries) {
    long long inverse = mod_pow(left.residue, modulus - 2, modulus);
    std::uint32_t need =
        static_cast<std::uint32_t>(static_cast<__int128>(target) * inverse % modulus);
    auto it = best_by_residue.find(need);
    if (it == best_by_residue.end()) continue;
    int weight = left.weight + it->second.weight;
    if (weight > MAX_WEIGHT) continue;
    if (left.product != 0 && it->second.product > max_value / left.product) continue;
    unsigned __int128 candidate = left.product * it->second.product;
    if (!found || weight < best_weight ||
        (weight == best_weight && candidate < best_product)) {
      found = true;
      best_weight = weight;
      best_product = candidate;
    }
  }

  return found ? to_string_u128(best_product) : "0";
}

int main(int argc, char** argv) {
  long long prime = 2'000'000'011LL;
  if (argc > 1) prime = std::atoll(argv[1]);
  std::cout << solve(prime) << '\n';
  return 0;
}
