#include <iostream>
#include <string>
#include <vector>

static constexpr int VALUE_MOD = 10'000'019;
static constexpr int ANSWER_MOD = 1'000'000'007;
static constexpr int TARGET = 1'000'000;

class Fenwick {
 public:
  explicit Fenwick(int size) : tree_(size + 1, 0) {}

  void add(int index, long long value) {
    value %= ANSWER_MOD;
    for (int i = index; i < static_cast<int>(tree_.size()); i += i & -i) {
      int next = static_cast<int>(tree_[i] + value);
      if (next >= ANSWER_MOD) next -= ANSWER_MOD;
      tree_[i] = next;
    }
  }

  int sum(int index) const {
    long long result = 0;
    for (int i = index; i > 0; i -= i & -i) {
      result += tree_[i];
      if (result >= ANSWER_MOD) result -= ANSWER_MOD;
    }
    return static_cast<int>(result);
  }

 private:
  std::vector<int> tree_;
};

static int solve_for(int n) {
  std::vector<Fenwick> counts;
  std::vector<Fenwick> sums;
  counts.reserve(5);
  sums.reserve(5);
  for (int i = 0; i < 5; ++i) {
    counts.emplace_back(VALUE_MOD + 2);
    sums.emplace_back(VALUE_MOD + 2);
  }

  long long value = 1;
  for (int i = 1; i <= n; ++i) {
    value = value * 153 % VALUE_MOD;
    int x = static_cast<int>(value);
    int index = x + 1;
    int before = index - 1;

    for (int length = 4; length >= 2; --length) {
      int previous_count = counts[length - 1].sum(before);
      int previous_sum = sums[length - 1].sum(before);
      int new_sum = static_cast<int>((previous_sum + value * previous_count) % ANSWER_MOD);
      counts[length].add(index, previous_count);
      sums[length].add(index, new_sum);
    }

    counts[1].add(index, 1);
    sums[1].add(index, x);
  }

  return sums[4].sum(VALUE_MOD + 1);
}

int main(int argc, char **argv) {
  int n = TARGET;
  if (argc > 1) {
    n = std::stoi(argv[1]);
  }
  std::cout << solve_for(n) << '\n';
  return 0;
}
