#!/usr/bin/env python3
import hashlib
import subprocess
import tempfile
from pathlib import Path


CPP_SOURCE = r"""
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>

using u64 = unsigned long long;
using u128 = __uint128_t;

static constexpr u64 OUTMOD = 10000000000000061ULL;

static u64 add_mod(u64 a, u64 b) {
    return (u64)(((u128)a + b) % OUTMOD);
}

static u64 mul_mod(u64 a, u64 b) {
    return (u64)(((u128)a * b) % OUTMOD);
}

static std::vector<int> primes_upto(int n) {
    std::vector<unsigned char> is_prime((size_t)n + 1, 1);
    if (n >= 0) is_prime[0] = 0;
    if (n >= 1) is_prime[1] = 0;
    for (int p = 2; (long long)p * p <= n; ++p) {
        if (is_prime[p]) {
            for (long long q = (long long)p * p; q <= n; q += p) {
                is_prime[(size_t)q] = 0;
            }
        }
    }

    std::vector<int> primes;
    for (int p = 2; p <= n; ++p) {
        if (is_prime[p]) primes.push_back(p);
    }
    return primes;
}

static long long exponent_in_factorial(int n, int p) {
    long long total = 0;
    while (n > 0) {
        n /= p;
        total += n;
    }
    return total;
}

static u64 target_count(int n) {
    // 65432 = 8 * 8179, so divisor exponents must have v2 = 3 and v5 = 0.
    // The remaining unit part is counted modulo 100000 / 8 = 12500.
    static constexpr int RESIDUE_MOD = 12500;
    static constexpr int TARGET = 8179;

    std::vector<int> units;
    std::vector<unsigned char> is_unit(RESIDUE_MOD, 0);
    for (int r = 0; r < RESIDUE_MOD; ++r) {
        if (std::gcd(r, 10) == 1) {
            units.push_back(r);
            is_unit[r] = 1;
        }
    }

    std::vector<u64> dp(RESIDUE_MOD), next(RESIDUE_MOD);
    dp[1] = 1;
    auto primes = primes_upto(n);
    std::vector<int> seen(RESIDUE_MOD, 0);
    int stamp = 0;

    for (int p : primes) {
        if (p == 2 || p == 5) continue;
        long long exponent = exponent_in_factorial(n, p);
        int base = p % RESIDUE_MOD;

        std::fill(next.begin(), next.end(), 0);
        ++stamp;
        if (stamp == INT32_MAX) {
            std::fill(seen.begin(), seen.end(), 0);
            stamp = 1;
        }

        for (int unit : units) {
            if (seen[unit] == stamp) continue;

            std::vector<int> cycle;
            int x = unit;
            while (seen[x] != stamp) {
                seen[x] = stamp;
                cycle.push_back(x);
                x = (int)((long long)x * base % RESIDUE_MOD);
            }

            int length = (int)cycle.size();
            long long choices = exponent + 1;
            u64 full_cycles = (u64)(choices / length);
            int remainder = (int)(choices % length);

            u64 cycle_sum = 0;
            for (int residue : cycle) cycle_sum = add_mod(cycle_sum, dp[residue]);
            u64 common = mul_mod(full_cycles % OUTMOD, cycle_sum);

            if (remainder == 0) {
                for (int residue : cycle) next[residue] = common;
                continue;
            }

            u64 extra = 0;
            for (int t = 0; t < remainder; ++t) {
                extra = add_mod(extra, dp[cycle[(length - t) % length]]);
            }
            for (int i = 0; i < length; ++i) {
                next[cycle[i]] = add_mod(common, extra);
                extra = add_mod(extra, dp[cycle[(i + 1) % length]]);
                u64 remove = dp[cycle[(i - remainder + 1 + length) % length]];
                extra = (extra + OUTMOD - remove) % OUTMOD;
            }
        }
        dp.swap(next);
    }

    return dp[TARGET];
}

static u64 small_full_count(int n, int digits) {
    int modulus = 1;
    for (size_t i = 0; i < std::to_string(digits).size(); ++i) modulus *= 10;

    std::vector<u64> dp(modulus), next(modulus);
    dp[1 % modulus] = 1;
    for (int p : primes_upto(n)) {
        long long exponent = exponent_in_factorial(n, p);
        std::fill(next.begin(), next.end(), 0);
        int power = 1 % modulus;
        for (long long e = 0; e <= exponent; ++e) {
            for (int residue = 0; residue < modulus; ++residue) {
                if (dp[residue] == 0) continue;
                int nr = (int)((long long)residue * power % modulus);
                next[nr] = add_mod(next[nr], dp[residue]);
            }
            power = (int)((long long)power * (p % modulus) % modulus);
        }
        dp.swap(next);
    }
    return dp[digits % modulus];
}

int main(int argc, char** argv) {
    if (argc > 1 && std::string(argv[1]) == "sample12") {
        std::cout << small_full_count(12, 12) << '\n';
    } else if (argc > 1 && std::string(argv[1]) == "sample50") {
        std::cout << small_full_count(50, 123) << '\n';
    } else {
        std::cout << target_count(1000000) << '\n';
    }
    return 0;
}
"""


def _binary():
    digest = hashlib.sha256(CPP_SOURCE.encode()).hexdigest()[:16]
    root = Path(tempfile.gettempdir()) / "eulerslop_build"
    root.mkdir(exist_ok=True)
    src = root / f"p474_{digest}.cpp"
    exe = root / f"p474_{digest}"
    if not exe.exists():
        src.write_text(CPP_SOURCE)
        subprocess.run(
            ["g++", "-O3", "-march=native", "-std=c++17", str(src), "-o", str(exe)],
            check=True,
        )
    return exe


def run(*args):
    result = subprocess.run(
        [str(_binary()), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.strip())


def solve():
    assert run("sample12") == 11
    assert run("sample50") == 17_888
    return run()


if __name__ == "__main__":
    print(solve())
