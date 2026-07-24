#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <unordered_map>
#include <vector>

using u32 = std::uint32_t;
using u64 = std::uint64_t;

constexpr u64 MODULUS = 1'000'000'007;
constexpr u64 INVERSE_TWO = 500'000'004;
constexpr u64 INVERSE_SIX = 166'666'668;
constexpr int SIEVE_LIMIT = 3'000'000;

using Sums = std::array<u32, 3>;

u64 add_mod(u64 first, u64 second) {
  const u64 sum = first + second;
  return sum >= MODULUS ? sum - MODULUS : sum;
}

u64 subtract_mod(u64 first, u64 second) {
  return first >= second ? first - second
                         : first + MODULUS - second;
}

u64 multiply_mod(u64 first, u64 second) {
  return first * second % MODULUS;
}

u64 sum_first_powers(u64 n) {
  const u64 reduced = n % MODULUS;
  return multiply_mod(
      multiply_mod(reduced, (reduced + 1) % MODULUS),
      INVERSE_TWO);
}

u64 sum_second_powers(u64 n) {
  const u64 reduced = n % MODULUS;
  return multiply_mod(
      multiply_mod(
          multiply_mod(reduced, (reduced + 1) % MODULUS),
          (2 * reduced + 1) % MODULUS),
      INVERSE_SIX);
}

u64 sum_third_powers(u64 n) {
  const u64 triangular = sum_first_powers(n);
  return multiply_mod(triangular, triangular);
}

