#include <algorithm>
#include <cassert>
#include <cmath>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <limits>
#include <numeric>
#include <stdexcept>
#include <unordered_map>
#include <utility>
#include <vector>

using u64 = std::uint64_t;

constexpr int PRIME_LIMIT = 5'000'000;
constexpr int TARGET = 20'000;
constexpr long double INFINITY_COST =
    std::numeric_limits<long double>::infinity();

std::vector<int> prime_sieve(int limit) {
  std::vector<bool> is_prime(limit + 1, true);
  is_prime[0] = is_prime[1] = false;
  for (int value = 2;
       static_cast<u64>(value) * value
           <= static_cast<u64>(limit);
       ++value) {
    if (!is_prime[value]) {
      continue;
    }
    for (int multiple = value * value; multiple <= limit;
         multiple += value) {
      is_prime[multiple] = false;
    }
  }

  std::vector<int> primes;
  for (int value = 2; value <= limit; ++value) {
    if (is_prime[value]) {
      primes.push_back(value);
    }
  }
  return primes;
}

std::vector<std::pair<int, int>> factorize(int value) {
  std::vector<std::pair<int, int>> factors;
  for (int prime = 2; prime * prime <= value; ++prime) {
    if (value % prime != 0) {
      continue;
    }
    int exponent = 0;
    do {
      value /= prime;
      ++exponent;
    } while (value % prime == 0);
    factors.emplace_back(prime, exponent);
  }
  if (value > 1) {
    factors.emplace_back(value, 1);
  }
  return factors;
}

std::vector<int> make_divisors(
    const std::vector<std::pair<int, int>>& factors) {
  std::vector<int> divisors{1};
  for (const auto& [prime, exponent] : factors) {
    const std::size_t old_size = divisors.size();
    int power = 1;
    for (int count = 1; count <= exponent; ++count) {
      power *= prime;
      for (std::size_t index = 0; index < old_size; ++index) {
        divisors.push_back(divisors[index] * power);
      }
    }
  }
  std::sort(divisors.begin(), divisors.end());
  return divisors;
}

int power_mod(int base, int exponent, int modulus) {
  u64 result = 1;
  u64 current = base % modulus;
  while (exponent > 0) {
    if (exponent & 1) {
      result = result * current % modulus;
    }
    current = current * current % modulus;
    exponent >>= 1;
  }
  return static_cast<int>(result);
}

int multiplicative_order(
    int value,
    int modulus,
    int group_order,
    const std::vector<std::pair<int, int>>& group_factors) {
  int order = group_order;
  for (const auto& [prime, ignored_exponent] : group_factors) {
    (void)ignored_exponent;
    while (order % prime == 0
           && power_mod(value, order / prime, modulus) == 1) {
      order /= prime;
    }
  }
  return order;
}

struct MinimumValue {
  long double logarithm;
  std::vector<std::pair<int, int>> factors;
};

struct DpResult {
  long double actual_cost;
  long double hypothetical_cost;
  std::vector<int> parent;
};

DpResult bounded_dp(const std::vector<int>& divisors,
                    const std::vector<int>& edge_base,
                    int unseen_prime) {
  const int count = static_cast<int>(divisors.size());
  std::vector<long double> actual(count, INFINITY_COST);
  std::vector<long double> hypothetical(count, INFINITY_COST);
  std::vector<int> parent(count, -1);
  actual[0] = 0;
  const long double unseen_log = std::log(
      static_cast<long double>(unseen_prime));

  for (int from = 0; from < count; ++from) {
    if (!std::isfinite(actual[from])
        && !std::isfinite(hypothetical[from])) {
      continue;
    }
    for (int to = from + 1; to < count; ++to) {
      if (divisors[to] % divisors[from] != 0) {
        continue;
      }
      const int ratio = divisors[to] / divisors[from];
      const int base = edge_base[from * count + to];

      if (base != 0) {
        const long double edge_cost =
            (ratio - 1) * std::log(
                              static_cast<long double>(base));
        const long double actual_candidate =
            actual[from] + edge_cost;
        if (actual_candidate < actual[to]) {
          actual[to] = actual_candidate;
          parent[to] = from;
        }
        hypothetical[to] =
            std::min(hypothetical[to],
                     hypothetical[from] + edge_cost);
      } else {
        const long double edge_cost =
            (ratio - 1) * unseen_log;
        hypothetical[to] = std::min(
            hypothetical[to],
            std::min(actual[from], hypothetical[from])
                + edge_cost);
      }
    }
  }

  return {actual.back(), hypothetical.back(), std::move(parent)};
}

