#!/usr/bin/env python3
import hashlib
import subprocess
import tempfile
from pathlib import Path


CPP_SOURCE = r"""
#include <iomanip>
#include <iostream>

static long double S(unsigned int limit) {
    long double total = 0.0L;
    long double ja_prev = 0.0L;
    long double pow2_inv = 1.0L;
    long double reciprocal_binomial_sum = 1.0L; // R_0

    for (unsigned int n = 1; n <= limit; ++n) {
        pow2_inv *= 0.5L;
        long double ja = 0.5L * ja_prev + (1.0L - pow2_inv) / (long double)n;
        long double jb = reciprocal_binomial_sum / (long double)n;
        total += ja + jb;

        reciprocal_binomial_sum =
            1.0L + ((long double)n + 1.0L) * reciprocal_binomial_sum / (2.0L * (long double)n);
        ja_prev = ja;
    }
    return total;
}

int main(int argc, char** argv) {
    unsigned int limit = 123456789U;
    if (argc > 1) limit = (unsigned int)std::stoul(argv[1]);
    std::cout << std::fixed << std::setprecision(8) << (double)S(limit) << '\n';
    return 0;
}
"""


def _binary():
    digest = hashlib.sha256(CPP_SOURCE.encode()).hexdigest()[:16]
    root = Path(tempfile.gettempdir()) / "eulerslop_build"
    root.mkdir(exist_ok=True)
    src = root / f"p567_{digest}.cpp"
    exe = root / f"p567_{digest}"
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
    return result.stdout.strip()


def solve():
    assert S(6) == "7.58932292"
    return S(123456789)


if __name__ == "__main__":
    print(solve())
