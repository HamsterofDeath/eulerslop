#!/usr/bin/env python3
import hashlib
import subprocess
import tempfile
from pathlib import Path


CPP_SOURCE = r"""
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <numeric>
#include <string>
#include <vector>

using i128 = __int128_t;

static std::string to_string_i128(i128 x) {
    if (x == 0) return "0";
    std::string out;
    while (x > 0) {
        out.push_back(char('0' + x % 10));
        x /= 10;
    }
    std::reverse(out.begin(), out.end());
    return out;
}

static i128 int_pow(int base, int exponent) {
    i128 result = 1;
    while (exponent--) result *= base;
    return result;
}

static int cycle_count(const std::array<unsigned char, 24>& permutation) {
    bool seen[24] = {};
    int count = 0;
    for (int i = 0; i < 24; ++i) {
        if (seen[i]) continue;
        ++count;
        int j = i;
        while (!seen[j]) {
            seen[j] = true;
            j = permutation[j];
        }
    }
    return count;
}

static std::string count_colourings(int colours) {
    int sticker_id[8][3];
    int id = 0;
    for (int corner = 0; corner < 8; ++corner) {
        for (int axis = 0; axis < 3; ++axis) {
            sticker_id[corner][axis] = id++;
        }
    }

    std::map<int, long long> histogram;
    std::array<int, 8> corner_permutation{};
    std::iota(corner_permutation.begin(), corner_permutation.end(), 0);
    long long states = 0;

    do {
        for (int encoded = 0; encoded < 2187; ++encoded) {
            std::array<int, 8> orientation{};
            int value = encoded;
            int sum = 0;
            for (int i = 0; i < 7; ++i) {
                orientation[i] = value % 3;
                sum += orientation[i];
                value /= 3;
            }
            orientation[7] = (3 - sum % 3) % 3;

            std::array<unsigned char, 24> sticker_permutation{};
            for (int position = 0; position < 8; ++position) {
                int cubie = corner_permutation[position];
                int twist = orientation[position];
                for (int axis = 0; axis < 3; ++axis) {
                    sticker_permutation[sticker_id[cubie][axis]] =
                        (unsigned char)sticker_id[position][(axis + twist) % 3];
                }
            }
            ++histogram[cycle_count(sticker_permutation)];
            ++states;
        }
    } while (std::next_permutation(corner_permutation.begin(), corner_permutation.end()));

    i128 total = 0;
    for (const auto& [cycles, frequency] : histogram) {
        total += (i128)frequency * int_pow(colours, cycles);
    }
    return to_string_i128(total / states);
}

int main(int argc, char** argv) {
    int colours = argc > 1 ? std::stoi(argv[1]) : 10;
    std::cout << count_colourings(colours) << '\n';
    return 0;
}
"""


def _binary():
    digest = hashlib.sha256(CPP_SOURCE.encode()).hexdigest()[:16]
    root = Path(tempfile.gettempdir()) / "eulerslop_build"
    root.mkdir(exist_ok=True)
    src = root / f"p599_{digest}.cpp"
    exe = root / f"p599_{digest}"
    if not exe.exists():
        src.write_text(CPP_SOURCE)
        subprocess.run(
            ["g++", "-O3", "-march=native", "-std=c++17", str(src), "-o", str(exe)],
            check=True,
        )
    return exe


def count_colourings(colours):
    result = subprocess.run(
        [str(_binary()), str(colours)],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def solve():
    assert count_colourings(2) == "183"
    return count_colourings(10)


if __name__ == "__main__":
    print(solve())
