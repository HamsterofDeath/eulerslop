// Project Euler 819: forward absorption is backward coalescence.  With k
// current lineages, the previous generation has j distinct parents with the
// occupancy distribution of k balls in n boxes.
#include <cmath>
#include <cstdio>
#include <iomanip>
#include <iostream>
#include <vector>

using namespace std;

static long double expected_steps(int n) {
    vector<long double> expected(n + 1, 0), prev(n + 1, 0), cur(n + 1, 0);
    prev[0] = 1;
    for (int k = 1; k <= n; ++k) {
        fill(cur.begin(), cur.end(), 0);
        for (int j = 1; j <= k; ++j) {
            cur[j] += prev[j] * ((long double)j / n);
            cur[j] += prev[j - 1] * ((long double)(n - j + 1) / n);
        }
        if (k >= 2) {
            long double lower = 0;
            for (int j = 1; j < k; ++j) lower += cur[j] * expected[j];
            expected[k] = (1 + lower) / (1 - cur[k]);
        }
        prev.swap(cur);
    }
    return expected[n];
}

int main() {
    if (fabsl(expected_steps(3) - 27.0L / 7.0L) > 1e-12L ||
        fabsl(expected_steps(5) - 468125.0L / 60701.0L) > 1e-12L) {
        fprintf(stderr, "self-test failed\n");
        return 1;
    }
    cout << fixed << setprecision(6) << (double)expected_steps(1000) << "\n";
    return 0;
}
