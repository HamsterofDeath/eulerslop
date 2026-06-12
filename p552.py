#!/usr/bin/env python3
import hashlib
import subprocess
import tempfile
from pathlib import Path


CPP_SOURCE = r"""
#include <cstdint>
#include <iostream>
#include <vector>

static std::vector<int> primes_up_to(int n) {
    std::vector<bool> sieve(n + 1, true);
    if (n >= 0) sieve[0] = false;
    if (n >= 1) sieve[1] = false;
    for (int p = 2; (long long)p * p <= n; ++p) {
        if (sieve[p]) {
            for (long long j = (long long)p * p; j <= n; j += p) sieve[(std::size_t)j] = false;
        }
    }
    std::vector<int> primes;
    for (int i = 2; i <= n; ++i) if (sieve[i]) primes.push_back(i);
    return primes;
}

static long long mod_pow(long long a, long long e, long long mod) {
    long long r = 1;
    while (e) {
        if (e & 1LL) r = (__int128)r * a % mod;
        a = (__int128)a * a % mod;
        e >>= 1LL;
    }
    return r;
}

static long long S(int limit) {
    auto primes = primes_up_to(limit);
    int m = (int)primes.size();
    std::vector<int> a(m, 0), prod(m, 1);
    std::vector<char> found(m, 0);

    for (int idx = 0; idx < m; ++idx) {
        int p = primes[idx];
        int n = idx + 1;
        long long rhs = n - a[idx];
        rhs %= p;
        if (rhs < 0) rhs += p;
        int t = (int)(rhs * mod_pow(prod[idx], p - 2, p) % p);

        for (int j = idx + 1; j < m; ++j) {
            int q = primes[j];
            a[j] = (a[j] + (long long)prod[j] * t) % q;
            prod[j] = (long long)prod[j] * p % q;
            if (a[j] == 0) found[j] = 1;
        }
    }

    long long total = 0;
    for (int i = 0; i < m; ++i) {
        if (found[i]) total += primes[i];
    }
    return total;
}

int main(int argc, char** argv) {
    int limit = 300000;
    if (argc > 1) limit = std::stoi(argv[1]);
    std::cout << S(limit) << '\n';
    return 0;
}
"""


def _binary():
    digest = hashlib.sha256(CPP_SOURCE.encode()).hexdigest()[:16]
    root = Path(tempfile.gettempdir()) / "eulerslop_build"
    root.mkdir(exist_ok=True)
    src = root / f"p552_{digest}.cpp"
    exe = root / f"p552_{digest}"
    if not exe.exists():
        src.write_text(CPP_SOURCE)
        subprocess.run(["g++", "-O3", "-std=c++17", str(src), "-o", str(exe)], check=True)
    return exe


def S(limit):
    result = subprocess.run(
        [str(_binary()), str(limit)],
        check=True,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.strip())


def solve():
    assert S(50) == 69
    return S(300_000)


if __name__ == "__main__":
    print(solve())
