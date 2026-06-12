#!/usr/bin/env python3
import hashlib
import subprocess
import tempfile
from pathlib import Path


CPP_SOURCE = r"""
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <utility>
#include <vector>

static int required_side(int a, int b) {
    int x[6] = {
        0,
        a,
        a - b,
        -2 * b,
        -a - 2 * b,
        -a - b
    };
    int y[6] = {
        0,
        b,
        a + 2 * b,
        2 * a + 2 * b,
        2 * a + b,
        a
    };
    int min_x = x[0], min_y = y[0], max_sum = x[0] + y[0];
    for (int i = 1; i < 6; ++i) {
        min_x = std::min(min_x, x[i]);
        min_y = std::min(min_y, y[i]);
        max_sum = std::max(max_sum, x[i] + y[i]);
    }
    return max_sum - min_x - min_y;
}

static long long choose3(long long n) {
    if (n < 3) return 0;
    return (long long)((__int128)n * (n - 1) * (n - 2) / 6);
}

static long long H(int n) {
    __int128 total = 0;
    for (int a = -n; a <= n; ++a) {
        for (int b = -n; b <= n; ++b) {
            if (a == 0 && b == 0) continue;
            int req = required_side(a, b);
            if (req <= n) {
                long long t = n - req + 1;
                total += (__int128)t * (t + 1) / 2;
            }
        }
    }
    return (long long)(total / 6);
}

static long long sum_H(int limit) {
    __int128 total = 0;
    for (int a = -limit; a <= limit; ++a) {
        for (int b = -limit; b <= limit; ++b) {
            if (a == 0 && b == 0) continue;
            int req = required_side(a, b);
            if (req <= limit) {
                total += choose3((long long)limit - req + 3);
            }
        }
    }
    return (long long)(total / 6);
}

int main(int argc, char** argv) {
    if (argc == 3 && std::string(argv[1]) == "H") {
        std::cout << H(std::stoi(argv[2])) << '\n';
    } else {
        int limit = argc > 1 ? std::stoi(argv[1]) : 12345;
        std::cout << sum_H(limit) << '\n';
    }
    return 0;
}
"""


def _binary():
    digest = hashlib.sha256(CPP_SOURCE.encode()).hexdigest()[:16]
    root = Path(tempfile.gettempdir()) / "eulerslop_build"
    root.mkdir(exist_ok=True)
    src = root / f"p577_{digest}.cpp"
    exe = root / f"p577_{digest}"
    if not exe.exists():
        src.write_text(CPP_SOURCE)
        subprocess.run(["g++", "-O3", "-std=c++17", str(src), "-o", str(exe)], check=True)
    return exe


def _run(*args):
    result = subprocess.run(
        [str(_binary()), *map(str, args)],
        check=True,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.strip())


def H(n):
    return _run("H", n)


def solve():
    assert H(3) == 1
    assert H(6) == 12
    assert H(20) == 966
    return _run(12345)


if __name__ == "__main__":
    print(solve())
