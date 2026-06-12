#!/usr/bin/env python3
import hashlib
import subprocess
import tempfile
from pathlib import Path


CPP_SOURCE = r"""
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <vector>

static int exponent_in_factorial(long long m, int p) {
    long long total = 0;
    while (m > 0) {
        m /= p;
        total += m;
    }
    return (int)total;
}

static int least_factorial_multiple(int p, int exponent) {
    long long low = 1;
    long long high = (long long)p * exponent;
    while (exponent_in_factorial(high, p) < exponent) high *= 2;

    while (low < high) {
        long long mid = (low + high) / 2;
        if (exponent_in_factorial(mid, p) >= exponent) {
            high = mid;
        } else {
            low = mid + 1;
        }
    }
    return (int)low;
}

static std::vector<int> primes_upto(int limit) {
    std::vector<unsigned char> composite((size_t)limit + 1, 0);
    std::vector<int> primes;
    for (int n = 2; n <= limit; ++n) {
        if (!composite[n]) {
            primes.push_back(n);
            if ((long long)n * n <= limit) {
                for (long long q = (long long)n * n; q <= limit; q += n) {
                    composite[(size_t)q] = 1;
                }
            }
        }
    }
    return primes;
}

static long long S(int limit) {
    std::vector<int> required((size_t)limit + 1, 0);
    auto primes = primes_upto(limit);

    for (int p : primes) {
        long long power = p;
        int exponent = 1;
        while (power <= limit) {
            int needed = least_factorial_multiple(p, exponent);
            for (int multiple = (int)power; multiple <= limit; multiple += (int)power) {
                if (required[multiple] < needed) required[multiple] = needed;
            }
            if (power > limit / p) break;
            power *= p;
            ++exponent;
        }
    }

    long long total = 0;
    for (int n = 2; n <= limit; ++n) total += required[n];
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
    src = root / f"p549_{digest}.cpp"
    exe = root / f"p549_{digest}"
    if not exe.exists():
        src.write_text(CPP_SOURCE)
        subprocess.run(
            ["g++", "-O3", "-march=native", "-std=c++17", str(src), "-o", str(exe)],
            check=True,
        )
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
    assert S(100) == 2012
    return S(100_000_000)


if __name__ == "__main__":
    print(solve())
