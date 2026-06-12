#!/usr/bin/env python3
import hashlib
import subprocess
import tempfile
from pathlib import Path


CPP_SOURCE = r"""
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>

static void generate_smooth(const std::vector<unsigned long long>& primes,
                            size_t index,
                            unsigned long long value,
                            unsigned long long limit,
                            std::vector<unsigned long long>& out) {
    if (index == primes.size()) {
        out.push_back(value);
        return;
    }

    const unsigned long long p = primes[index];
    while (value <= limit) {
        generate_smooth(primes, index + 1, value, limit, out);
        if (value > limit / p) break;
        value *= p;
    }
}

static unsigned long long sum_indices(const std::vector<unsigned long long>& primes,
                                      unsigned long long largest_consecutive_member) {
    std::vector<unsigned long long> smooth;
    generate_smooth(primes, 0, 1, largest_consecutive_member, smooth);
    std::sort(smooth.begin(), smooth.end());

    unsigned long long total = 0;
    for (size_t i = 1; i < smooth.size(); ++i) {
        if (smooth[i] == smooth[i - 1] + 1) {
            // T(n) = n(n+1)/2 is p-smooth exactly when both n and n+1
            // are p-smooth.  Add the lower member, which is the index n.
            total += smooth[i - 1];
        }
    }
    return total;
}

int main() {
    const std::vector<unsigned long long> primes5 = {2, 3, 5};
    const std::vector<unsigned long long> primes47 =
        {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47};

    assert(sum_indices(primes5, 81ULL) == 151ULL);

    // Størmer's theorem makes the search finite.  OEIS A117581 gives
    // 1109496723126 as the largest larger member of a consecutive
    // 47-smooth pair.
    std::cout << sum_indices(primes47, 1109496723126ULL) << '\n';
    return 0;
}
"""


def _binary():
    digest = hashlib.sha256(CPP_SOURCE.encode()).hexdigest()[:16]
    root = Path(tempfile.gettempdir()) / "eulerslop_build"
    root.mkdir(exist_ok=True)
    src = root / f"p581_{digest}.cpp"
    exe = root / f"p581_{digest}"
    if not exe.exists():
        src.write_text(CPP_SOURCE)
        subprocess.run(
            ["g++", "-O3", "-march=native", "-std=c++17", str(src), "-o", str(exe)],
            check=True,
        )
    return exe


def solve():
    result = subprocess.run(
        [str(_binary())],
        check=True,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.strip())


if __name__ == "__main__":
    print(solve())
