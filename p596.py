#!/usr/bin/env python3
import hashlib
import subprocess
import tempfile
from pathlib import Path


CPP_SOURCE = r"""
#include <cstdint>
#include <iostream>

static const unsigned long long MOD = 1000000007ULL;
static const unsigned long long INV2 = 500000004ULL;

static unsigned long long range_sum_mod(unsigned long long lo, unsigned long long hi) {
    unsigned long long a = (lo + hi) % MOD;
    unsigned long long b = (hi - lo + 1) % MOD;
    return (unsigned long long)((__uint128_t)a * b % MOD * INV2 % MOD);
}

static unsigned long long A(unsigned long long n) {
    unsigned long long total = 0;
    unsigned long long i = 1;
    while (i <= n) {
        unsigned long long q = n / i;
        unsigned long long j = n / q;
        unsigned long long add = (unsigned long long)((__uint128_t)(q % MOD) * range_sum_mod(i, j) % MOD);
        total += add;
        if (total >= MOD) total -= MOD;
        i = j + 1;
    }
    return total;
}

static unsigned long long T(unsigned long long r) {
    unsigned long long n = r * r;
    unsigned long long all = A(n);
    unsigned long long excluded = 4ULL * A(n / 4ULL) % MOD;
    unsigned long long inner = (all + MOD - excluded) % MOD;
    return (1ULL + 8ULL * inner) % MOD;
}

int main(int argc, char **argv) {
    unsigned long long r = 100000000ULL;
    if (argc > 1) r = std::stoull(argv[1]);
    std::cout << T(r) << '\n';
    return 0;
}
"""


def _binary():
    digest = hashlib.sha256(CPP_SOURCE.encode()).hexdigest()[:16]
    root = Path(tempfile.gettempdir()) / "eulerslop_build"
    root.mkdir(exist_ok=True)
    src = root / f"p596_{digest}.cpp"
    exe = root / f"p596_{digest}"
    if not exe.exists():
        src.write_text(CPP_SOURCE)
        subprocess.run(["g++", "-O3", "-std=c++17", str(src), "-o", str(exe)], check=True)
    return exe


def T(r):
    result = subprocess.run(
        [str(_binary()), str(r)],
        check=True,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.strip())


def solve():
    assert T(2) == 89
    assert T(5) == 3121
    assert T(100) == 493490641
    assert T(10 ** 4) == 49348022079085897 % 1_000_000_007
    return T(10 ** 8)


if __name__ == "__main__":
    print(solve())
