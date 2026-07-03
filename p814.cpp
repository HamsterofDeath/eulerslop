// Project Euler 814: each person selects one incident edge of a Mobius ladder.
// A screaming pair is a bidirected edge; count assignments with exactly n such
// edges using a 4-state transfer over the two vertices in each column.
#include <array>
#include <cstdint>
#include <cstdio>
#include <vector>

using namespace std;

static const int MOD = 998244353;

static int s_value(int n) {
    int columns = 2 * n;
    int answer = 0;

    for (int start = 0; start < 4; ++start) {
        vector<array<int, 4>> dp(n + 1), next(n + 1);
        dp[0][start] = 1;

        for (int col = 0; col < columns; ++col) {
            for (auto& row : next) row = {0, 0, 0, 0};
            for (int k = 0; k <= n; ++k) {
                for (int state = 0; state < 4; ++state) {
                    int ways = dp[k][state];
                    if (!ways) continue;
                    int prev_top = state & 1;
                    int prev_bottom = (state >> 1) & 1;
                    for (int top = 0; top < 3; ++top) {
                        for (int bottom = 0; bottom < 3; ++bottom) {
                            int add = 0;
                            if (prev_top && top == 0) ++add;
                            if (prev_bottom && bottom == 0) ++add;
                            if (top == 2 && bottom == 2) ++add;
                            if (k + add > n) continue;
                            int ns = (top == 1) | ((bottom == 1) << 1);
                            int& slot = next[k + add][ns];
                            slot += ways;
                            if (slot >= MOD) slot -= MOD;
                        }
                    }
                }
            }
            dp.swap(next);
        }

        for (int out = 0; out < 4; ++out) {
            int swapped = ((out & 1) << 1) | (out >> 1);
            if (swapped == start) {
                answer += dp[n][out];
                if (answer >= MOD) answer -= MOD;
            }
        }
    }
    return answer;
}

int main() {
    if (s_value(1) != 48 || s_value(10) != 420121075) {
        fprintf(stderr, "self-test failed\n");
        return 1;
    }
    printf("%d\n", s_value(1000));
    return 0;
}
