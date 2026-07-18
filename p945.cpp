#include <cstdint>
#include <iostream>
#include <vector>

using u32 = std::uint32_t;
using u64 = std::uint64_t;

constexpr u32 TARGET = 10'000'000;
constexpr u32 POLYNOMIAL_SPACE = 1U << 24;

int degree(u32 polynomial) {
  return 31 - __builtin_clz(polynomial);
}

u32 polynomial_remainder(u32 dividend, u32 divisor) {
  const int divisor_degree = degree(divisor);
  while (dividend != 0 && degree(dividend) >= divisor_degree) {
    dividend ^= divisor << (degree(dividend) - divisor_degree);
  }
  return dividend;
}

u32 polynomial_gcd(u32 a, u32 b) {
  while (b != 0) {
    const u32 remainder = polynomial_remainder(a, b);
    a = b;
    b = remainder;
  }
  return a;
}

u32 polynomial_quotient(u32 dividend, u32 divisor) {
  u32 quotient = 0;
  const int divisor_degree = degree(divisor);
  while (dividend != 0) {
    const int shift = degree(dividend) - divisor_degree;
    if (shift < 0) {
      break;
    }
    quotient |= 1U << shift;
    dividend ^= divisor << shift;
  }
  return quotient;
}

// Compact bits 0,2,4,... into consecutive low bits.
u32 compact_even_bits(u32 value) {
  value &= 0x55555555U;
  value = (value | (value >> 1)) & 0x33333333U;
  value = (value | (value >> 2)) & 0x0f0f0f0fU;
  value = (value | (value >> 4)) & 0x00ff00ffU;
  value = (value | (value >> 8)) & 0x0000ffffU;
  return value;
}

// Put consecutive low bits into positions 0,2,4,...
u32 spread_even_bits(u32 value) {
  value &= 0x0000ffffU;
  value = (value | (value << 8)) & 0x00ff00ffU;
  value = (value | (value << 4)) & 0x0f0f0f0fU;
  value = (value | (value << 2)) & 0x33333333U;
  value = (value | (value << 1)) & 0x55555555U;
  return value;
}

u32 square_class(u32 polynomial) {
  const u32 even = compact_even_bits(polynomial);
  const u32 odd = compact_even_bits(polynomial >> 1);
  const u32 common = polynomial_gcd(even, odd);
  const u32 reduced_even = polynomial_quotient(even, common);
  const u32 reduced_odd = polynomial_quotient(odd, common);
  return spread_even_bits(reduced_even)
         | (spread_even_bits(reduced_odd) << 1);
}

u64 count_solutions(u32 limit) {
  std::vector<u32> frequency(POLYNOMIAL_SPACE);
  for (u32 value = 1; value <= limit; ++value) {
    ++frequency[square_class(value)];
  }

  // a=0 gives one solution for every b.  For nonzero pairs, use the
  // representative not divisible by x to count each unordered pair once.
  u64 answer = static_cast<u64>(limit) + 1;
  for (u32 representative = 1;
       representative < POLYNOMIAL_SPACE / 2;
       representative += 2) {
    answer += static_cast<u64>(frequency[representative])
              * frequency[representative << 1];
  }
  return answer;
}

int main() {
  if (count_solutions(10) != 21) {
    std::cerr << "sample self-check failed\n";
    return 1;
  }
  std::cout << count_solutions(TARGET) << '\n';
}
