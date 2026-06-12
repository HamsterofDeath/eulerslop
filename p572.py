#!/usr/bin/env python3
import hashlib
import subprocess
import tempfile
from pathlib import Path


CPP_SOURCE = r"""
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <string>

static long long floor_div(long long a, long long b) {
    if (b < 0) {
        a = -a;
        b = -b;
    }
    if (a >= 0) return a / b;
    return -((-a + b - 1) / b);
}

static long long ceil_div(long long a, long long b) {
    if (b < 0) {
        a = -a;
        b = -b;
    }
    if (a >= 0) return (a + b - 1) / b;
    return -((-a) / b);
}

struct Range {
    int low;
    int high;
};

static long long count_complement_projectors(std::array<int, 3> u, int bound) {
    Range ranges[3];

    for (int column = 0; column < 3; ++column) {
        long long low = -4000000000000000000LL;
        long long high = 4000000000000000000LL;

        for (int row = 0; row < 3; ++row) {
            long long coeff = u[row];
            if (coeff == 0) {
                if (row == column && bound < 1) return 0;
                continue;
            }

            long long lo = row == column ? 1 - bound : -bound;
            long long hi = row == column ? 1 + bound : bound;
            if (coeff > 0) {
                low = std::max(low, ceil_div(lo, coeff));
                high = std::min(high, floor_div(hi, coeff));
            } else {
                low = std::max(low, ceil_div(hi, coeff));
                high = std::min(high, floor_div(lo, coeff));
            }
        }

        if (low > high) return 0;
        ranges[column] = {(int)low, (int)high};
    }

    int z = 0;
    for (int i = 1; i < 3; ++i) {
        if (std::abs(u[i]) > std::abs(u[z])) z = i;
    }
    int x = (z + 1) % 3;
    int y = (z + 2) % 3;

    long long count = 0;
    for (int vx = ranges[x].low; vx <= ranges[x].high; ++vx) {
        for (int vy = ranges[y].low; vy <= ranges[y].high; ++vy) {
            long long remainder = 1LL - u[x] * vx - u[y] * vy;
            if (remainder % u[z] != 0) continue;
            long long vz = remainder / u[z];
            if (ranges[z].low <= vz && vz <= ranges[z].high) ++count;
        }
    }
    return count;
}

static long long count_rank1(int bound) {
    long long total = 0;
    for (int a = -bound; a <= bound; ++a) {
        for (int b = -bound; b <= bound; ++b) {
            for (int c = -bound; c <= bound; ++c) {
                if (a == 0 && b == 0 && c == 0) continue;
                if (std::gcd(std::gcd(std::abs(a), std::abs(b)), std::abs(c)) != 1) {
                    continue;
                }

                std::array<int, 3> u{a, b, c};
                int max_abs = std::max({std::abs(a), std::abs(b), std::abs(c)});
                int vbound = bound / max_abs;
                int z = 0;
                for (int i = 1; i < 3; ++i) {
                    if (std::abs(u[i]) > std::abs(u[z])) z = i;
                }
                int x = (z + 1) % 3;
                int y = (z + 2) % 3;

                long long count = 0;
                for (int vx = -vbound; vx <= vbound; ++vx) {
                    for (int vy = -vbound; vy <= vbound; ++vy) {
                        long long remainder = 1LL - u[x] * vx - u[y] * vy;
                        if (remainder % u[z] != 0) continue;
                        long long vz = remainder / u[z];
                        if (-vbound <= vz && vz <= vbound) ++count;
                    }
                }
                total += count;
            }
        }
    }
    return total / 2;
}

static long long count_rank2(int bound) {
    long long total = 0;
    int ubound = bound + 1;
    for (int a = -ubound; a <= ubound; ++a) {
        for (int b = -ubound; b <= ubound; ++b) {
            for (int c = -ubound; c <= ubound; ++c) {
                if (a == 0 && b == 0 && c == 0) continue;
                if (std::gcd(std::gcd(std::abs(a), std::abs(b)), std::abs(c)) != 1) {
                    continue;
                }
                total += count_complement_projectors({a, b, c}, bound);
            }
        }
    }
    return total / 2;
}

static long long C(int bound) {
    return 2 + count_rank1(bound) + count_rank2(bound);
}

int main(int argc, char** argv) {
    int bound = argc > 1 ? std::stoi(argv[1]) : 200;
    std::cout << C(bound) << '\n';
    return 0;
}
"""


def _binary():
    digest = hashlib.sha256(CPP_SOURCE.encode()).hexdigest()[:16]
    root = Path(tempfile.gettempdir()) / "eulerslop_build"
    root.mkdir(exist_ok=True)
    src = root / f"p572_{digest}.cpp"
    exe = root / f"p572_{digest}"
    if not exe.exists():
        src.write_text(CPP_SOURCE)
        subprocess.run(
            ["g++", "-O3", "-march=native", "-std=c++17", str(src), "-o", str(exe)],
            check=True,
        )
    return exe


def C(n):
    result = subprocess.run(
        [str(_binary()), str(n)],
        check=True,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.strip())


def solve():
    assert C(1) == 164
    assert C(2) == 848
    return C(200)


if __name__ == "__main__":
    print(solve())
