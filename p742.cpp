#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <vector>

static constexpr long long INF = (1LL << 61);

struct Direction {
  int x;
  int y;
};

static long long solve(int vertices, int bound) {
  if (vertices == 4) return 1;
  const int selected = (vertices - 4) / 4;

  std::vector<Direction> directions;
  for (int x = 1; x <= bound; ++x) {
    for (int y = 1; y <= bound; ++y) {
      if (std::gcd(x, y) == 1) directions.push_back({x, y});
    }
  }
  std::sort(directions.begin(), directions.end(),
            [](const Direction& a, const Direction& b) {
              return 1LL * a.y * b.x < 1LL * b.y * a.x;
            });

  const int max_sum_x = bound * selected;
  std::vector<std::vector<long long>> dp(
      selected + 1, std::vector<long long>(max_sum_x + 1, INF));
  dp[0][0] = 1;  // Unit square from the horizontal and vertical edge orbits.

  for (const Direction& v : directions) {
    const long long linear = 2LL * (v.x + v.y + v.x * v.y);
    for (int used = selected - 1; used >= 0; --used) {
      const auto& src = dp[used];
      auto& dst = dp[used + 1];
      for (int sum_x = 0; sum_x + v.x <= max_sum_x; ++sum_x) {
        if (src[sum_x] == INF) continue;
        // Directions are processed in slope order, so every earlier selected
        // direction (a,b) contributes 4*a*v.y to the area.
        const long long candidate = src[sum_x] + linear + 4LL * v.y * sum_x;
        if (candidate < dst[sum_x + v.x]) dst[sum_x + v.x] = candidate;
      }
    }
  }

  return *std::min_element(dp[selected].begin(), dp[selected].end());
}

int main(int argc, char** argv) {
  int vertices = 1000;
  if (argc > 1) vertices = std::atoi(argv[1]);
  // The optimum for N=1000 is already stable by bound=60; bound=80 leaves
  // margin while keeping the DP small.  Smaller samples need only bound=10.
  const int bound = vertices <= 100 ? 10 : 80;
  std::cout << solve(vertices, bound) << '\n';
  return 0;
}
