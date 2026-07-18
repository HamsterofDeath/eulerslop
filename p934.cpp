#include <algorithm>
#include <cstdint>
#include <iostream>
#include <vector>

using u64 = std::uint64_t;

u64 modular_power(u64 base, u64 exponent, u64 modulus) {
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

bool is_prime(int candidate, const std::vector<int>& primes) {
  for (const int prime : primes) {
    if (1LL * prime * prime > candidate) {
      break;
    }
    if (candidate % prime == 0) {
      return false;
    }
  }
  return true;
}

u64 represented_count(
    const std::vector<u64>& residues,
    u64 modulus,
    u64 limit
) {
  const u64 full_cycles = limit / modulus;
  const u64 remainder = limit % modulus;
  u64 result = full_cycles * residues.size();
  for (const u64 residue : residues) {
    if (residue != 0 && residue <= remainder) {
      ++result;
    }
  }
  return result;
}

u64 unlucky_prime_sum(u64 limit) {
  // Initially the single residue 0 modulo 1 represents every n.
  std::vector<u64> survivors{0};
  u64 modulus = 1;
  bool explicit_numbers = false;
  u64 survivor_count = limit;
  u64 result = 0;

  std::vector<int> primes;
  for (
      int candidate = 2;
      survivor_count != 0;
      candidate = candidate == 2 ? 3 : candidate + 2
  ) {
    if (!is_prime(candidate, primes)) {
      continue;
    }
    primes.push_back(candidate);
    const u64 prime = candidate;
    u64 next_survivor_count;

    if (explicit_numbers) {
      std::size_t write = 0;
      for (const u64 number : survivors) {
        if ((number % prime) % 7 == 0) {
          survivors[write++] = number;
        }
      }
      survivors.resize(write);
      next_survivor_count = survivors.size();
    } else {
      const int allowed_count =
          (candidate + 6) / 7;
      const bool remains_periodic =
          modulus <= limit / prime;
      const u64 next_modulus = modulus * prime;
      std::vector<u64> next;
      if (remains_periodic) {
        next.reserve(
            survivors.size() * allowed_count
        );
      } else {
        next.reserve(survivors.size() * 2);
      }

      const u64 inverse_modulus =
          modular_power(
              modulus % prime,
              prime - 2,
              prime
          );
      for (const u64 residue : survivors) {
        const u64 residue_mod_prime = residue % prime;
        for (
            u64 allowed = 0;
            allowed < prime;
            allowed += 7
        ) {
          const u64 difference =
              (
                  allowed + prime - residue_mod_prime
              ) % prime;
          const u64 multiplier =
              difference * inverse_modulus % prime;
          const u64 combined =
              residue + modulus * multiplier;

          if (
              remains_periodic
              || (combined != 0 && combined <= limit)
          ) {
            next.push_back(combined);
          }
        }
      }
      survivors.swap(next);
      modulus = next_modulus;

      if (remains_periodic) {
        next_survivor_count =
            represented_count(
                survivors, modulus, limit
            );
      } else {
        explicit_numbers = true;
        next_survivor_count = survivors.size();
      }
    }

    result += prime
        * (survivor_count - next_survivor_count);
    survivor_count = next_survivor_count;
  }
  return result;
}

int main(int argc, char** argv) {
  const u64 limit =
      argc > 1 ? std::stoull(argv[1])
               : 100'000'000'000'000'000ULL;

  if (unlucky_prime_sum(1470) != 4293) {
    std::cerr << "sample self-check failed\n";
    return 1;
  }
  std::cout << unlucky_prime_sum(limit) << '\n';
}
