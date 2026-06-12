#!/usr/bin/env python3

import subprocess
import tempfile
from pathlib import Path


SOURCE = r"""
#include <bits/stdc++.h>
using namespace std;

using u64 = unsigned long long;
using u128 = __uint128_t;

static const uint32_t MOD = 100000007U;

uint64_t mod_pow(uint64_t base, uint64_t exp) {
    uint64_t result = 1;
    while (exp > 0) {
        if (exp & 1) result = result * base % MOD;
        base = base * base % MOD;
        exp >>= 1;
    }
    return result;
}

struct LucasBinomial {
    vector<uint32_t> needed;
    vector<uint32_t> factorial;

    void collect(u64 n) {
        u128 top = (u128)2 * n - 1;
        u128 bottom = n;
        while (top || bottom) {
            uint32_t a = top % MOD;
            uint32_t b = bottom % MOD;
            if (b <= a) {
                needed.push_back(a);
                needed.push_back(b);
                needed.push_back(a - b);
            }
            top /= MOD;
            bottom /= MOD;
        }
    }

    void build() {
        needed.push_back(0);
        sort(needed.begin(), needed.end());
        needed.erase(unique(needed.begin(), needed.end()), needed.end());
        factorial.assign(needed.size(), 0);

        uint64_t value = 1;
        size_t at = 0;
        if (needed[0] == 0) {
            factorial[0] = 1;
            at = 1;
        }

        for (uint32_t i = 1; i <= needed.back(); ++i) {
            value = value * i % MOD;
            while (at < needed.size() && needed[at] == i) {
                factorial[at++] = value;
            }
        }
    }

    uint64_t fact(uint32_t n) const {
        auto it = lower_bound(needed.begin(), needed.end(), n);
        return factorial[it - needed.begin()];
    }

    uint64_t small_binomial(uint32_t n, uint32_t k) const {
        if (k > n) return 0;
        uint64_t result = fact(n);
        result = result * mod_pow(fact(k), MOD - 2) % MOD;
        result = result * mod_pow(fact(n - k), MOD - 2) % MOD;
        return result;
    }

    uint64_t central(u64 n) const {
        u128 top = (u128)2 * n - 1;
        u128 bottom = n;
        uint64_t result = 1;
        while (top || bottom) {
            uint32_t a = top % MOD;
            uint32_t b = bottom % MOD;
            if (b > a) return 0;
            result = result * small_binomial(a, b) % MOD;
            top /= MOD;
            bottom /= MOD;
        }
        return result;
    }
};

uint64_t c_value(u64 n, const LucasBinomial& lucas) {
    uint64_t n_mod = n % MOD;
    uint64_t result = 16 * lucas.central(n) % MOD;
    result = (result + MOD - (3 * n_mod % MOD) * n_mod % MOD) % MOD;
    result = (result + MOD - 2 * n_mod % MOD) % MOD;
    result = (result + MOD - 7) % MOD;
    return result;
}

int main() {
    vector<u64> fib(91);
    fib[1] = fib[2] = 1;
    for (int i = 3; i <= 90; ++i) fib[i] = fib[i - 1] + fib[i - 2];

    LucasBinomial lucas;
    for (int i = 1; i <= 90; ++i) lucas.collect(fib[i]);
    lucas.build();

    if (c_value(1, lucas) != 4) return 1;
    if (c_value(2, lucas) != 25) return 2;
    if (c_value(10, lucas) != 1477721) return 3;

    uint64_t answer = 0;
    for (int i = 2; i <= 90; ++i) {
        answer += c_value(fib[i], lucas);
        answer %= MOD;
    }
    cout << answer << '\n';
    return 0;
}
"""


def solve():
    with tempfile.TemporaryDirectory(prefix="p554_") as tmp:
        tmp_path = Path(tmp)
        cpp = tmp_path / "p554.cpp"
        exe = tmp_path / "p554"
        cpp.write_text(SOURCE)
        subprocess.run(
            ["g++", "-O3", "-std=c++17", str(cpp), "-o", str(exe)],
            check=True,
        )
        result = subprocess.run(
            [str(exe)],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        )
    return result.stdout.strip()


if __name__ == "__main__":
    print(solve())
