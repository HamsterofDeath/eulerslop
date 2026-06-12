#!/usr/bin/env python3
import hashlib
import subprocess
import tempfile
from pathlib import Path


CPP_SOURCE = r"""
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <vector>

static std::vector<std::vector<int>> right_triangle_legs(int max_leg) {
    std::vector<std::vector<int>> by_leg((size_t)max_leg + 1);
    const int max_m = (int)std::sqrt(2.0 * max_leg) + 10;

    for (long long m = 2; m <= max_m; ++m) {
        for (long long n = 1; n < m; ++n) {
            if (((m - n) & 1) == 0 || std::gcd((int)m, (int)n) != 1) continue;

            const long long leg1 = m * m - n * n;
            const long long leg2 = 2 * m * n;
            const long long smaller = std::min(leg1, leg2);

            for (long long k = 1; k * smaller <= max_leg; ++k) {
                const long long a = k * leg1;
                const long long b = k * leg2;
                if (a <= max_leg && b <= max_leg) {
                    by_leg[(size_t)a].push_back((int)b);
                    by_leg[(size_t)b].push_back((int)a);
                } else if (a <= max_leg) {
                    by_leg[(size_t)a].push_back((int)b);
                } else if (b <= max_leg) {
                    by_leg[(size_t)b].push_back((int)a);
                }
            }
        }
    }

    for (auto& legs : by_leg) {
        std::sort(legs.begin(), legs.end());
        legs.erase(std::unique(legs.begin(), legs.end()), legs.end());
    }
    return by_leg;
}

static long long S(int perimeter_limit) {
    const int max_leg = perimeter_limit;
    const auto legs = right_triangle_legs(max_leg);
    long long total = 0;

    const int max_m = (int)std::sqrt((double)perimeter_limit) + 10;
    for (long long m = 2; m <= max_m; ++m) {
        for (long long n = 1; n < m; ++n) {
            if (((m - n) & 1) == 0 || std::gcd((int)m, (int)n) != 1) continue;

            const long long leg1 = m * m - n * n;
            const long long leg2 = 2 * m * n;
            const long long hypotenuse = m * m + n * n;

            for (int swapped = 0; swapped < 2; ++swapped) {
                const long long half_width0 = swapped ? leg2 : leg1;
                const long long flap_height0 = swapped ? leg1 : leg2;

                for (long long scale = 1;
                     2 * scale * (half_width0 + hypotenuse) <= perimeter_limit;
                     ++scale) {
                    const long long half_width = half_width0 * scale;
                    const long long flap_height = flap_height0 * scale;
                    const long long flap_side = hypotenuse * scale;
                    const long long max_rectangle_height =
                        (perimeter_limit - 2 * half_width - 2 * flap_side) / 2;

                    const auto& rectangle_heights = legs[(size_t)(2 * half_width)];
                    const auto& long_diagonal_heights = legs[(size_t)half_width];

                    auto begin = std::upper_bound(rectangle_heights.begin(),
                                                  rectangle_heights.end(),
                                                  (int)flap_height);
                    auto end = std::upper_bound(rectangle_heights.begin(),
                                                rectangle_heights.end(),
                                                (int)max_rectangle_height);
                    if (begin >= end) continue;

                    for (auto it = begin; it != end; ++it) {
                        const long long rectangle_height = *it;
                        const int combined_height =
                            (int)(rectangle_height + flap_height);
                        if (std::binary_search(long_diagonal_heights.begin(),
                                               long_diagonal_heights.end(),
                                               combined_height)) {
                            total += 2 * half_width + 2 * rectangle_height
                                   + 2 * flap_side;
                        }
                    }
                }
            }
        }
    }

    return total;
}

int main(int argc, char** argv) {
    int perimeter_limit = argc > 1 ? std::stoi(argv[1]) : 10000000;
    std::cout << S(perimeter_limit) << '\n';
    return 0;
}
"""


def _binary():
    digest = hashlib.sha256(CPP_SOURCE.encode()).hexdigest()[:16]
    root = Path(tempfile.gettempdir()) / "eulerslop_build"
    root.mkdir(exist_ok=True)
    src = root / f"p583_{digest}.cpp"
    exe = root / f"p583_{digest}"
    if not exe.exists():
        src.write_text(CPP_SOURCE)
        subprocess.run(
            ["g++", "-O3", "-march=native", "-std=c++17", str(src), "-o", str(exe)],
            check=True,
        )
    return exe


def S(perimeter_limit):
    result = subprocess.run(
        [str(_binary()), str(perimeter_limit)],
        check=True,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.strip())


def solve():
    assert S(10_000) == 884680
    return S(10_000_000)


if __name__ == "__main__":
    print(solve())
