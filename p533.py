#!/usr/bin/env python3

import subprocess
import tempfile
from pathlib import Path


SOURCE = r"""
#include <bits/stdc++.h>
using namespace std;

static const uint64_t MOD = 1000000000ULL;

uint64_t solve_limit(int limit) {
    vector<int> spf(limit + 1);
    vector<int> primes;
    for (int i = 2; i <= limit; ++i) {
        if (spf[i] == 0) {
            spf[i] = i;
            primes.push_back(i);
        }
        for (int p : primes) {
            long long v = 1LL * p * i;
            if (v > limit) break;
            spf[v] = p;
            if (p == spf[i]) break;
        }
    }

    vector<double> logarithm(limit, 0.0);
    vector<uint32_t> residue(limit, 1);

    auto multiply_multiples = [&](int component, int prime) {
        double log_prime = log((double)prime);
        for (int m = component; m < limit; m += component) {
            logarithm[m] += log_prime;
            residue[m] = (uint64_t)residue[m] * prime % MOD;
        }
    };

    multiply_multiples(1, 2);
    if (2 < limit) {
        multiply_multiples(2, 2);
        multiply_multiples(2, 2);
    }
    for (long long component = 4; component < limit; component *= 2) {
        multiply_multiples((int)component, 2);
    }

    for (int p : primes) {
        if (p == 2) continue;
        long long component = p - 1;
        while (component < limit) {
            multiply_multiples((int)component, p);
            if (component > (long long)(limit - 1) / p) break;
            component *= p;
        }
    }

    int best = 1;
    for (int m = 2; m < limit; ++m) {
        if (logarithm[m] > logarithm[best]) best = m;
    }
    return (residue[best] + 1) % MOD;
}

int main(int argc, char** argv) {
    for (int i = 1; i < argc; ++i) {
        cout << solve_limit(atoi(argv[i])) << '\n';
    }
    return 0;
}
"""


def run_limits(*limits):
    with tempfile.TemporaryDirectory(prefix="p533_") as tmp:
        tmp_path = Path(tmp)
        cpp = tmp_path / "p533.cpp"
        exe = tmp_path / "p533"
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
    sample_6, sample_100, answer = run_limits(6, 100, 20_000_000)
    assert sample_6 == "241"
    assert sample_100 == "174525281"
    return answer


if __name__ == "__main__":
    print(solve())
