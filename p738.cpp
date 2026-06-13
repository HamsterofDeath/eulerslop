#include <cstdint>
#include <cstdlib>
#include <iostream>

static constexpr long long MOD = 1'000'000'007LL;

class Solver {
 public:
  Solver(long long limit, long long max_length)
      : limit_(limit), max_length_(max_length), answer_(max_length % MOD) {}

  int solve() {
    dfs(2, limit_, 0);
    return static_cast<int>(answer_);
  }

 private:
  long long limit_;
  long long max_length_;
  long long answer_;

  void add(long long value) {
    answer_ += value;
    answer_ %= MOD;
  }

  void dfs(long long minimum, long long limit, long long length) {
    if (limit < minimum || length >= max_length_) return;

    long long choices = limit - minimum + 1;
    long long padding_count = (max_length_ - length) % MOD;
    add((choices % MOD) * padding_count % MOD);

    for (long long factor = minimum; factor <= limit / factor; ++factor) {
      dfs(factor, limit / factor, length + 1);
    }
  }
};

int main(int argc, char** argv) {
  long long limit = 10'000'000'000LL;
  long long max_length = 10'000'000'000LL;
  if (argc > 1) limit = std::atoll(argv[1]);
  if (argc > 2) max_length = std::atoll(argv[2]);
  std::cout << Solver(limit, max_length).solve() << '\n';
  return 0;
}
