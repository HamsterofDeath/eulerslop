#!/usr/bin/env python3

import subprocess
import tempfile
from pathlib import Path


SOURCE = r"""
#include <bits/stdc++.h>
using namespace std;

static const int MOD = 1000000123;

long long mod_pow(long long base, long long exp) {
    long long result = 1;
    while (exp) {
        if (exp & 1) result = result * base % MOD;
        base = base * base % MOD;
        exp >>= 1;
    }
    return result;
}

struct Solver {
    int n;
    vector<int> factorial;
    vector<int> inv_factorial;
    vector<int> inv_factorial_power;
    int factorial_power;

    Solver(int n_, int rows) : n(n_), factorial(n + 1), inv_factorial(n + 1), inv_factorial_power(n + 1) {
        factorial[0] = 1;
        for (int i = 1; i <= n; ++i) factorial[i] = (long long)factorial[i - 1] * i % MOD;

        inv_factorial[n] = mod_pow(factorial[n], MOD - 2);
        for (int i = n; i >= 1; --i) inv_factorial[i - 1] = (long long)inv_factorial[i] * i % MOD;

        factorial_power = mod_pow(factorial[n], rows);
        for (int i = 0; i <= n; ++i) inv_factorial_power[i] = mod_pow(inv_factorial[i], rows);
    }

    int p_value(int k) const {
        int multiple_count = (n - 1) / k;
        vector<int> dp(multiple_count + 1);
        dp[0] = 1;

        for (int end = 1; end <= multiple_count; ++end) {
            long long total = 0;
            for (int length = 1; length <= end; ++length) {
                long long term = (long long)dp[end - length] * inv_factorial_power[length * k] % MOD;
                if ((length - 1) & 1) total -= term;
                else total += term;
                if (total > (long long)MOD * MOD || total < -(long long)MOD * MOD) total %= MOD;
            }
            dp[end] = (total % MOD + MOD) % MOD;
        }

        long long total = 0;
        for (int cut = 0; cut <= multiple_count; ++cut) {
            long long term = (long long)dp[cut] * inv_factorial_power[n - cut * k] % MOD;
            if ((multiple_count - cut) & 1) total -= term;
            else total += term;
            if (total > (long long)MOD * MOD || total < -(long long)MOD * MOD) total %= MOD;
        }
        total = (total % MOD + MOD) % MOD;
        return total * factorial_power % MOD;
    }

    int q_value() const {
        long long total = 0;
        for (int k = 1; k <= n; ++k) {
            total += p_value(k);
            total %= MOD;
        }
        return total;
    }
};

int main() {
    if (Solver(3, 2).p_value(1) != 19) return 1;
    if (Solver(6, 4).p_value(2) != 65508751) return 2;
    if (Solver(30, 5).p_value(7) != 161858102) return 3;
    if (Solver(5, 5).q_value() != 21879393751LL % MOD) return 4;
    if (Solver(50, 50).q_value() != 819573537) return 5;
    cout << Solver(50000, 50000).q_value() << '\n';
    return 0;
}
"""


def solve():
    with tempfile.TemporaryDirectory(prefix="p559_") as tmp:
        tmp_path = Path(tmp)
        cpp = tmp_path / "p559.cpp"
        exe = tmp_path / "p559"
        cpp.write_text(SOURCE)
        subprocess.run(
            ["g++", "-O3", "-std=c++17", str(cpp), "-o", str(exe)],
            check=True,
        )
        result = subprocess.run(
            [str(exe)],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        )
    return result.stdout.strip()


if __name__ == "__main__":
    print(solve())
