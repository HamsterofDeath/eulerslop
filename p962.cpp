#include <algorithm>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <limits>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>

using u64 = std::uint64_t;
using u128 = unsigned __int128;

constexpr int TARGET_PERIMETER = 1'000'000;

u64 integer_sqrt(u64 value) {
  u64 root = static_cast<u64>(
      std::sqrt(static_cast<long double>(value))
  );
  while (static_cast<u128>(root + 1) * (root + 1) <= value) {
    ++root;
  }
  while (static_cast<u128>(root) * root > value) {
    --root;
  }
  return root;
}

u64 ceil_sqrt_ratio(u64 numerator, u64 denominator) {
  u64 root = integer_sqrt(numerator / denominator);
  while (
      static_cast<u128>(root) * root * denominator
      < numerator
  ) {
    ++root;
  }
  return root;
}

struct Sieve {
  std::vector<int> smallest_prime;
  std::vector<int> squarefree_kernel;
};

Sieve make_sieve(int limit) {
  Sieve sieve;
  sieve.smallest_prime.resize(limit + 1);
  sieve.squarefree_kernel.resize(limit + 1);
  sieve.squarefree_kernel[1] = 1;

  for (int value = 2; value <= limit; ++value) {
    if (sieve.smallest_prime[value] == 0) {
      for (int multiple = value; multiple <= limit;
           multiple += value) {
        if (sieve.smallest_prime[multiple] == 0) {
          sieve.smallest_prime[multiple] = value;
        }
      }
    }

    int remaining = value;
    int kernel = 1;
    while (remaining > 1) {
      const int prime = sieve.smallest_prime[remaining];
      int parity = 0;
      do {
        remaining /= prime;
        parity ^= 1;
      } while (
          remaining > 1
          && sieve.smallest_prime[remaining] == prime
      );
      if (parity != 0) {
        kernel *= prime;
      }
    }
    sieve.squarefree_kernel[value] = kernel;
  }
  return sieve;
}

std::vector<u64> squarefree_divisors(
    int first,
    int second,
    const std::vector<int>& smallest_prime
) {
  std::vector<int> primes;
  for (int value : {first, second}) {
    while (value > 1) {
      const int prime = smallest_prime[value];
      primes.push_back(prime);
      do {
        value /= prime;
      } while (
          value > 1
          && smallest_prime[value] == prime
      );
    }
  }

  std::vector<u64> divisors{1};
  for (const int prime : primes) {
    const std::size_t previous_size = divisors.size();
    for (std::size_t index = 0; index < previous_size; ++index) {
      divisors.push_back(divisors[index] * prime);
    }
  }
  return divisors;
}

u64 triangle_count(int perimeter_limit) {
  const int half_limit = perimeter_limit / 2;
  const Sieve sieve = make_sieve(half_limit);
  u64 result = 0;

  // A=d*alpha and B=d*beta are g-w and g+w, where
  // a:g=u, b:g=v, and c=(u+v)w.
  for (int beta = 3; beta <= half_limit; ++beta) {
    const int beta_kernel = sieve.squarefree_kernel[beta];
    const int beta_square =
        static_cast<int>(integer_sqrt(beta / beta_kernel));
    const u64 reduced_sum_limit = perimeter_limit / beta;

    const u64 kernel_bound =
        reduced_sum_limit * reduced_sum_limit
        / (4ULL * beta_kernel);
    const int alpha_kernel_limit = static_cast<int>(
        std::min<u64>(beta / 3, kernel_bound)
    );

    for (
        int alpha_kernel = 1;
        alpha_kernel <= alpha_kernel_limit;
        ++alpha_kernel
    ) {
      if (
          sieve.squarefree_kernel[alpha_kernel]
              != alpha_kernel
          || std::gcd(alpha_kernel, beta_kernel) != 1
      ) {
        continue;
      }

      const u64 combined_kernel =
          static_cast<u64>(alpha_kernel) * beta_kernel;
      const std::vector<u64> divisors = squarefree_divisors(
          alpha_kernel,
          beta_kernel,
          sieve.smallest_prime
      );

      u64 minimum_reduced_sum =
          std::numeric_limits<u64>::max();
      for (const u64 divisor : divisors) {
        minimum_reduced_sum = std::min(
            minimum_reduced_sum,
            divisor + combined_kernel / divisor
        );
      }
      if (minimum_reduced_sum > reduced_sum_limit) {
        continue;
      }

      const int alpha_square_limit = static_cast<int>(
          integer_sqrt(beta / (3ULL * alpha_kernel))
      );
      for (
          int alpha_square = 1;
          alpha_square <= alpha_square_limit;
          ++alpha_square
      ) {
        const int alpha =
            alpha_kernel * alpha_square * alpha_square;
        if (std::gcd(alpha, beta) != 1) {
          continue;
        }

        for (const u64 first_kernel : divisors) {
          const u64 second_kernel =
              combined_kernel / first_kernel;
          if (first_kernel >= reduced_sum_limit) {
            continue;
          }

          const u64 first_square_limit = integer_sqrt(
              (reduced_sum_limit - 1) / first_kernel
          );
          for (
              u64 first_square = 1;
              first_square <= first_square_limit;
              ++first_square
          ) {
            if (std::gcd(first_square, second_kernel) != 1) {
              continue;
            }

            const u64 first_side =
                first_kernel * first_square * first_square;
            const u64 ratio_limit = static_cast<u64>(
                static_cast<u128>(beta - alpha) * first_side
                / (2ULL * alpha)
            );
            const u64 maximum_second_side = std::min(
                reduced_sum_limit - first_side,
                ratio_limit
            );
            if (maximum_second_side < first_side) {
              continue;
            }

            const u64 minimum_second_square =
                ceil_sqrt_ratio(first_side, second_kernel);
            const u64 maximum_second_square = integer_sqrt(
                maximum_second_side / second_kernel
            );

            for (
                u64 second_square = minimum_second_square;
                second_square <= maximum_second_square;
                ++second_square
            ) {
              if (
                  std::gcd(
                      second_square,
                      first_kernel * first_square
                  )
                  != 1
              ) {
                continue;
              }

              const u64 second_side =
                  second_kernel
                  * second_square * second_square;
              const u64 maximum_scale =
                  reduced_sum_limit
                  / (first_side + second_side);

              u64 required_scale = second_square / std::gcd(
                  second_square,
                  static_cast<u64>(
                      alpha_square * beta_square
                  )
              );
              if ((alpha & 1) == 0 || (beta & 1) == 0) {
                required_scale = std::lcm(required_scale, u64{2});
              }
              result += maximum_scale / required_scale;
            }
          }
        }
      }
    }
  }
  return result;
}

int main(int argc, char** argv) {
  const int limit =
      argc > 1 ? std::stoi(argv[1]) : TARGET_PERIMETER;

  if (
      triangle_count(50) != 8
      || triangle_count(100) != 26
      || triangle_count(200) != 71
  ) {
    throw std::runtime_error("small-case self-check failed");
  }

  std::cout << triangle_count(limit) << '\n';
}
