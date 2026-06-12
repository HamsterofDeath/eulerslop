#!/usr/bin/env python3

import subprocess
import tempfile
from math import comb, factorial
from pathlib import Path

MOD = 135707531


def f_small(n):
    zero_indegree = n * (n - 1) * (n - 2) ** (n - 1)
    special_cycles = 0
    for cycle_size in range(2, n + 1):
        outside = n - cycle_size
        outside_maps = 1 if outside == 0 else (outside - 1) ** outside
        special_cycles += comb(n, cycle_size) * factorial(cycle_size - 1) * outside_maps
    return zero_indegree + special_cycles - factorial(n - 1)


def f_mod(n):
    source = r"""
#include <bits/stdc++.h>
using namespace std;

static const long long MOD = 135707531LL;

long long mod_pow(long long base, long long exp) {
    long long result = 1;
    while (exp > 0) {
        if (exp & 1) result = result * base % MOD;
        base = base * base % MOD;
        exp >>= 1;
    }
    return result;
}

int main(int argc, char** argv) {
    int n = atoi(argv[1]);

    vector<int> inv(n + 1);
    inv[1] = 1;
    for (int i = 2; i <= n; ++i) {
        inv[i] = (long long)(MOD - MOD / i) * inv[MOD % i] % MOD;
    }

    long long fact = 1;
    for (int i = 2; i <= n; ++i) fact = fact * i % MOD;

    long long answer = (long long)n * (n - 1) % MOD * mod_pow(n - 2, n - 1) % MOD;
    long long inv_fact = 1;
    for (int j = 2; j <= n - 2; ++j) {
        inv_fact = inv_fact * inv[j] % MOD;
        long long term = fact * inv[n - j] % MOD * inv_fact % MOD;
        term = term * mod_pow(j - 1, j) % MOD;
        answer += term;
        if (answer >= MOD) answer -= MOD;
    }

    cout << answer % MOD << '\n';
    return 0;
}
"""
    with tempfile.TemporaryDirectory(prefix="p522_") as tmp:
        tmp_path = Path(tmp)
        cpp = tmp_path / "p522.cpp"
        exe = tmp_path / "p522"
        cpp.write_text(source)
        subprocess.run(
            ["g++", "-O3", "-std=c++17", str(cpp), "-o", str(exe)],
            check=True,
        )
        result = subprocess.run(
            [str(exe), str(n)],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        )
    return int(result.stdout)


def solve():
    assert f_small(3) == 6
    assert f_small(8) == 16276736
    assert f_mod(100) == 84326147
    return str(f_mod(12344321))


if __name__ == "__main__":
    print(solve())
