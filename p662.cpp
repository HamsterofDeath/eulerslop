#include <algorithm>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>

namespace {

constexpr std::uint32_t MOD = 1'000'000'007U;

struct Step {
    int x;
    int y;
    int offset;
};

int isqrt_ll(long long n) {
    long long r = static_cast<long long>(std::sqrt(static_cast<long double>(n)));
    while ((r + 1) * (r + 1) <= n) {
        ++r;
    }
    while (r * r > n) {
        --r;
    }
    return static_cast<int>(r);
}

std::vector<Step> fibonacci_steps(int width, int height, int columns) {
    const int max_distance = isqrt_ll(1LL * width * width + 1LL * height * height);
    std::vector<int> fibs{1, 2};
    while (fibs.back() < max_distance) {
        fibs.push_back(fibs[fibs.size() - 1] + fibs[fibs.size() - 2]);
    }

    std::vector<Step> steps;
    for (int f : fibs) {
        if (f > max_distance) {
            continue;
        }
        const long long ff = 1LL * f * f;
        const int xmax = std::min(width, f);
        for (int x = 0; x <= xmax; ++x) {
            const long long y2 = ff - 1LL * x * x;
            const int y = isqrt_ll(y2);
            if (1LL * y * y == y2 && y <= height) {
                steps.push_back({x, y, x * columns + y});
            }
        }
    }

    std::sort(steps.begin(), steps.end(), [](const Step& a, const Step& b) {
        if (a.y != b.y) {
            return a.y < b.y;
        }
        return a.x < b.x;
    });
    steps.erase(std::unique(steps.begin(), steps.end(), [](const Step& a, const Step& b) {
                    return a.x == b.x && a.y == b.y;
                }),
                steps.end());
    return steps;
}

std::uint32_t count_paths(int width, int height) {
    const int columns = height + 1;
    const std::vector<Step> steps = fibonacci_steps(width, height, columns);
    std::vector<std::uint32_t> dp(static_cast<std::size_t>(width + 1) * columns, 0);
    std::vector<Step> active;
    active.reserve(steps.size());

    dp[0] = 1;
    for (int x = 0; x <= width; ++x) {
        active.clear();
        for (const Step& step : steps) {
            if (step.x <= x) {
                active.push_back(step);
            }
        }

        const int row = x * columns;
        for (int y = 0; y <= height; ++y) {
            if (x == 0 && y == 0) {
                continue;
            }

            const int index = row + y;
            std::uint32_t total = 0;
            for (const Step& step : active) {
                if (step.y > y) {
                    break;
                }
                total += dp[index - step.offset];
                if (total >= MOD) {
                    total -= MOD;
                }
            }
            dp[index] = total;
        }
    }

    return dp[static_cast<std::size_t>(width) * columns + height];
}

}  // namespace

int main(int argc, char** argv) {
    int width = 10'000;
    int height = 10'000;
    if (argc >= 3) {
        width = std::atoi(argv[1]);
        height = std::atoi(argv[2]);
    }
    std::cout << count_paths(width, height) << '\n';
    return 0;
}
