#!/usr/bin/env python3
import hashlib
import subprocess
import tempfile
from pathlib import Path


CPP_SOURCE = r"""
#include <cstdint>
#include <iostream>
#include <vector>

static unsigned long long odd_totient_sum(unsigned int n) {
    unsigned int m = (n - 1) / 2;
    std::vector<unsigned int> phi(m + 1);
    for (unsigned int i = 0; i <= m; ++i) {
        phi[i] = 2 * i + 1;
    }

    for (unsigned int i = 1; i <= m; ++i) {
        unsigned int p = 2 * i + 1;
        if (phi[i] != p) {
            continue;
        }
        for (unsigned long long j = i; j <= m; j += p) {
            phi[(std::size_t)j] -= phi[(std::size_t)j] / p;
        }
    }

    unsigned long long total = 0;
    for (unsigned int v : phi) {
        total += v;
    }
    return total;
}

int main(int argc, char **argv) {
    unsigned int n = 500000000U;
    if (argc > 1) {
        n = (unsigned int)std::stoul(argv[1]);
    }
    std::cout << odd_totient_sum(n) << '\n';
    return 0;
}
"""


def _binary():
    digest = hashlib.sha256(CPP_SOURCE.encode()).hexdigest()[:16]
    root = Path(tempfile.gettempdir()) / "eulerslop_build"
    root.mkdir(exist_ok=True)
    src = root / f"p512_{digest}.cpp"
    exe = root / f"p512_{digest}"
    if not exe.exists():
        src.write_text(CPP_SOURCE)
        subprocess.run(
            ["g++", "-O3", "-std=c++17", str(src), "-o", str(exe)],
            check=True,
        )
    return exe


def _run(n):
    result = subprocess.run(
        [str(_binary()), str(n)],
        check=True,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.strip())


def solve():
    # For odd n, sum_i phi(n^i) == phi(n) (mod n+1); for even n it is 0.
    # Therefore g(N) is the summatory totient over odd integers <= N.
    assert _run(100) == 2007
    return _run(500_000_000)


if __name__ == "__main__":
    print(solve())