MinimumValue minimum_s(
    int modulus,
    const std::vector<int>& available_primes) {
  if (modulus == 2) {
    return {0, {}};
  }

  const int group_order = modulus - 1;
  const auto group_factors = factorize(group_order);
  const auto divisors = make_divisors(group_factors);
  const int divisor_count = static_cast<int>(divisors.size());
  std::unordered_map<int, int> divisor_index;
  for (int index = 0; index < divisor_count; ++index) {
    divisor_index.emplace(divisors[index], index);
  }

  std::vector<int> edge_base(divisor_count * divisor_count);
  DpResult certified_result;

  for (std::size_t prime_index = 0;
       prime_index + 1 < available_primes.size(); ++prime_index) {
    const int base = available_primes[prime_index];
    if (base != modulus) {
      const int order = multiplicative_order(
          base, modulus, group_order, group_factors);
      for (int from = 0; from < divisor_count; ++from) {
        const int reached =
            std::lcm(divisors[from], order);
        if (reached == divisors[from]) {
          continue;
        }
        const int to = divisor_index.at(reached);
        int& edge = edge_base[from * divisor_count + to];
        if (edge == 0) {
          edge = base;
        }
      }
    }

    if (prime_index % 64 != 63) {
      continue;
    }
    const int unseen_prime = available_primes[prime_index + 1];
    certified_result =
        bounded_dp(divisors, edge_base, unseen_prime);
    if (certified_result.actual_cost
        + 1e-15L
            < certified_result.hypothetical_cost) {
      std::vector<std::pair<int, int>> factors;
      int to = divisor_count - 1;
      while (to > 0) {
        const int from = certified_result.parent[to];
        assert(from >= 0);
        const int base = edge_base[from * divisor_count + to];
        const int exponent =
            divisors[to] / divisors[from] - 1;
        factors.emplace_back(base, exponent);
        to = from;
      }
      return {
          certified_result.actual_cost / std::log(10.0L),
          std::move(factors),
      };
    }
  }

  throw std::runtime_error("prime search limit was insufficient");
}

u64 exact_value(
    const std::vector<std::pair<int, int>>& factors) {
  u64 result = 1;
  for (const auto& [base, exponent] : factors) {
    for (int count = 0; count < exponent; ++count) {
      result *= base;
    }
  }
  return result;
}

int main() {
  const std::vector<int> primes = prime_sieve(PRIME_LIMIT);
  long double total_logarithm = 0;
  long double hundred_logarithm = 0;
  u64 twenty_product = 1;

  for (int modulus : primes) {
    if (modulus >= TARGET) {
      break;
    }
    const MinimumValue minimum = minimum_s(modulus, primes);
    total_logarithm += minimum.logarithm;
    if (modulus < 100) {
      hundred_logarithm += minimum.logarithm;
    }
    if (modulus < 20) {
      twenty_product *= exact_value(minimum.factors);
    }
  }

  assert(twenty_product == 1'348'422'598'656ULL);
  const long double hundred_exponent =
      std::floor(hundred_logarithm);
  const long double hundred_mantissa =
      std::pow(10.0L, hundred_logarithm - hundred_exponent);
  assert(std::fabs(hundred_mantissa - 1.37451L) < 0.000005L);

  long long exponent =
      static_cast<long long>(std::floor(total_logarithm));
  long double mantissa =
      std::pow(10.0L, total_logarithm - exponent);
  if (std::round(mantissa * 100'000) >= 1'000'000) {
    mantissa /= 10;
    ++exponent;
  }
  std::cout << std::fixed << std::setprecision(5)
            << mantissa << 'e' << exponent << '\n';
}
