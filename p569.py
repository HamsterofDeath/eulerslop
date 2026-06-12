#!/usr/bin/env python3

import subprocess
import tempfile
from pathlib import Path


SOURCE = r"""
#include <bits/stdc++.h>
using namespace std;

using i64 = long long;
using i128 = __int128_t;

long long solve_limit(int limit_count) {
    int needed_primes = 2 * limit_count;
    int sieve_limit = 100;
    if (needed_primes >= 6) {
        double n = needed_primes;
        sieve_limit = (int)(n * (log(n) + log(log(n))) + 20);
    }

    vector<char> composite(sieve_limit + 1, false);
    vector<int> primes;
    primes.reserve(needed_primes);
    for (int i = 2; i <= sieve_limit && (int)primes.size() < needed_primes; ++i) {
        if (!composite[i]) {
            primes.push_back(i);
            if (1LL * i * i <= sieve_limit) {
                for (long long j = 1LL * i * i; j <= sieve_limit; j += i) {
                    composite[j] = true;
                }
            }
        }
    }
    if ((int)primes.size() < needed_primes) return -1;

    vector<i64> x(limit_count);
    vector<i64> y(limit_count);
    i64 current_x = 0;
    i64 current_y = 0;
    for (int k = 0; k < limit_count; ++k) {
        current_x += primes[2 * k];
        current_y += primes[2 * k];
        x[k] = current_x;
        y[k] = current_y;
        current_x += primes[2 * k + 1];
        current_y -= primes[2 * k + 1];
    }

    vector<vector<int>> visible_chain(limit_count);
    vector<int> seen(limit_count, -1);
    vector<int> stack;
    stack.reserve(1024);

    long long total = 0;
    for (int i = 1; i < limit_count; ++i) {
        stack.clear();
        stack.push_back(i - 1);

        bool has_best = false;
        i64 best_num = 0;
        i64 best_den = 1;

        vector<int>& chain = visible_chain[i];
        while (!stack.empty()) {
            int j = stack.back();
            stack.pop_back();
            if (seen[j] == i) continue;
            seen[j] = i;

            i64 num = y[i] - y[j];
            i64 den = x[i] - x[j];
            if (!has_best || (i128)num * best_den < (i128)best_num * den) {
                has_best = true;
                best_num = num;
                best_den = den;
                chain.push_back(j);

                const vector<int>& previous = visible_chain[j];
                for (auto it = previous.rbegin(); it != previous.rend(); ++it) {
                    stack.push_back(*it);
                }
            }
        }
        total += (int)chain.size();
    }

    return total;
}

int main(int argc, char** argv) {
    for (int i = 1; i < argc; ++i) {
        cout << solve_limit(atoi(argv[i])) << '\n';
    }
    return 0;
}
"""


def run_limits(*limits):
    with tempfile.TemporaryDirectory(prefix="p569_") as tmp:
        tmp_path = Path(tmp)
        cpp = tmp_path / "p569.cpp"
        exe = tmp_path / "p569"
        cpp.write_text(SOURCE)
        subprocess.run(
            ["g++", "-O3", "-std=c++17", str(cpp), "-o", str(exe)],
            check=True,
        )
        result = subprocess.run(
            [str(exe), *(str(limit) for limit in limits)],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        )
    return result.stdout.strip().splitlines()


def solve():
    sample, answer = run_limits(100, 2_500_000)
    assert sample == "227"
    return answer


if __name__ == "__main__":
    print(solve())
