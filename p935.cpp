#include <cmath>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <vector>

using u64 = std::uint64_t;

// The endpoint of the exceptional final-contact rotation interval.
// Iterating the corner-to-corner map brackets it between
// 0.7645565447088691 and 0.7645566047088679; this value is therefore
// sufficient to classify every fraction needed for N=10^8.
constexpr long double ROTATION_THRESHOLD = 0.76455657L;

std::vector<int> distinct_prime_factors(u64 value) {
  std::vector<int> factors;
  for (u64 prime = 2; prime * prime <= value; ++prime) {
    if (value % prime != 0) {
      continue;
    }
    factors.push_back(static_cast<int>(prime));
    do {
      value /= prime;
    } while (value % prime == 0);
  }
  if (value > 1) {
    factors.push_back(static_cast<int>(value));
  }
  return factors;
}

u64 coprime_count(
    u64 maximum,
    const std::vector<int>& prime_factors
) {
  std::int64_t result = 0;
  const int subsets = 1 << prime_factors.size();
  for (int mask = 0; mask < subsets; ++mask) {
    u64 divisor = 1;
    int parity = 0;
    for (
        int index = 0;
        index < static_cast<int>(prime_factors.size());
        ++index
    ) {
      if (mask & (1 << index)) {
        divisor *= prime_factors[index];
        parity ^= 1;
      }
    }
    if (parity == 0) {
      result += maximum / divisor;
    } else {
      result -= maximum / divisor;
    }
  }
  return static_cast<u64>(result);
}

u64 totient_prefix(int limit) {
  std::vector<std::uint32_t> totient(limit + 1);
  std::iota(totient.begin(), totient.end(), 0);
  for (int prime = 2; prime <= limit; ++prime) {
    if (totient[prime] != static_cast<unsigned int>(prime)) {
      continue;
    }
    for (
        int multiple = prime;
        multiple <= limit;
        multiple += prime
    ) {
      totient[multiple] -= totient[multiple] / prime;
    }
  }

  u64 result = 0;
  for (int value = 1; value <= limit; ++value) {
    result += totient[value];
  }
  return result;
}

u64 rolling_square_count(int maximum_steps) {
  const int complete_layer = maximum_steps / 2;
  const u64 final_denominator =
      static_cast<u64>(complete_layer) + 1;
  const std::vector<int> factors =
      distinct_prime_factors(final_denominator);

  u64 final_totient = final_denominator;
  for (const int prime : factors) {
    final_totient =
        final_totient / prime * (prime - 1);
  }

  // Positive coprime pairs with sum at most K contribute
  // sum_{q=2}^K phi(q) = Phi(K)-1.
  const u64 complete_count =
      totient_prefix(complete_layer) - 1;

  // In layer K+1, all fractions return in 2q-2 steps except
  // those in the critical interval [3/4, rho], which need 2q.
  const u64 exceptional_first =
      (3 * final_denominator + 3) / 4;
  const u64 exceptional_last = static_cast<u64>(
      std::floor(
          ROTATION_THRESHOLD * final_denominator
      )
  );
  u64 exceptional_count = 0;
  if (exceptional_first <= exceptional_last) {
    exceptional_count =
        coprime_count(exceptional_last, factors)
        - coprime_count(exceptional_first - 1, factors);
  }

  return complete_count
      + final_totient
      - exceptional_count;
}

int main(int argc, char** argv) {
  const int maximum_steps =
      argc > 1 ? std::stoi(argv[1]) : 100'000'000;

  if (
      rolling_square_count(6) != 4
      || rolling_square_count(100) != 805
  ) {
    std::cerr << "sample self-check failed\n";
    return 1;
  }
  std::cout << rolling_square_count(maximum_steps) << '\n';
}
