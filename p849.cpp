// Project Euler 849: generalized Landau inequalities for score sequences.
// Each pair contributes four total points, so sorted sequences s are feasible
// iff sum s = 4*C(n,2) and every k-prefix has sum at least 4*C(k,2).
#include <cstdint>
#include <cstdio>
#include <vector>

using namespace std;

static const int MOD = 1000000007;

static int f_value(int n) {
    int max_score = 4 * (n - 1);
    int total = 2 * n * (n - 1);
    vector<vector<int>> prev(max_score + 1, vector<int>(total + 1));
    prev[0][0] = 1;

    for (int len = 1; len <= n; ++len) {
        vector<vector<int>> next(max_score + 1, vector<int>(total + 1));
        vector<int> prefix(total + 1);
        int lower = 2 * len * (len - 1);
        for (int score = 0; score <= max_score; ++score) {
            for (int sum = 0; sum <= total; ++sum) {
                prefix[sum] += prev[score][sum];
                if (prefix[sum] >= MOD) prefix[sum] -= MOD;
            }
            for (int sum = 0; sum + score <= total; ++sum) {
                if (sum + score >= lower) {
                    next[score][sum + score] += prefix[sum];
                    if (next[score][sum + score] >= MOD)
                        next[score][sum + score] -= MOD;
                }
            }
        }
        prev.swap(next);
    }

    int answer = 0;
    for (int score = 0; score <= max_score; ++score) {
        answer += prev[score][total];
        if (answer >= MOD) answer -= MOD;
    }
    return answer;
}

int main() {
    if (f_value(2) != 3 || f_value(7) != 32923) {
        fprintf(stderr, "self-test failed\n");
        return 1;
    }
    printf("%d\n", f_value(100));
    return 0;
}
