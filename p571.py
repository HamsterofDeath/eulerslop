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

static bool is_pandigital_in_base(unsigned long long value, int base) {
    unsigned mask = 0;
    unsigned full = (1u << base) - 1u;
    while (value > 0) {
        mask |= 1u << (value % base);
        value /= base;
    }
    return mask == full;
}

static bool is_super_pandigital(unsigned long long value, int max_base) {
    for (int base = max_base - 1; base >= 2; --base) {
        if (!is_pandigital_in_base(value, base)) return false;
    }
    return true;
}

static unsigned long long sum_smallest(int max_base, int wanted) {
    std::vector<int> digits;
    digits.push_back(1);
    digits.push_back(0);
    for (int d = 2; d < max_base; ++d) digits.push_back(d);

    unsigned long long total = 0;
    int found = 0;
    do {
        if (digits[0] == 0) continue;
        unsigned long long value = 0;
        for (int digit : digits) value = value * max_base + digit;

        if (is_super_pandigital(value, max_base)) {
            total += value;
            if (++found == wanted) break;
        }
    } while (std::next_permutation(digits.begin(), digits.end()));

    return total;
}

int main(int argc, char** argv) {
    int base = argc > 1 ? std::stoi(argv[1]) : 12;
    std::cout << sum_smallest(base, 10) << '\n';
    return 0;
}
"""


def _binary():
    digest = hashlib.sha256(CPP_SOURCE.encode()).hexdigest()[:16]
    root = Path(tempfile.gettempdir()) / "eulerslop_build"
    root.mkdir(exist_ok=True)
    src = root / f"p571_{digest}.cpp"
    exe = root / f"p571_{digest}"
    if not exe.exists():
        src.write_text(CPP_SOURCE)
        subprocess.run(
            ["g++", "-O3", "-march=native", "-std=c++17", str(src), "-o", str(exe)],
            check=True,
        )
    return exe


def super_sum(base):
    result = subprocess.run(
        [str(_binary()), str(base)],
        check=True,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.strip())


def solve():
    assert super_sum(10) == 20_319_792_309
    return super_sum(12)


if __name__ == "__main__":
    print(solve())
