#!/usr/bin/env python3

import subprocess
import tempfile
from pathlib import Path


SOURCE = r"""
#include <bits/stdc++.h>
using namespace std;

static const uint32_t MOD = 1000000993U;

struct SegmentTree {
    int n;
    int size;
    vector<uint32_t> sum;
    vector<uint32_t> lazy;

    explicit SegmentTree(int n_) : n(n_) {
        size = 1;
        while (size < n) size <<= 1;
        sum.assign(2 * size, 0);
        lazy.assign(2 * size, 1);
        for (int i = 0; i < n; ++i) sum[size + i] = 1;
        for (int i = size - 1; i > 0; --i) {
            sum[i] = (sum[i << 1] + sum[i << 1 | 1]) % MOD;
        }
    }

    void apply(int node, uint32_t factor) {
        sum[node] = (uint64_t)sum[node] * factor % MOD;
        lazy[node] = (uint64_t)lazy[node] * factor % MOD;
    }

    void push(int node) {
        if (lazy[node] == 1) return;
        uint32_t factor = lazy[node];
        apply(node << 1, factor);
        apply(node << 1 | 1, factor);
        lazy[node] = 1;
    }

    void suffix_multiply(int node, int left, int right, int query_left, uint32_t factor) {
        if (right <= query_left) return;
        if (query_left <= left) {
            apply(node, factor);
            return;
        }
        push(node);
        int mid = (left + right) >> 1;
        suffix_multiply(node << 1, left, mid, query_left, factor);
        suffix_multiply(node << 1 | 1, mid, right, query_left, factor);
        sum[node] = (sum[node << 1] + sum[node << 1 | 1]) % MOD;
    }

    void suffix_multiply(int prime, uint32_t factor) {
        if (factor != 1) suffix_multiply(1, 0, size, prime - 1, factor);
    }

    uint32_t total() const {
        return sum[1];
    }
};

uint32_t solve_limit(int limit) {
    vector<int> spf(limit + 1);
    vector<int> primes;
    primes.reserve(limit / 10);

    for (int i = 2; i <= limit; ++i) {
        if (spf[i] == 0) {
            spf[i] = i;
            primes.push_back(i);
        }
        for (int p : primes) {
            long long v = 1LL * p * i;
            if (v > limit) break;
            spf[v] = p;
            if (p == spf[i]) break;
        }
    }

    vector<uint32_t> inverse(limit + 1);
    inverse[1] = 1;
    for (int i = 2; i <= limit; ++i) {
        inverse[i] = (uint64_t)(MOD - MOD / i) * inverse[MOD % i] % MOD;
    }

    SegmentTree tree(limit);
    uint64_t answer = tree.total();

    auto apply_factorization = [&](int value, bool numerator) {
        while (value > 1) {
            int p = spf[value];
            uint64_t factor = 1;
            uint32_t base = numerator ? (uint32_t)p : inverse[p];
            while (value % p == 0) {
                value /= p;
                factor = factor * base % MOD;
            }
            tree.suffix_multiply(p, (uint32_t)factor);
        }
    };

    for (int r = 0; r < limit; ++r) {
        apply_factorization(limit - r, true);
        apply_factorization(r + 1, false);
        answer += tree.total();
        if (answer >= (uint64_t)MOD * MOD) answer %= MOD;
    }

    return answer % MOD;
}

int main(int argc, char** argv) {
    for (int i = 1; i < argc; ++i) {
        cout << solve_limit(atoi(argv[i])) << '\n';
    }
    return 0;
}
"""


def run_limits(*limits):
    with tempfile.TemporaryDirectory(prefix="p468_") as tmp:
        tmp_path = Path(tmp)
        cpp = tmp_path / "p468.cpp"
        exe = tmp_path / "p468"
        cpp.write_text(SOURCE)
        subprocess.run(
            ["g++", "-O3", "-std=c++17", str(cpp), "-o", str(exe)],
            check=True,
        )
        result = subprocess.run(
            [str(exe), *(str(limit) for limit in limits)],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        )
    return result.stdout.strip().splitlines()


def solve():
    sample_11, sample_1111, sample_111111, answer = run_limits(
        11, 1111, 111_111, 11_111_111
    )
    assert sample_11 == "3132"
    assert sample_1111 == "706036312"
    assert sample_111111 == "22156169"
    return answer


if __name__ == "__main__":
    print(solve())
