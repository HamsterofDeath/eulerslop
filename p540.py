#!/usr/bin/env python3
import hashlib
import subprocess
import tempfile
from pathlib import Path


CPP_SOURCE = r"""
#include <bits/stdc++.h>
using namespace std;

static unsigned long long isqrt_u64(unsigned long long x) {
    unsigned long long r = (unsigned long long)sqrtl((long double)x);
    while ((__int128)(r + 1) * (r + 1) <= x) ++r;
    while ((__int128)r * r > x) --r;
    return r;
}

static vector<int8_t> mobius_upto(int limit) {
    vector<int> primes;
    vector<int> least_prime(limit + 1, 0);
    vector<int8_t> mu(limit + 1, 0);
    mu[1] = 1;

    for (int n = 2; n <= limit; ++n) {
        if (least_prime[n] == 0) {
            least_prime[n] = n;
            primes.push_back(n);
            mu[n] = -1;
        }

        for (int p : primes) {
            long long v = (long long)p * n;
            if (v > limit || p > least_prime[n]) break;

            least_prime[(int)v] = p;
            if (p == least_prime[n]) {
                mu[(int)v] = 0;
                break;
            }
            mu[(int)v] = -mu[n];
        }
    }

    return mu;
}

struct CircleCounter {
    int table_limit;
    vector<uint32_t> prefix;

    explicit CircleCounter(int limit) : table_limit(limit), prefix((size_t)limit + 1, 0) {
        for (long long n = 1; n * n + (n + 1) * (n + 1) <= table_limit; ++n) {
            long long max_m = (long long)isqrt_u64((unsigned long long)table_limit - n * n);
            for (long long m = n + 1; m <= max_m; m += 2) {
                ++prefix[(size_t)(n * n + m * m)];
            }
        }

        for (int i = 1; i <= table_limit; ++i) {
            prefix[i] += prefix[i - 1];
        }
    }

    unsigned long long count_opposite_parity_pairs(unsigned long long x) const {
        if (x <= (unsigned long long)table_limit) return prefix[(size_t)x];

        unsigned long long total = 0;
        for (unsigned long long n = 1; n * n + (n + 1) * (n + 1) <= x; ++n) {
            unsigned long long max_m = isqrt_u64(x - n * n);
            total += (max_m - n + 1) / 2;
        }
        return total;
    }
};

static unsigned long long P(unsigned long long limit) {
    int max_divisor = (int)isqrt_u64(limit / 5);
    vector<int8_t> mu = mobius_upto(max_divisor);
    CircleCounter counter(100000000);

    long long total = 0;
    for (int d = 1; d <= max_divisor; d += 2) {
        if (mu[d] == 0) continue;

        unsigned long long scaled = limit / ((unsigned long long)d * d);
        unsigned long long pairs = counter.count_opposite_parity_pairs(scaled);
        total += (long long)mu[d] * (long long)pairs;
    }
    return (unsigned long long)total;
}

int main(int argc, char** argv) {
    unsigned long long limit = 3141592653589793ULL;
    if (argc > 1) limit = strtoull(argv[1], nullptr, 10);
    cout << P(limit) << '\n';
    return 0;
}
"""


def _binary():
    digest = hashlib.sha256(CPP_SOURCE.encode()).hexdigest()[:16]
    root = Path(tempfile.gettempdir()) / "eulerslop_build"
    root.mkdir(exist_ok=True)
    src = root / f"p540_{digest}.cpp"
    exe = root / f"p540_{digest}"
    if not exe.exists():
        src.write_text(CPP_SOURCE)
        subprocess.run(
            ["g++", "-O3", "-march=native", "-std=c++17", str(src), "-o", str(exe)],
            check=True,
        )
    return exe


def P(limit):
    result = subprocess.run(
        [str(_binary()), str(limit)],
        check=True,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.strip())


def solve():
    assert P(20) == 3
    assert P(10**6) == 159139
    return P(3_141_592_653_589_793)


if __name__ == "__main__":
    print(solve())
