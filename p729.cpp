#include <cmath>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

static constexpr int TARGET = 25;

class PeriodicRanges {
 public:
  explicit PeriodicRanges(int limit) : limit_(limit) {}

  long double sum() {
    total_ = 0;
    for (int n = 1; n <= limit_; ++n) {
      word_.assign(n + 1, 0);
      generate(n, 1, 1);
    }
    return total_;
  }

 private:
  int limit_;
  std::vector<int> word_;
  long double total_ = 0;

  static long double inverse_branch(int bit, long double y, long double &derivative) {
    long double root = std::sqrt(y * y + 4);
    if (bit) {
      derivative *= (1 + y / root) / 2;
      return (y + root) / 2;
    }
    derivative *= (1 - y / root) / 2;
    return (y - root) / 2;
  }

  long double fixed_point(int n) const {
    long double x = 0;
    for (int iteration = 0; iteration < 8; ++iteration) {
      long double y = x;
      long double derivative = 1;
      for (int i = n; i >= 1; --i) {
        y = inverse_branch(word_[i], y, derivative);
      }
      x -= (y - x) / (derivative - 1);
    }
    return x;
  }

  void process_word(int n) {
    bool all_same = true;
    for (int i = 2; i <= n; ++i) {
      if (word_[i] != word_[1]) {
        all_same = false;
        break;
      }
    }
    if (all_same) return;

    long double x = fixed_point(n);
    long double lo = x;
    long double hi = x;
    for (int i = 0; i < n; ++i) {
      if (x < lo) lo = x;
      if (x > hi) hi = x;
      x = x - 1 / x;
    }
    total_ += n * (hi - lo);
  }

  void generate(int n, int t, int p) {
    if (t > n) {
      if (p == n) process_word(n);
      return;
    }
    word_[t] = word_[t - p];
    generate(n, t + 1, p);
    for (int value = word_[t - p] + 1; value < 2; ++value) {
      word_[t] = value;
      generate(n, t + 1, t);
    }
  }
};

int main(int argc, char **argv) {
  int limit = TARGET;
  if (argc > 1) {
    limit = std::stoi(argv[1]);
  }
  PeriodicRanges ranges(limit);
  std::cout << std::fixed << std::setprecision(4) << static_cast<double>(ranges.sum()) << '\n';
  return 0;
}
