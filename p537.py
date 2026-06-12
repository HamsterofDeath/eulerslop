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

static constexpr int MOD = 1004535809;
static constexpr int ROOT = 3;

static long long mod_pow(long long base, long long exponent) {
    long long result = 1;
    while (exponent) {
        if (exponent & 1) result = result * base % MOD;
        base = base * base % MOD;
        exponent >>= 1;
    }
    return result;
}

static void ntt(std::vector<int>& a, bool inverse) {
    int n = (int)a.size();
    static std::vector<int> rev;
    static std::vector<int> roots{0, 1};

    if ((int)rev.size() != n) {
        int bits = __builtin_ctz(n);
        rev.assign(n, 0);
        for (int i = 0; i < n; ++i) {
            rev[i] = (rev[i >> 1] >> 1) | ((i & 1) << (bits - 1));
        }
    }

    if ((int)roots.size() < n) {
        int bits = __builtin_ctz((int)roots.size());
        roots.resize(n);
        while ((1 << bits) < n) {
            long long step = mod_pow(ROOT, (MOD - 1) >> (bits + 1));
            for (int i = 1 << (bits - 1); i < (1 << bits); ++i) {
                roots[2 * i] = roots[i];
                roots[2 * i + 1] = (long long)roots[i] * step % MOD;
            }
            ++bits;
        }
    }

    for (int i = 0; i < n; ++i) {
        if (i < rev[i]) std::swap(a[i], a[rev[i]]);
    }

    for (int len = 1; len < n; len <<= 1) {
        for (int start = 0; start < n; start += 2 * len) {
            for (int j = 0; j < len; ++j) {
                int u = a[start + j];
                int v = (long long)a[start + j + len] * roots[len + j] % MOD;
                int x = u + v;
                if (x >= MOD) x -= MOD;
                int y = u - v;
                if (y < 0) y += MOD;
                a[start + j] = x;
                a[start + j + len] = y;
            }
        }
    }

    if (inverse) {
        std::reverse(a.begin() + 1, a.end());
        long long inv_n = mod_pow(n, MOD - 2);
        for (int& x : a) x = x * inv_n % MOD;
    }
}

static std::vector<int> multiply(std::vector<int> a, std::vector<int> b, int need) {
    int result_size = std::min(need, (int)a.size() + (int)b.size() - 1);
    int n = 1;
    while (n < (int)a.size() + (int)b.size() - 1) n <<= 1;
    a.resize(n);
    b.resize(n);
    ntt(a, false);
    ntt(b, false);
    for (int i = 0; i < n; ++i) a[i] = (long long)a[i] * b[i] % MOD;
    ntt(a, true);
    a.resize(result_size);
    return a;
}

static std::vector<int> poly_pow(std::vector<int> base, int exponent, int need) {
    std::vector<int> result(1, 1);
    while (exponent) {
        if (exponent & 1) result = multiply(result, base, need);
        exponent >>= 1;
        if (exponent) base = multiply(base, base, need);
    }
    return result;
}

static std::vector<int> first_primes(int count) {
    int limit = 300000;
    while (true) {
        std::vector<unsigned char> is_prime((size_t)limit + 1, 1);
        is_prime[0] = is_prime[1] = 0;
        for (int p = 2; (long long)p * p <= limit; ++p) {
            if (is_prime[p]) {
                for (long long q = (long long)p * p; q <= limit; q += p) {
                    is_prime[(size_t)q] = 0;
                }
            }
        }
        std::vector<int> primes;
        for (int p = 2; p <= limit; ++p) {
            if (is_prime[p]) primes.push_back(p);
        }
        if ((int)primes.size() >= count) return primes;
        limit *= 2;
    }
}

static int T(int n, int k) {
    auto primes = first_primes(n + 2);
    std::vector<int> counts(n + 1);
    counts[0] = 1;
    for (int j = 1; j <= n; ++j) {
        counts[j] = primes[j] - primes[j - 1];
    }
    auto powered = poly_pow(counts, k, n + 1);
    return n < (int)powered.size() ? powered[n] : 0;
}

int main(int argc, char** argv) {
    if (argc == 3) {
        std::cout << T(std::stoi(argv[1]), std::stoi(argv[2])) << '\n';
    } else {
        std::cout << T(20000, 20000) << '\n';
    }
    return 0;
}
"""


def _binary():
    digest = hashlib.sha256(CPP_SOURCE.encode()).hexdigest()[:16]
    root = Path(tempfile.gettempdir()) / "eulerslop_build"
    root.mkdir(exist_ok=True)
    src = root / f"p537_{digest}.cpp"
    exe = root / f"p537_{digest}"
    if not exe.exists():
        src.write_text(CPP_SOURCE)
        subprocess.run(
            ["g++", "-O3", "-march=native", "-std=c++17", str(src), "-o", str(exe)],
            check=True,
        )
    return exe


def T(n, k):
    result = subprocess.run(
        [str(_binary()), str(n), str(k)],
        check=True,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.strip())


def solve():
    assert T(3, 3) == 19
    assert T(10, 10) == 869_985
    assert T(1000, 1000) == 578_270_566

    result = subprocess.run(
        [str(_binary())],
        check=True,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.strip())


if __name__ == "__main__":
    print(solve())
