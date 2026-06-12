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

static const long long MOD = 1000000000LL;

static std::vector<std::pair<unsigned long long, int>> factor(unsigned long long n) {
    std::vector<std::pair<unsigned long long, int>> out;
    for (unsigned long long p = 2; p * p <= n; p += (p == 2 ? 1 : 2)) {
        if (n % p == 0) {
            int e = 0;
            while (n % p == 0) {
                n /= p;
                ++e;
            }
            out.push_back({p, e});
        }
    }
    if (n > 1) out.push_back({n, 1});
    return out;
}

static void gen_divisors(
    const std::vector<std::pair<unsigned long long, int>>& f,
    int idx,
    unsigned long long cur,
    std::vector<unsigned long long>& divisors
) {
    if (idx == (int)f.size()) {
        divisors.push_back(cur);
        return;
    }
    auto [p, e] = f[idx];
    unsigned long long v = 1;
    for (int i = 0; i <= e; ++i) {
        gen_divisors(f, idx + 1, cur * v, divisors);
        v *= p;
    }
}

static std::vector<long long> convolve(
    const std::vector<long long>& a,
    const std::vector<long long>& b
) {
    int k = (int)a.size();
    std::vector<long long> c(k, 0);
    for (int i = 0; i < k; ++i) {
        long long ai = a[i];
        if (!ai) continue;
        for (int j = 0; j < k; ++j) {
            long long bj = b[j];
            if (!bj) continue;
            int idx = i + j;
            if (idx >= k) idx -= k;
            c[idx] = (c[idx] + ai * bj) % MOD;
        }
    }
    return c;
}

static long long seq(unsigned long long n, int k) {
    std::vector<unsigned long long> divisors;
    gen_divisors(factor(n), 0, 1, divisors);

    std::vector<long long> base(k, 0), result(k, 0);
    result[0] = 1;
    for (auto d : divisors) {
        base[d % (unsigned long long)k] += 1;
    }

    unsigned long long exp = n;
    while (exp) {
        if (exp & 1ULL) result = convolve(result, base);
        exp >>= 1ULL;
        if (exp) base = convolve(base, base);
    }
    return result[(k - (int)(n % (unsigned long long)k)) % k];
}

int main(int argc, char** argv) {
    unsigned long long n = std::stoull(argv[1]);
    int k = std::stoi(argv[2]);
    std::cout << seq(n, k) << '\n';
    return 0;
}
"""


def _binary():
    digest = hashlib.sha256(CPP_SOURCE.encode()).hexdigest()[:16]
    root = Path(tempfile.gettempdir()) / "eulerslop_build"
    root.mkdir(exist_ok=True)
    src = root / f"p511_{digest}.cpp"
    exe = root / f"p511_{digest}"
    if not exe.exists():
        src.write_text(CPP_SOURCE)
        subprocess.run(["g++", "-O3", "-std=c++17", str(src), "-o", str(exe)], check=True)
    return exe


def Seq(n, k):
    result = subprocess.run(
        [str(_binary()), str(n), str(k)],
        check=True,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.strip())


def solve():
    assert Seq(3, 4) == 4
    assert Seq(4, 11) == 8
    assert Seq(1111, 24) == 840643584
    return Seq(1234567898765, 4321)


if __name__ == "__main__":
    print(solve())
