#!/usr/bin/env python3
import hashlib
import subprocess
import tempfile
from pathlib import Path


CPP_SOURCE = r"""
#include <bits/stdc++.h>
using namespace std;

static long long isqrtll(long long x) {
    long long r = (long long)sqrtl((long double)x);
    while ((__int128)(r + 1) * (r + 1) <= x) ++r;
    while ((__int128)r * r > x) --r;
    return r;
}

static vector<int> gaussian_mobius_coefficients(int limit) {
    vector<int> primes;
    vector<int> least_prime(limit + 1, 0);
    vector<int> coeff(limit + 1, 0);
    coeff[1] = 1;

    for (int n = 2; n <= limit; ++n) {
        if (!least_prime[n]) {
            least_prime[n] = n;
            primes.push_back(n);
        }
        for (int p : primes) {
            long long v = (long long)n * p;
            if (v > limit || p > least_prime[n]) break;
            least_prime[(int)v] = p;
        }
    }

    for (int n = 2; n <= limit; ++n) {
        int p = least_prime[n];
        int rest = n / p;
        int exponent = 1;
        while (rest % p == 0) {
            rest /= p;
            ++exponent;
        }

        int local = 0;
        if (p == 2) {
            local = exponent == 1 ? -1 : 0;
        } else if (p % 4 == 1) {
            if (exponent == 1) local = -2;
            else if (exponent == 2) local = 1;
        } else {
            if (exponent == 2) local = -1;
        }

        coeff[n] = coeff[rest] * local;
    }

    return coeff;
}

struct CircleCounter {
    unordered_map<long long, long long> memo;

    long long count_nonzero(long long radius_squared) {
        if (radius_squared <= 0) return 0;

        auto found = memo.find(radius_squared);
        if (found != memo.end()) return found->second;

        long long radius = isqrtll(radius_squared);
        long long total = 2 * radius + 1;
        for (long long x = 1; x <= radius; ++x) {
            long long y = isqrtll(radius_squared - x * x);
            total += 2 * (2 * y + 1);
        }

        --total;  // remove the origin
        memo.emplace(radius_squared, total);
        return total;
    }
};

static long long f(long long limit) {
    int root = (int)isqrtll(limit);
    vector<int> coeff = gaussian_mobius_coefficients(root);

    CircleCounter circles;
    __int128 total = 0;
    for (int norm = 1; norm <= root; ++norm) {
        if (!coeff[norm]) continue;
        long long scaled = limit / ((long long)norm * norm);
        total += (__int128)coeff[norm] * circles.count_nonzero(scaled);
    }

    return (long long)(total / 4);
}

int main(int argc, char** argv) {
    long long limit = 100000000000000LL;
    if (argc > 1) limit = atoll(argv[1]);
    cout << f(limit) << '\n';
    return 0;
}
"""


def _binary():
    digest = hashlib.sha256(CPP_SOURCE.encode()).hexdigest()[:16]
    root = Path(tempfile.gettempdir()) / "eulerslop_build"
    root.mkdir(exist_ok=True)
    src = root / f"p556_{digest}.cpp"
    exe = root / f"p556_{digest}"
    if not exe.exists():
        src.write_text(CPP_SOURCE)
        subprocess.run(
            ["g++", "-O3", "-march=native", "-std=c++17", str(src), "-o", str(exe)],
            check=True,
        )
    return exe


def f(limit):
    result = subprocess.run(
        [str(_binary()), str(limit)],
        check=True,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.strip())


def solve():
    assert f(10) == 7
    assert f(10**2) == 54
    assert f(10**4) == 5218
    assert f(10**8) == 52126906
    return f(10**14)


if __name__ == "__main__":
    print(solve())
