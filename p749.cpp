#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <string>
#include <unordered_set>
#include <vector>

static constexpr unsigned long long LIMIT_16 = 9'999'999'999'999'999ULL;
static constexpr int MAX_EXPONENT = 60;

class Finder {
 public:
  explicit Finder(int max_digits) : max_digits_(max_digits) {
    limit_ = 1;
    for (int i = 0; i < max_digits; ++i) limit_ *= 10;
    --limit_;
  }

  unsigned long long sum() {
    found_.clear();
    for (int exponent = 1; exponent <= MAX_EXPONENT; ++exponent) {
      build_powers(exponent);
      counts_.fill(0);
      search(1, 0, 0);
    }

    unsigned long long total = 0;
    for (unsigned long long value : found_) total += value;
    return total;
  }

 private:
  int max_digits_;
  unsigned long long limit_;
  std::array<unsigned long long, 10> powers_{};
  std::array<int, 10> counts_{};
  std::unordered_set<unsigned long long> found_;

  void build_powers(int exponent) {
    unsigned long long cap = limit_ + 1;
    powers_[0] = 0;
    powers_[1] = 1;
    for (int digit = 2; digit <= 9; ++digit) {
      __int128 value = 1;
      for (int i = 0; i < exponent; ++i) {
        value *= digit;
        if (value > cap) {
          value = cap;
          break;
        }
      }
      powers_[digit] = static_cast<unsigned long long>(value);
    }
  }

  bool has_matching_digits(unsigned long long value) const {
    std::array<int, 10> actual{};
    while (value > 0) {
      ++actual[value % 10];
      value /= 10;
    }
    int digits = 0;
    for (int digit = 0; digit <= 9; ++digit) digits += actual[digit];
    if (digits > max_digits_) return false;
    for (int digit = 1; digit <= 9; ++digit) {
      if (actual[digit] != counts_[digit]) return false;
    }
    return true;
  }

  void test(unsigned long long total) {
    if (total > 1) {
      unsigned long long candidate = total - 1;
      if (candidate <= limit_ && has_matching_digits(candidate)) found_.insert(candidate);
    }
    if (total < limit_) {
      unsigned long long candidate = total + 1;
      if (candidate <= limit_ && has_matching_digits(candidate)) found_.insert(candidate);
    }
  }

  void search(int digit, int used_digits, unsigned long long total) {
    if (digit == 10) {
      if (used_digits > 0) test(total);
      return;
    }

    int remaining = max_digits_ - used_digits;
    for (int count = 0; count <= remaining; ++count) {
      __int128 next = static_cast<__int128>(total) + static_cast<__int128>(count) * powers_[digit];
      if (next > limit_ + 1) break;
      counts_[digit] = count;
      search(digit + 1, used_digits + count, static_cast<unsigned long long>(next));
    }
    counts_[digit] = 0;
  }
};

int main(int argc, char **argv) {
  int digits = 16;
  if (argc > 1) {
    digits = std::stoi(argv[1]);
  }
  Finder finder(digits);
  std::cout << finder.sum() << '\n';
  return 0;
}
