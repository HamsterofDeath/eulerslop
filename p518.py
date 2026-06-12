#!/usr/bin/env python3
import hashlib
import subprocess
import tempfile
from pathlib import Path


CPP_SOURCE = r"""
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <vector>

static std::vector<unsigned char> prime_sieve(int n) {
    std::vector<unsigned char> is_prime((std::size_t)n + 1, 1);
    if (n >= 0) is_prime[0] = 0;
    if (n >= 1) is_prime[1] = 0;
    for (int p = 2; (long long)p * p <= n; ++p) {
        if (is_prime[p]) {
            for (long long q = (long long)p * p; q <= n; q += p) {
                is_prime[(std::size_t)q] = 0;
            }
        }
    }
    return is_prime;
}

static long long S(int limit) {
    auto is_prime = prime_sieve(limit);
    long long total = 0;
    for (int s = 2; (long long)s * s <= limit; ++s) {
        for (int r = 1; r < s; ++r) {
            if (std::gcd(r, s) != 1) continue;
            int dmax = limit / (s * s);
            for (int d = 1; d <= dmax; ++d) {
                int a = d * r * r - 1;
                int b = d * r * s - 1;
                int c = d * s * s - 1;
                if (a >= 2 && c < limit && is_prime[a] && is_prime[b] && is_prime[c]) {
                    total += (long long)a + b + c;
                }
            }
        }
    }
    return total;
}

int main(int argc, char** argv) {
    int limit = argc > 1 ? std::stoi(argv[1]) : 100000000;
    std::cout << S(limit) << '\n';
    return 0;
}
"""


def _binary():
    digest = hashlib.sha256(CPP_SOURCE.encode()).hexdigest()[:16]
    root = Path(tempfile.gettempdir()) / "eulerslop_build"
    root.mkdir(exist_ok=True)
    src = root / f"p518_{digest}.cpp"
    exe = root / f"p518_{digest}"
    if not exe.exists():
        src.write_text(CPP_SOURCE)
        subprocess.run(["g++", "-O3", "-std=c++17", str(src), "-o", str(exe)], check=True)
    return exe


def S(limit):
    result = subprocess.run(
        [str(_binary()), str(limit)],
        check=True,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.strip())


def solve():
    assert S(100) == 1035
    return S(100_000_000)


if __name__ == "__main__":
    print(solve())
