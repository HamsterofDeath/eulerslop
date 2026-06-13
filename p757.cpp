#include <algorithm>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>

static constexpr unsigned long long TARGET = 100'000'000'000'000ULL;

static unsigned long long count_stealthy(unsigned long long limit) {
  std::vector<unsigned long long> values;
  values.reserve(80'000'000);

  for (unsigned long long x = 1;; ++x) {
    unsigned long long px = x * (x + 1);
    if ((__int128)px * px > limit) break;
    for (unsigned long long y = x;; ++y) {
      unsigned long long py = y * (y + 1);
      __int128 product = static_cast<__int128>(px) * py;
      if (product > limit) break;
      values.push_back(static_cast<unsigned long long>(product));
    }
  }

  std::sort(values.begin(), values.end());
  return std::unique(values.begin(), values.end()) - values.begin();
}

int main(int argc, char **argv) {
  unsigned long long limit = TARGET;
  if (argc > 1) {
    limit = std::stoull(argv[1]);
  }
  std::cout << count_stealthy(limit) << '\n';
  return 0;
}
