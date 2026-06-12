#!/usr/bin/env python3
import subprocess
from pathlib import Path


CPP = r'''
#include <bits/stdc++.h>
using namespace std;

long long egcd(long long a, long long b, long long &x, long long &y) {
    if (b == 0) {
        x = 1; y = 0;
        return a;
    }
    long long x1, y1;
    long long g = egcd(b, a % b, x1, y1);
    x = y1;
    y = x1 - y1 * (a / b);
    return g;
}

long long invmod(long long a, long long mod) {
    long long x, y;
    egcd((a % mod + mod) % mod, mod, x, y);
    x %= mod;
    if (x < 0) x += mod;
    return x;
}

vector<int> smallest_prime_factors(int n) {
    vector<int> spf(n + 1), primes;
    for (int i = 2; i <= n; ++i) {
        if (!spf[i]) {
            spf[i] = i;
            primes.push_back(i);
        }
        for (int p : primes) {
            long long v = 1LL * p * i;
            if (v > n || p > spf[i]) break;
            spf[(int)v] = p;
        }
    }
    return spf;
}

int I(int n, const vector<int> &spf) {
    int x = n;
    vector<pair<int, int>> factors;
    while (x > 1) {
        int p = spf[x], q = 1;
        while (x % p == 0) {
            x /= p;
            q *= p;
        }
        factors.push_back({p, q});
    }

    vector<pair<int, int>> roots = {{0, 1}};
    for (auto [p, q] : factors) {
        vector<int> local;
        if (p == 2) {
            if (q == 2) local = {1};
            else if (q == 4) local = {1, 3};
            else local = {1, q - 1, 1 + q / 2, q / 2 - 1};
        } else {
            local = {1, q - 1};
        }

        vector<pair<int, int>> next;
        for (auto [a, m] : roots) {
            long long inv = invmod(m, q);
            for (int r : local) {
                long long t = ((r - a) % q + q) % q;
                t = t * inv % q;
                next.push_back({(int)(a + 1LL * m * t), m * q});
            }
        }
        roots.swap(next);
    }

    int best = 1;
    for (auto [r, _] : roots) {
        if (r > 0 && r < n - 1 && r > best) best = r;
    }
    return best;
}

long long solve(int limit) {
    vector<int> spf = smallest_prime_factors(limit);
    assert(I(7, spf) == 1);
    assert(I(15, spf) == 11);
    assert(I(100, spf) == 51);
    long long total = 0;
    for (int n = 3; n <= limit; ++n) {
        total += I(n, spf);
    }
    return total;
}

int main() {
    cout << solve(20000000) << "\n";
}
'''


def _binary():
    src = Path("/tmp/eulerslop_p451.cpp")
    exe = Path("/tmp/eulerslop_p451")
    old = src.read_text() if src.exists() else ""
    if not exe.exists() or old != CPP:
        src.write_text(CPP)
        subprocess.run(
            ["g++", "-O3", "-std=c++17", str(src), "-o", str(exe)],
            check=True,
        )
    return exe


def solve():
    return subprocess.check_output([str(_binary())], text=True).strip()


if __name__ == "__main__":
    print(solve())
