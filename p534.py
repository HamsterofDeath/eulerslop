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
#include <unordered_map>
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

static std::vector<int> decode(uint64_t state, int len) {
    std::vector<int> out(len);
    for (int i = len - 1; i >= 0; --i) {
        out[i] = (int)(state & 15ULL);
        state >>= 4;
    }
    return out;
}

static uint64_t push_state(uint64_t state, int col, int keep) {
    uint64_t next = (state << 4) | (uint64_t)col;
    if (keep < 16) next &= ((1ULL << (4 * keep)) - 1ULL);
    return next;
}

static i128 Q(int n, int w) {
    int reach = n - 1 - w;
    if (reach == 0) {
        i128 total = 1;
        for (int i = 0; i < n; ++i) total *= n;
        return total;
    }

    std::unordered_map<uint64_t, i128> dp, next;
    dp.reserve(1 << 16);
    dp[0] = 1;
    for (int row = 0; row < n; ++row) {
        int len = std::min(reach, row);
        int next_len = std::min(reach, row + 1);
        next.clear();
        next.reserve(dp.size() * 2 + 32);
        for (const auto& kv : dp) {
            auto prev = decode(kv.first, len);
            for (int col = 0; col < n; ++col) {
                bool ok = true;
                for (int i = 0; i < len; ++i) {
                    int back = len - i;
                    int old_col = prev[i];
                    if (col == old_col || std::abs(col - old_col) == back) {
                        ok = false;
                        break;
                    }
                }
                if (ok) {
                    next[push_state(kv.first, col, next_len)] += kv.second;
                }
            }
        }
        dp.swap(next);
    }

    i128 total = 0;
    for (const auto& kv : dp) total += kv.second;
    return total;
}

static i128 S(int n) {
    i128 total = 0;
    for (int w = 0; w < n; ++w) total += Q(n, w);
    return total;
}

int main(int argc, char** argv) {
    int n = argc > 1 ? std::stoi(argv[1]) : 14;
    std::cout << to_string_i128(S(n)) << '\n';
    return 0;
}
"""


def _binary():
    digest = hashlib.sha256(CPP_SOURCE.encode()).hexdigest()[:16]
    root = Path(tempfile.gettempdir()) / "eulerslop_build"
    root.mkdir(exist_ok=True)
    src = root / f"p534_{digest}.cpp"
    exe = root / f"p534_{digest}"
    if not exe.exists():
        src.write_text(CPP_SOURCE)
        subprocess.run(["g++", "-O2", "-std=c++17", str(src), "-o", str(exe)], check=True)
    return exe


def S(n):
    result = subprocess.run(
        [str(_binary()), str(n)],
        check=True,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.strip())


def solve():
    assert S(4) == 276
    assert S(5) == 3347
    return S(14)


if __name__ == "__main__":
    print(solve())
