#!/usr/bin/env python3
import hashlib
import subprocess
import tempfile
from pathlib import Path


CPP_SOURCE = r"""
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <vector>

struct Pair {
    double sum;
    uint32_t square_sum;
};

static uint64_t g(int n) {
    const double pi = std::acos(-1.0);
    int max_k = (int)std::ceil(n * std::log(pi + 1.0)) + 1;

    std::vector<double> f(max_k + 1);
    for (int k = 0; k <= max_k; ++k) {
        f[k] = std::expm1((double)k / n);
    }

    std::vector<Pair> pairs;
    pairs.reserve((uint64_t)(max_k + 1) * (max_k + 2) / 2);
    for (int a = 0; a <= max_k; ++a) {
        for (int b = a; b <= max_k; ++b) {
            pairs.push_back({f[a] + f[b], (uint32_t)(a * a + b * b)});
        }
    }

    std::sort(pairs.begin(), pairs.end(), [](const Pair& left, const Pair& right) {
        return left.sum < right.sum;
    });

    double best_error = 1e100;
    uint64_t best_square_sum = 0;
    for (const Pair& left : pairs) {
        double target = pi - left.sum;
        auto it = std::lower_bound(
            pairs.begin(), pairs.end(), target,
            [](const Pair& item, double value) { return item.sum < value; });

        for (int offset = -2; offset <= 2; ++offset) {
            auto jt = it;
            if (offset < 0) {
                size_t delta = (size_t)(-offset);
                if ((size_t)(it - pairs.begin()) < delta) continue;
                jt -= delta;
            } else {
                size_t delta = (size_t)offset;
                if ((size_t)(it - pairs.begin()) + delta >= pairs.size()) continue;
                jt += delta;
            }

            double error = std::fabs(left.sum + jt->sum - pi);
            uint64_t square_sum = (uint64_t)left.square_sum + jt->square_sum;
            if (error < best_error ||
                (error == best_error && square_sum < best_square_sum)) {
                best_error = error;
                best_square_sum = square_sum;
            }
        }
    }
    return best_square_sum;
}

int main(int argc, char** argv) {
    int n = argc > 1 ? std::stoi(argv[1]) : 10000;
    std::cout << g(n) << '\n';
    return 0;
}
"""


def _binary():
    digest = hashlib.sha256(CPP_SOURCE.encode()).hexdigest()[:16]
    root = Path(tempfile.gettempdir()) / "eulerslop_build"
    root.mkdir(exist_ok=True)
    src = root / f"p461_{digest}.cpp"
    exe = root / f"p461_{digest}"
    if not exe.exists():
        src.write_text(CPP_SOURCE)
        subprocess.run(
            ["g++", "-O3", "-march=native", "-std=c++17", str(src), "-o", str(exe)],
            check=True,
        )
    return exe


def g(n):
    result = subprocess.run(
        [str(_binary()), str(n)],
        check=True,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.strip())


def solve():
    assert g(200) == 64_658
    return g(10_000)


if __name__ == "__main__":
    print(solve())
