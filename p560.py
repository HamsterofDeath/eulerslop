#!/usr/bin/env python3
import hashlib
import subprocess
import tempfile
from pathlib import Path


CPP_SOURCE = r"""
#include <cstdint>
#include <iostream>
#include <vector>

static constexpr int MOD = 1000000007;

static long long mod_pow(long long base, long long exponent) {
    long long result = 1;
    while (exponent) {
        if (exponent & 1) result = result * base % MOD;
        base = base * base % MOD;
        exponent >>= 1;
    }
    return result;
}

static std::vector<int> grundy_counts(int n) {
    int limit = n - 1;
    std::vector<int> spf(limit + 1), primes, prime_index(limit + 1);
    for (int i = 2; i <= limit; ++i) {
        if (spf[i] == 0) {
            spf[i] = i;
            primes.push_back(i);
            prime_index[i] = (int)primes.size();
        }
        for (int p : primes) {
            long long x = (long long)p * i;
            if (x > limit || p > spf[i]) break;
            spf[(int)x] = p;
        }
    }

    int size = 1;
    while (size <= (int)primes.size() + 1) size <<= 1;
    std::vector<int> counts(size);
    for (int x = 1; x <= limit; ++x) {
        int grundy;
        if (x % 2 == 0) {
            grundy = 0;
        } else if (x == 1) {
            grundy = 1;
        } else {
            grundy = prime_index[spf[x]];
        }
        if (++counts[grundy] == MOD) counts[grundy] = 0;
    }
    return counts;
}

static void fwht(std::vector<int>& a, bool inverse) {
    int n = (int)a.size();
    for (int len = 1; 2 * len <= n; len <<= 1) {
        for (int start = 0; start < n; start += 2 * len) {
            for (int j = 0; j < len; ++j) {
                int u = a[start + j];
                int v = a[start + j + len];
                int x = u + v;
                if (x >= MOD) x -= MOD;
                int y = u - v;
                if (y < 0) y += MOD;
                a[start + j] = x;
                a[start + j + len] = y;
            }
        }
    }

    if (inverse) {
        long long inv_n = mod_pow(n, MOD - 2);
        for (int& x : a) x = x * inv_n % MOD;
    }
}

static int L(int n, long long k) {
    auto counts = grundy_counts(n);
    fwht(counts, false);
    for (int& x : counts) x = (int)mod_pow(x, k);
    fwht(counts, true);
    return counts[0];
}

int main(int argc, char** argv) {
    if (argc == 3) {
        std::cout << L(std::stoi(argv[1]), std::stoll(argv[2])) << '\n';
    } else {
        std::cout << L(10000000, 10000000) << '\n';
    }
    return 0;
}
"""


def _binary():
    digest = hashlib.sha256(CPP_SOURCE.encode()).hexdigest()[:16]
    root = Path(tempfile.gettempdir()) / "eulerslop_build"
    root.mkdir(exist_ok=True)
    src = root / f"p560_{digest}.cpp"
    exe = root / f"p560_{digest}"
    if not exe.exists():
        src.write_text(CPP_SOURCE)
        subprocess.run(
            ["g++", "-O3", "-march=native", "-std=c++17", str(src), "-o", str(exe)],
            check=True,
        )
    return exe


def L(n, k):
    result = subprocess.run(
        [str(_binary()), str(n), str(k)],
        check=True,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.strip())


def solve():
    assert L(5, 2) == 6
    assert L(10, 5) == 9_964
    assert L(10, 10) == 472_400_303
    assert L(1000, 1000) == 954_021_836

    result = subprocess.run(
        [str(_binary())],
        check=True,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.strip())


if __name__ == "__main__":
    print(solve())
