#include <cstdint>
#include <iostream>
#include <string>
#include <vector>

static constexpr int MOD = 1'000'000'007;
static constexpr int TARGET = 100'000'000;

static int solve_for(int k) {
  std::vector<char> is_composite(k + 1, 0);
  long long result = 2;
  for (int p = 2; p <= k; ++p) {
    if (is_composite[p]) continue;
    for (long long multiple = 1LL * p * p; multiple <= k; multiple += p) {
      is_composite[static_cast<std::size_t>(multiple)] = 1;
    }
    long long power = p;
    while (power * p <= k) power *= p;
    result = result * (power % MOD) % MOD;
  }
  return static_cast<int>(result);
}

int main(int argc, char **argv) {
  int k = TARGET;
  if (argc > 1) {
    k = std::stoi(argv[1]);
  }
  std::cout << solve_for(k) << '\n';
  return 0;
}
