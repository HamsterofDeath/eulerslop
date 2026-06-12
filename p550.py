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

static constexpr int64_t MOD = 987654321;

static int64_t mod_pow(int64_t base, int64_t exponent) {
    int64_t result = 1;
    base %= MOD;
    while (exponent > 0) {
        if (exponent & 1) result = (__int128)result * base % MOD;
        base = (__int128)base * base % MOD;
        exponent >>= 1;
    }
    return result;
}

static std::vector<int64_t> xor_convolution(const std::vector<int64_t>& a,
                                            const std::vector<int64_t>& b) {
    const int size = (int)a.size();
    std::vector<int64_t> out(size, 0);
    for (int i = 0; i < size; ++i) {
        if (a[i] == 0) continue;
        for (int j = 0; j < size; ++j) {
            if (b[j] == 0) continue;
            out[i ^ j] = (out[i ^ j] + (__int128)a[i] * b[j]) % MOD;
        }
    }
    return out;
}

static std::vector<int64_t> xor_power(std::vector<int64_t> base, int64_t exponent) {
    std::vector<int64_t> result(base.size(), 0);
    result[0] = 1;
    while (exponent > 0) {
        if (exponent & 1) result = xor_convolution(result, base);
        exponent >>= 1;
        if (exponent) base = xor_convolution(base, base);
    }
    return result;
}

static std::vector<int> grundy_by_factor_count(int max_omega) {
    std::vector<int> grundy(max_omega + 1, 0);
    for (int omega = 2; omega <= max_omega; ++omega) {
        std::vector<unsigned char> seen(128, 0);
        for (int left = 1; left < omega; ++left) {
            for (int right = 1; right < omega; ++right) {
                seen[grundy[left] ^ grundy[right]] = 1;
            }
        }
        int mex = 0;
        while (seen[mex]) ++mex;
        grundy[omega] = mex;
    }
    return grundy;
}

static std::vector<int64_t> grundy_distribution(int limit) {
    int max_omega = 0;
    for (int x = limit; x > 1; x >>= 1) ++max_omega;
    auto grundy = grundy_by_factor_count(max_omega);

    int vector_size = 1;
    while (vector_size <= *std::max_element(grundy.begin(), grundy.end())) {
        vector_size <<= 1;
    }

    std::vector<unsigned char> composite((size_t)limit + 1, 0);
    std::vector<unsigned char> omega((size_t)limit + 1, 0);

    for (int p = 2; p <= limit; ++p) {
        if (composite[p]) continue;

        if ((int64_t)p * p <= limit) {
            for (int64_t multiple = (int64_t)p * p; multiple <= limit; multiple += p) {
                composite[(size_t)multiple] = 1;
            }
        }

        for (int64_t power = p; power <= limit; ) {
            for (int multiple = (int)power; multiple <= limit; multiple += (int)power) {
                ++omega[(size_t)multiple];
            }
            if (power > limit / p) break;
            power *= p;
        }
    }

    std::vector<int64_t> distribution(vector_size, 0);
    for (int n = 2; n <= limit; ++n) {
        ++distribution[grundy[omega[(size_t)n]]];
    }
    return distribution;
}

static int64_t f(int limit, int64_t piles) {
    auto distribution = grundy_distribution(limit);
    auto powered = xor_power(distribution, piles);
    int64_t total = mod_pow(limit - 1, piles);
    return (total - powered[0] + MOD) % MOD;
}

int main(int argc, char** argv) {
    int limit = argc > 1 ? std::stoi(argv[1]) : 10000000;
    int64_t piles = argc > 2 ? std::stoll(argv[2]) : 1000000000000LL;
    std::cout << f(limit, piles) << '\n';
    return 0;
}
"""


def _binary():
    digest = hashlib.sha256(CPP_SOURCE.encode()).hexdigest()[:16]
    root = Path(tempfile.gettempdir()) / "eulerslop_build"
    root.mkdir(exist_ok=True)
    src = root / f"p550_{digest}.cpp"
    exe = root / f"p550_{digest}"
    if not exe.exists():
        src.write_text(CPP_SOURCE)
        subprocess.run(
            ["g++", "-O3", "-march=native", "-std=c++17", str(src), "-o", str(exe)],
            check=True,
        )
    return exe


def f(limit, piles):
    result = subprocess.run(
        [str(_binary()), str(limit), str(piles)],
        check=True,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.strip())


def solve():
    assert f(10, 5) == 40085
    return f(10_000_000, 10**12)


if __name__ == "__main__":
    print(solve())
