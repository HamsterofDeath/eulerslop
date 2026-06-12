#!/usr/bin/env python3
import hashlib
import subprocess
import tempfile
from pathlib import Path


CPP_SOURCE = r"""
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <string>

static long long S(int limit) {
    long long total = 0;
    for (long long a = 1; a <= limit; ++a) {
        for (long long b = 1; b <= limit - a; ++b) {
            long long cmax = std::min<long long>(limit - a - b, (a * a - 1) / b);
            if (cmax < b) continue;

            for (long long c = b; c <= cmax; ++c) {
                long long denominator = a * a - b * c;
                long long numerator = b * c * (2 * a + b + c);
                if (numerator % denominator != 0) continue;

                long long d = numerator / denominator;
                long long area = a + b + c + d;
                if (area <= limit) total += area;
            }
        }
    }
    return total;
}

int main(int argc, char** argv) {
    int limit = argc > 1 ? std::stoi(argv[1]) : 10000;
    std::cout << S(limit) << '\n';
    return 0;
}
"""


def _binary():
    digest = hashlib.sha256(CPP_SOURCE.encode()).hexdigest()[:16]
    root = Path(tempfile.gettempdir()) / "eulerslop_build"
    root.mkdir(exist_ok=True)
    src = root / f"p557_{digest}.cpp"
    exe = root / f"p557_{digest}"
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
    # If the two cevians cut areas (a,b,c,d), the geometry gives
    # d(a^2-bc)=bc(2a+b+c), with b <= c and a^2 > bc.
    assert S(20) == 259
    return S(10_000)


if __name__ == "__main__":
    print(solve())
