#!/usr/bin/env python3
import hashlib
import subprocess
import tempfile
from pathlib import Path


CPP_SOURCE = r"""
#include <cmath>
#include <cstdint>
#include <iostream>
#include <vector>

static long long isqrt_floor(long long n) {
    long long r = std::sqrt((long double)n);
    while ((__int128)(r + 1) * (r + 1) <= n) ++r;
    while ((__int128)r * r > n) --r;
    return r;
}

static long long hilbert_count_below(long long limit) {
    if (limit <= 1) return 0;

    const long long root = isqrt_floor(limit - 1);
    const int odd_count = (int)(root / 2 + 1);

    std::vector<unsigned char> composite(odd_count, 0);
    for (long long p = 3; p * p <= root; p += 2) {
        if (composite[(size_t)(p / 2)]) continue;
        for (long long multiple = p * p; multiple <= root; multiple += 2 * p) {
            composite[(size_t)(multiple / 2)] = 1;
        }
    }

    std::vector<int> accumulated(odd_count, 0);
    long long total = 0;

    for (long long d = 1; d <= root; d += 2) {
        const size_t index = (size_t)(d / 2);

        // Let t be the odd square root of the square part of a Hilbert
        // number.  It is not enough to use Hilbert d only: for instance
        // lcm(9, 21) = 63.  The ordinary divisor transform below gives
        // coefficients lambda(d) for "t has no Hilbert divisor > 1".
        const bool no_hilbert_divisor =
            d == 1 || (d % 4 == 3 && !composite[index]);
        const int lambda = (no_hilbert_divisor ? 1 : 0) - accumulated[index];

        if (lambda != 0) {
            for (long long multiple = 3 * d; multiple <= root; multiple += 2 * d) {
                accumulated[(size_t)(multiple / 2)] += lambda;
            }
        }

        const long long quotient_limit = (limit - 1) / (d * d);
        const long long hilbert_quotients = (quotient_limit + 3) / 4;
        total += (long long)lambda * hilbert_quotients;
    }

    return total;
}

int main(int argc, char** argv) {
    long long limit = argc > 1 ? std::stoll(argv[1]) : 10000000000000000LL;
    std::cout << hilbert_count_below(limit) << '\n';
    return 0;
}
"""


def _binary():
    digest = hashlib.sha256(CPP_SOURCE.encode()).hexdigest()[:16]
    root = Path(tempfile.gettempdir()) / "eulerslop_build"
    root.mkdir(exist_ok=True)
    src = root / f"p580_{digest}.cpp"
    exe = root / f"p580_{digest}"
    if not exe.exists():
        src.write_text(CPP_SOURCE)
        subprocess.run(
            ["g++", "-O3", "-march=native", "-std=c++17", str(src), "-o", str(exe)],
            check=True,
        )
    return exe


def hilbert_count_below(limit):
    result = subprocess.run(
        [str(_binary()), str(limit)],
        check=True,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.strip())


def solve():
    assert hilbert_count_below(10**7) == 2327192
    return hilbert_count_below(10**16)


if __name__ == "__main__":
    print(solve())
