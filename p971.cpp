#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>

using u64 = std::uint64_t;

constexpr int LIMIT = 100'000'000;

u64 modular_power(u64 base, u64 exponent, u64 modulus) {
  u64 result = 1;
  while (exponent != 0) {
    if ((exponent & 1) != 0) {
      result = result * base % modulus;
    }
    base = base * base % modulus;
    exponent >>= 1;
  }
  return result;
}

u64 periodic_points(int prime) {
  const u64 subgroup_size = (prime - 1) / 5;

  u64 generator = 1;
  for (u64 base = 2; generator == 1; ++base) {
    generator = modular_power(base, subgroup_size, prime);
  }

  std::array<u64, 5> roots{};
  roots[0] = 1;
  for (int index = 1; index < 5; ++index) {
    roots[index] = roots[index - 1] * generator % prime;
  }

  std::array<int, 5> next{};
  for (int index = 0; index < 5; ++index) {
    const u64 quotient = modular_power(
        (roots[index] + 1) % prime,
        subgroup_size,
        prime
    );
    const u64 next_root = roots[index] * quotient % prime;
    const auto iterator = std::find(
        roots.begin(), roots.end(), next_root
    );
    assert(iterator != roots.end());
    next[index] = iterator - roots.begin();
  }

  int cyclic_states = 0;
  for (int start = 0; start < 5; ++start) {
    int state = next[start];
    for (int steps = 1; steps <= 5; ++steps) {
      if (state == start) {
        ++cyclic_states;
        break;
      }
      state = next[state];
    }
  }
  return 1 + subgroup_size * cyclic_states;
}

std::vector<bool> prime_sieve(int limit) {
  std::vector<bool> is_prime(limit + 1, true);
  is_prime[0] = is_prime[1] = false;
  for (int prime = 2; prime * prime <= limit; ++prime) {
    if (!is_prime[prime]) {
      continue;
    }
    for (int multiple = prime * prime;
         multiple <= limit;
         multiple += prime) {
      is_prime[multiple] = false;
    }
  }
  return is_prime;
}

u64 sum_periodic_points(int limit) {
  const std::vector<bool> is_prime = prime_sieve(limit);
  u64 result = 0;
  for (int prime = 11; prime <= limit; prime += 5) {
    if (is_prime[prime]) {
      result += periodic_points(prime);
    }
  }
  return result;
}

int main(int argc, char** argv) {
  assert(periodic_points(11) == 7);
  assert(sum_periodic_points(100) == 127);

  if (argc == 3 && std::string(argv[1]) == "--prime") {
    std::cout << periodic_points(std::stoi(argv[2])) << '\n';
  } else {
    const int limit = argc > 1 ? std::stoi(argv[1]) : LIMIT;
    std::cout << sum_periodic_points(limit) << '\n';
  }
}
