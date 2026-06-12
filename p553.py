#!/usr/bin/env python3
import hashlib
import subprocess
import tempfile
from pathlib import Path


CPP_SOURCE = r"""
#include <cstdint>
#include <iostream>
#include <vector>

static constexpr int MOD = 1000000007;

static long long mod_pow(long long base, long long exponent, long long modulus) {
    long long result = 1 % modulus;
    base %= modulus;
    while (exponent > 0) {
        if (exponent & 1) result = result * base % modulus;
        base = base * base % modulus;
        exponent >>= 1;
    }
    return result;
}

static int add_mod(int a, long long b) {
    long long value = a + b;
    value %= MOD;
    return (int)value;
}

static int C(int n, int components) {
    std::vector<int> fact(n + 1, 1), invfact(n + 1, 1), inv(n + 1, 1);
    for (int i = 1; i <= n; ++i) fact[i] = (long long)fact[i - 1] * i % MOD;
    invfact[n] = (int)mod_pow(fact[n], MOD - 2, MOD);
    for (int i = n; i >= 1; --i) invfact[i - 1] = (long long)invfact[i] * i % MOD;
    for (int i = 1; i <= n; ++i) inv[i] = (int)mod_pow(i, MOD - 2, MOD);

    std::vector<int> full_family_value(n + 1, 0);
    full_family_value[0] = 1;
    long long exponent_mod = 1;
    for (int m = 1; m <= n; ++m) {
        exponent_mod = exponent_mod * 2 % (MOD - 1);
        full_family_value[m] = (int)mod_pow(2, (exponent_mod - 1 + MOD - 1) % (MOD - 1), MOD);
    }

    // T(z) is the EGF for all non-empty-subset families whose union is the
    // whole labelled support.  Inclusion-exclusion gives ordinary series
    // coefficients T_m / m! directly.
    std::vector<int> all_full(n + 1, 0);
    all_full[0] = 1;
    for (int m = 1; m <= n; ++m) {
        long long total = 0;
        for (int r = 0; r <= m; ++r) {
            long long term = (long long)full_family_value[r] * invfact[r] % MOD
                           * invfact[m - r] % MOD;
            if ((m - r) & 1) {
                total -= term;
            } else {
                total += term;
            }
            total %= MOD;
        }
        if (total < 0) total += MOD;
        all_full[m] = (int)total;
    }

    // B(z) = log(T(z)) is the EGF for connected components.
    std::vector<int> connected(n + 1, 0);
    for (int m = 1; m <= n; ++m) {
        long long value = (long long)m * all_full[m] % MOD;
        for (int i = 1; i < m; ++i) {
            value -= (long long)i * connected[i] % MOD * all_full[m - i] % MOD;
            value %= MOD;
        }
        if (value < 0) value += MOD;
        connected[m] = (long long)value * inv[m] % MOD;
    }

    std::vector<int> power(n + 1, 0);
    power[0] = 1;
    for (int step = 0; step < components; ++step) {
        std::vector<int> next(n + 1, 0);
        for (int i = 0; i <= n; ++i) {
            if (power[i] == 0) continue;
            for (int j = 1; i + j <= n; ++j) {
                if (connected[j] == 0) continue;
                next[i + j] = add_mod(next[i + j],
                                      (long long)power[i] * connected[j]);
            }
        }
        power.swap(next);
    }

    // Unused ground elements contribute exp(z).  Divide by components! for
    // the unordered connected components, then extract the labelled count.
    long long coefficient = 0;
    for (int i = 0; i <= n; ++i) {
        coefficient += (long long)power[i] * invfact[n - i] % MOD;
        coefficient %= MOD;
    }

    return (long long)fact[n] * coefficient % MOD * invfact[components] % MOD;
}

int main(int argc, char** argv) {
    int n = argc > 1 ? std::stoi(argv[1]) : 10000;
    int components = argc > 2 ? std::stoi(argv[2]) : 10;
    std::cout << C(n, components) << '\n';
    return 0;
}
"""


def _binary():
    digest = hashlib.sha256(CPP_SOURCE.encode()).hexdigest()[:16]
    root = Path(tempfile.gettempdir()) / "eulerslop_build"
    root.mkdir(exist_ok=True)
    src = root / f"p553_{digest}.cpp"
    exe = root / f"p553_{digest}"
    if not exe.exists():
        src.write_text(CPP_SOURCE)
        subprocess.run(
            ["g++", "-O3", "-march=native", "-std=c++17", str(src), "-o", str(exe)],
            check=True,
        )
    return exe


def C(n, components):
    result = subprocess.run(
        [str(_binary()), str(n), str(components)],
        check=True,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.strip())


def solve():
    assert C(2, 1) == 6
    assert C(3, 1) == 111
    assert C(4, 2) == 486
    assert C(100, 10) == 728209718
    return C(10_000, 10)


if __name__ == "__main__":
    print(solve())
