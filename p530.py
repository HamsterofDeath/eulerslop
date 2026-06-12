#!/usr/bin/env python3
import hashlib
import subprocess
import tempfile
from pathlib import Path


CPP_SOURCE = r"""
#include <bits/stdc++.h>
using namespace std;

using u64 = unsigned long long;
using i128 = __int128_t;

static u64 isqrt_u64(u64 x) {
    u64 r = (u64)sqrtl((long double)x);
    while ((__int128)(r + 1) * (r + 1) <= x) ++r;
    while ((__int128)r * r > x) --r;
    return r;
}

static vector<u64> phi_prefix(int limit) {
    vector<int> phi(limit + 1, 0);
    vector<int> primes;
    vector<unsigned char> composite(limit + 1, 0);
    phi[1] = 1;

    for (int n = 2; n <= limit; ++n) {
        if (!composite[n]) {
            primes.push_back(n);
            phi[n] = n - 1;
        }

        for (int p : primes) {
            long long v = (long long)n * p;
            if (v > limit) break;
            composite[(size_t)v] = 1;
            if (n % p == 0) {
                phi[(size_t)v] = phi[n] * p;
                break;
            }
            phi[(size_t)v] = phi[n] * (p - 1);
        }
    }

    vector<u64> prefix(limit + 1, 0);
    for (int n = 1; n <= limit; ++n) {
        prefix[n] = prefix[n - 1] + (unsigned int)phi[n];
    }
    return prefix;
}

struct DivisorSummatory {
    int table_limit;
    vector<u64> small;
    unordered_map<u64, u64> memo;

    explicit DivisorSummatory(int limit) : table_limit(limit), small((size_t)limit + 1, 0) {
        for (int d = 1; d <= table_limit; ++d) {
            for (int multiple = d; multiple <= table_limit; multiple += d) {
                ++small[(size_t)multiple];
            }
        }

        for (int n = 1; n <= table_limit; ++n) {
            small[n] += small[n - 1];
        }
        memo.reserve(200000);
    }

    u64 D(u64 n) {
        if (n <= (u64)table_limit) return small[(size_t)n];

        auto found = memo.find(n);
        if (found != memo.end()) return found->second;

        u64 root = isqrt_u64(n);
        u64 sum = 0;
        for (u64 i = 1; i <= root; ++i) {
            sum += n / i;
        }

        u64 answer = 2 * sum - root * root;
        memo.emplace(n, answer);
        return answer;
    }
};

static string to_string_i128(i128 value) {
    if (value == 0) return "0";
    string digits;
    while (value > 0) {
        digits.push_back((char)('0' + value % 10));
        value /= 10;
    }
    reverse(digits.begin(), digits.end());
    return digits;
}

static i128 F(u64 limit) {
    int root = (int)isqrt_u64(limit);
    vector<u64> phi_sum = phi_prefix(root);
    DivisorSummatory divisor_sum(5000000);

    i128 total = 0;
    for (u64 t = 1; t <= (u64)root;) {
        u64 q = limit / (t * t);
        u64 high = isqrt_u64(limit / q);
        if (high > (u64)root) high = root;

        u64 phi_range = phi_sum[(size_t)high] - phi_sum[(size_t)t - 1];
        total += (i128)phi_range * divisor_sum.D(q);
        t = high + 1;
    }

    return total;
}

int main(int argc, char** argv) {
    u64 limit = 1000000000000000ULL;
    if (argc > 1) limit = strtoull(argv[1], nullptr, 10);
    cout << to_string_i128(F(limit)) << '\n';
    return 0;
}
"""


def _binary():
    digest = hashlib.sha256(CPP_SOURCE.encode()).hexdigest()[:16]
    root = Path(tempfile.gettempdir()) / "eulerslop_build"
    root.mkdir(exist_ok=True)
    src = root / f"p530_{digest}.cpp"
    exe = root / f"p530_{digest}"
    if not exe.exists():
        src.write_text(CPP_SOURCE)
        subprocess.run(
            ["g++", "-O3", "-march=native", "-std=c++17", str(src), "-o", str(exe)],
            check=True,
        )
    return exe


def F(limit):
    result = subprocess.run(
        [str(_binary()), str(limit)],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def solve():
    assert F(10) == "32"
    assert F(1000) == "12776"
    return F(10**15)


if __name__ == "__main__":
    print(solve())