class TotientSums {
 public:
  TotientSums()
      : sum_phi_(SIEVE_LIMIT + 1),
        sum_n_phi_(SIEVE_LIMIT + 1),
        sum_n2_phi_(SIEVE_LIMIT + 1) {
    build_sieve();
    memo_.reserve(200'000);
  }

  Sums get(u64 n) {
    if (n <= SIEVE_LIMIT) {
      return {sum_phi_[n], sum_n_phi_[n], sum_n2_phi_[n]};
    }
    const auto found = memo_.find(n);
    if (found != memo_.end()) {
      return found->second;
    }

    Sums answer{
        static_cast<u32>(sum_first_powers(n)),
        static_cast<u32>(sum_second_powers(n)),
        static_cast<u32>(sum_third_powers(n)),
    };

    for (u64 left = 2; left <= n;) {
      const u64 quotient = n / left;
      const u64 right = n / quotient;
      const Sums lower = get(quotient);

      const std::array<u64, 3> coefficients{
          (right - left + 1) % MODULUS,
          subtract_mod(sum_first_powers(right),
                       sum_first_powers(left - 1)),
          subtract_mod(sum_second_powers(right),
                       sum_second_powers(left - 1)),
      };
      for (int degree = 0; degree < 3; ++degree) {
        answer[degree] = static_cast<u32>(
            subtract_mod(answer[degree],
                         multiply_mod(coefficients[degree],
                                      lower[degree])));
      }
      left = right + 1;
    }

    memo_.emplace(n, answer);
    return answer;
  }

 private:
  std::vector<u32> sum_phi_;
  std::vector<u32> sum_n_phi_;
  std::vector<u32> sum_n2_phi_;
  std::unordered_map<u64, Sums> memo_;

  void build_sieve() {
    std::vector<int> primes;
    sum_phi_[1] = 1;

    for (int value = 2; value <= SIEVE_LIMIT; ++value) {
      if (sum_phi_[value] == 0) {
        sum_phi_[value] = value - 1;
        primes.push_back(value);
      }
      for (int prime : primes) {
        const u64 product = static_cast<u64>(value) * prime;
        if (product > SIEVE_LIMIT) {
          break;
        }
        if (value % prime == 0) {
          sum_phi_[product] = sum_phi_[value] * prime;
          break;
        }
        sum_phi_[product] = sum_phi_[value] * (prime - 1);
      }
    }

    u64 prefix_phi = 0;
    u64 prefix_n_phi = 0;
    u64 prefix_n2_phi = 0;
    for (u64 value = 1; value <= SIEVE_LIMIT; ++value) {
      const u64 phi = sum_phi_[value];
      const u64 reduced = value % MODULUS;
      prefix_phi = add_mod(prefix_phi, phi);
      prefix_n_phi =
          add_mod(prefix_n_phi, multiply_mod(reduced, phi));
      prefix_n2_phi =
          add_mod(prefix_n2_phi,
                  multiply_mod(multiply_mod(reduced, reduced), phi));
      sum_phi_[value] = static_cast<u32>(prefix_phi);
      sum_n_phi_[value] = static_cast<u32>(prefix_n_phi);
      sum_n2_phi_[value] = static_cast<u32>(prefix_n2_phi);
    }
  }
};

u64 choose_two(u64 n) {
  const u64 reduced = n % MODULUS;
  return multiply_mod(
      multiply_mod(reduced, (reduced + MODULUS - 1) % MODULUS),
      INVERSE_TWO);
}

u64 choose_three(u64 n) {
  const u64 reduced = n % MODULUS;
  return multiply_mod(
      multiply_mod(
          multiply_mod(reduced,
                       (reduced + MODULUS - 1) % MODULUS),
          (reduced + MODULUS - 2) % MODULUS),
      INVERSE_SIX);
}

u64 pairwise_intersecting_triples(u64 m, u64 n) {
  u64 answer = multiply_mod(choose_three(m), choose_three(n));
  answer = add_mod(
      answer,
      multiply_mod(
          multiply_mod(m % MODULUS,
                       (m - 1) % MODULUS),
          choose_three(n + 1)));
  answer = add_mod(
      answer,
      multiply_mod(
          multiply_mod(n % MODULUS,
                       (n - 1) % MODULUS),
          choose_three(m + 1)));
  answer = subtract_mod(
      answer,
      multiply_mod(2,
                   multiply_mod(choose_two(m), choose_two(n))));
  return answer;
}

u64 concurrent_triples(u64 m, u64 n, TotientSums& totients) {
  const u64 m_span = m - 1;
  const u64 n_span = n - 1;
  const u64 limit = std::min(m_span, n_span);
  u64 answer = 0;

  for (u64 left = 2; left <= limit;) {
    const u64 m_quotient = m_span / left;
    const u64 n_quotient = n_span / left;
    const u64 right = std::min(
        {limit, m_span / m_quotient, n_span / n_quotient});

    const u64 m_q = m_quotient % MODULUS;
    const u64 n_q = n_quotient % MODULUS;
    const u64 m_triangular = multiply_mod(
        multiply_mod(m_q, (m_q + 1) % MODULUS),
        INVERSE_TWO);
    const u64 n_triangular = multiply_mod(
        multiply_mod(n_q, (n_q + 1) % MODULUS),
        INVERSE_TWO);

    const u64 constant = multiply_mod(
        multiply_mod(m_q, n_q),
        multiply_mod(m % MODULUS, n % MODULUS));
    const u64 linear = add_mod(
        multiply_mod(multiply_mod(m_q, m % MODULUS),
                     n_triangular),
        multiply_mod(multiply_mod(n_q, n % MODULUS),
                     m_triangular));
    const u64 quadratic =
        multiply_mod(m_triangular, n_triangular);

    const Sums before = totients.get(left - 1);
    const Sums through = totients.get(right);
    const u64 phi_sum =
        subtract_mod(through[0], before[0]);
    const u64 h_phi_sum =
        subtract_mod(through[1], before[1]);
    const u64 h2_phi_sum =
        subtract_mod(through[2], before[2]);

    u64 block = multiply_mod(constant, phi_sum);
    block = subtract_mod(block, multiply_mod(linear, h_phi_sum));
    block = add_mod(block,
                    multiply_mod(quadratic, h2_phi_sum));
    answer = add_mod(answer, block);
    left = right + 1;
  }
  return answer;
}

u64 triangle_count(u64 m, u64 n, TotientSums& totients) {
  return subtract_mod(pairwise_intersecting_triples(m, n),
                      concurrent_triples(m, n, totients));
}

int main() {
  TotientSums totients;
  assert(triangle_count(2, 3, totients) == 8);
  assert(triangle_count(3, 5, totients) == 146);
  assert(triangle_count(12, 23, totients) == 756'716);

  constexpr u64 M = 1234ULL * 100'000'000;
  constexpr u64 N = 2345ULL * 100'000'000;
  std::cout << triangle_count(M, N, totients) << '\n';
}
