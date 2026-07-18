#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <limits>
#include <numeric>
#include <string>

using u64 = std::uint64_t;
using u128 = unsigned __int128;
using i128 = __int128;

constexpr u64 TARGET = 1'000'000'000'039ULL;

std::array<u64, 96> fibonacci{};
u64 target;
int total_sum;
int prefix_sum = 28;
u64 best_denominator;

u64 inverse_mod(u64 value, u64 modulus) {
  i128 old_r = value;
  i128 r = modulus;
  i128 old_s = 1;
  i128 s = 0;

  while (r != 0) {
    const i128 quotient = old_r / r;
    const i128 next_r = old_r - quotient * r;
    old_r = r;
    r = next_r;
    const i128 next_s = old_s - quotient * s;
    old_s = s;
    s = next_s;
  }

  old_s %= modulus;
  if (old_s < 0) {
    old_s += modulus;
  }
  return static_cast<u64>(old_s);
}

int quotient_sum(u64 first, u64 second) {
  int result = 0;
  while (second != 0) {
    result += static_cast<int>(first / second);
    const u64 remainder = first % second;
    first = second;
    second = remainder;
  }
  return result;
}

void complete_suffix(
    u64 numerator,
    u64 previous_numerator,
    u64 denominator,
    u64 previous_denominator,
    int remaining
) {
  if (numerator == 1) {
    return;
  }

  const u64 residue = static_cast<u64>(
      static_cast<u128>(target % numerator)
      * inverse_mod(previous_numerator, numerator)
      % numerator
  );
  u64 minimum_second = 1;
  const u128 largest_first_term =
      static_cast<u128>(numerator)
      * fibonacci[remaining + 1];
  if (largest_first_term < target) {
    minimum_second = static_cast<u64>(
        (target - largest_first_term
         + previous_numerator - 1)
        / previous_numerator
    );
  }

  u64 suffix_second = residue == 0 ? numerator : residue;
  if (suffix_second < minimum_second) {
    suffix_second += static_cast<u64>(
        (static_cast<u128>(
             minimum_second - suffix_second
         ) + numerator - 1)
        / numerator
        * numerator
    );
  }
  const u64 maximum_second = std::min(
      fibonacci[remaining],
      target / (numerator + previous_numerator)
  );

  for (
      ;
      suffix_second <= maximum_second;
      suffix_second += numerator
  ) {
    const u64 remainder =
        target - suffix_second * previous_numerator;
    if (remainder % numerator != 0) {
      continue;
    }
    const u64 suffix_first = remainder / numerator;
    if (
        suffix_first < suffix_second
        || suffix_first > fibonacci[remaining + 1]
        || std::gcd(suffix_first, suffix_second) != 1
        || quotient_sum(suffix_first, suffix_second) != remaining
    ) {
      continue;
    }

    const u64 final_denominator = static_cast<u64>(
        static_cast<u128>(suffix_first) * denominator
        + static_cast<u128>(suffix_second) * previous_denominator
    );
    best_denominator =
        std::min(best_denominator, final_denominator);

    if (maximum_second - suffix_second < numerator) {
      break;
    }
  }
}

void search_prefix(
    u64 numerator,
    u64 previous_numerator,
    u64 denominator,
    u64 previous_denominator,
    int used
) {
  const int remaining = total_sum - used;
  if (remaining == 0) {
    if (numerator == target) {
      best_denominator =
          std::min(best_denominator, denominator);
    }
    return;
  }

  const u128 minimum =
      static_cast<u128>(remaining) * numerator
      + previous_numerator;
  const u128 maximum =
      static_cast<u128>(fibonacci[remaining + 1]) * numerator
      + static_cast<u128>(fibonacci[remaining])
            * previous_numerator;
  if (target < minimum || target > maximum) {
    return;
  }

  if (used >= prefix_sum && numerator > 1) {
    complete_suffix(
        numerator,
        previous_numerator,
        denominator,
        previous_denominator,
        remaining
    );
    return;
  }

  for (int digit = 1; digit <= remaining; ++digit) {
    const u128 next_numerator =
        static_cast<u128>(digit) * numerator
        + previous_numerator;
    if (next_numerator > target) {
      break;
    }
    const u64 next_denominator =
        digit * denominator + previous_denominator;
    search_prefix(
        static_cast<u64>(next_numerator),
        numerator,
        next_denominator,
        denominator,
        used + digit
    );
  }
}

u64 least_labour_companion(u64 wanted) {
  target = wanted;
  int first_possible_sum = 1;
  while (fibonacci[first_possible_sum + 1] < target) {
    ++first_possible_sum;
  }

  for (total_sum = first_possible_sum; ; ++total_sum) {
    best_denominator = std::numeric_limits<u64>::max();
    search_prefix(1, 0, 0, 1, 0);
    if (best_denominator != std::numeric_limits<u64>::max()) {
      return best_denominator;
    }
  }
}

int main(int argc, char** argv) {
  fibonacci[1] = 1;
  for (std::size_t index = 2; index < fibonacci.size(); ++index) {
    const u128 next =
        static_cast<u128>(fibonacci[index - 1])
        + fibonacci[index - 2];
    fibonacci[index] = next > std::numeric_limits<u64>::max()
        ? std::numeric_limits<u64>::max()
        : static_cast<u64>(next);
  }

  if (argc == 2) {
    std::cout
        << least_labour_companion(std::stoull(argv[1]))
        << '\n';
    return 0;
  }

  if (argc >= 3) {
    target = std::stoull(argv[1]);
    total_sum = std::stoi(argv[2]);
    if (argc >= 5) {
      prefix_sum = std::stoi(argv[4]);
    }
    best_denominator = std::numeric_limits<u64>::max();
    const int first_begin =
        argc >= 4 ? std::stoi(argv[3]) : 1;
    const int first_end =
        argc >= 4 ? first_begin : total_sum;
    for (int first_digit = first_begin;
         first_digit <= first_end; ++first_digit) {
      search_prefix(
          first_digit, 1, 1, 0, first_digit
      );
    }
    std::cout << (
        best_denominator == std::numeric_limits<u64>::max()
            ? 0
            : best_denominator
    ) << '\n';
    return 0;
  }

  if (
      least_labour_companion(7) != 2
      || least_labour_companion(89) != 34
      || least_labour_companion(8191) != 1856
  ) {
    std::cerr << "sample self-check failed\n";
    return 1;
  }

  std::cout << least_labour_companion(TARGET) << '\n';
}
