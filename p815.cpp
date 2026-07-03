// Project Euler 815: DP over counts of values seen 0,1,2,3 times.  For each
// threshold L compute the probability that the active pile count never exceeds
// L, then sum tail probabilities to get E(max).
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <iomanip>
#include <iostream>
#include <unordered_map>

using namespace std;

static inline uint32_t pack(int n0, int n1, int n2, int n3) {
    return (uint32_t)n0 | ((uint32_t)n1 << 6) | ((uint32_t)n2 << 12) |
           ((uint32_t)n3 << 18);
}

static inline void unpack(uint32_t key, int& n0, int& n1, int& n2, int& n3) {
    n0 = key & 63;
    n1 = (key >> 6) & 63;
    n2 = (key >> 12) & 63;
    n3 = (key >> 18) & 63;
}

static long double probability_bounded(int n, int limit) {
    unordered_map<uint32_t, long double> current, next;
    current.reserve(200000);
    next.reserve(200000);
    current[pack(n, 0, 0, 0)] = 1.0L;

    for (int step = 0; step < 4 * n; ++step) {
        int remaining = 4 * n - step;
        next.clear();
        for (const auto& item : current) {
            int n0, n1, n2, n3;
            unpack(item.first, n0, n1, n2, n3);
            long double prob = item.second;

            if (n0) {
                int active = (n1 + 1) + n2 + n3;
                if (active <= limit) {
                    next[pack(n0 - 1, n1 + 1, n2, n3)] +=
                        prob * (4.0L * n0 / remaining);
                }
            }
            if (n1) {
                next[pack(n0, n1 - 1, n2 + 1, n3)] +=
                    prob * (3.0L * n1 / remaining);
            }
            if (n2) {
                next[pack(n0, n1, n2 - 1, n3 + 1)] +=
                    prob * (2.0L * n2 / remaining);
            }
            if (n3) {
                next[pack(n0, n1, n2, n3 - 1)] += prob * (1.0L * n3 / remaining);
            }
        }
        current.swap(next);
    }
    auto it = current.find(pack(0, 0, 0, 0));
    return it == current.end() ? 0.0L : it->second;
}

static long double expected_max(int n) {
    long double result = 0;
    for (int limit = 0; limit < n; ++limit) {
        result += 1.0L - probability_bounded(n, limit);
    }
    return result;
}

int main() {
    long double sample = expected_max(2);
    if (fabsl(sample - 1.97142857L) > 5e-9L) {
        fprintf(stderr, "self-test failed: %.12Lf\n", sample);
        return 1;
    }
    cout << fixed << setprecision(8) << (double)expected_max(60) << "\n";
    return 0;
}
