#!/usr/bin/env python3

import subprocess
import tempfile
from pathlib import Path


SOURCE = r"""
#include <bits/stdc++.h>
using namespace std;

using i128 = __int128_t;

struct Vec {
    i128 a[3];
};

static inline i128 abs128(i128 x) {
    return x < 0 ? -x : x;
}

static inline i128 norm(const Vec& v) {
    return abs128(v.a[0]) + abs128(v.a[1]) + abs128(v.a[2]);
}

static inline Vec addmul(const Vec& v, const Vec& u, long long k) {
    return Vec{{v.a[0] + (i128)k * u.a[0],
                v.a[1] + (i128)k * u.a[1],
                v.a[2] + (i128)k * u.a[2]}};
}

static inline long long floor_div(i128 a, i128 b) {
    if (b < 0) {
        a = -a;
        b = -b;
    }
    if (a >= 0) return (long long)(a / b);
    return (long long)(-((-a + b - 1) / b));
}

static pair<long long, i128> best_shift(const Vec& v, const Vec& u) {
    long long candidates[64];
    int count = 0;
    candidates[count++] = 0;

    for (int i = 0; i < 3; ++i) {
        if (u.a[i] == 0) continue;
        long long q = floor_div(-v.a[i], u.a[i]);
        for (long long d = -6; d <= 6; ++d) {
            candidates[count++] = q + d;
        }
    }

    long long best_k = 0;
    i128 best_norm = norm(v);
    for (int i = 0; i < count; ++i) {
        long long k = candidates[i];
        i128 candidate_norm = norm(addmul(v, u, k));
        if (candidate_norm < best_norm) {
            best_norm = candidate_norm;
            best_k = k;
        }
    }

    return {best_k, best_norm};
}

static i128 shortest(Vec u, Vec v) {
    for (int iteration = 0; iteration < 100; ++iteration) {
        if (norm(v) < norm(u)) swap(u, v);
        auto [k, shifted_norm] = best_shift(v, u);
        if (k == 0) return norm(u);
        v = addmul(v, u, k);
    }
    return min(norm(u), norm(v));
}

static string to_string128(i128 value) {
    if (value == 0) return "0";
    string text;
    while (value > 0) {
        text.push_back(char('0' + value % 10));
        value /= 10;
    }
    reverse(text.begin(), text.end());
    return text;
}

struct Tribonacci {
    static const int MOD = 10000000;
    long long r0 = 0;
    long long r1 = 0;
    long long r2 = 1;
    long long index = 0;

    long long next() {
        ++index;
        if (index == 1) return 0;
        if (index == 2) return 1;
        long long value = (r0 + r1 + r2) % MOD;
        r0 = r1;
        r1 = r2;
        r2 = value;
        return value;
    }
};

static i128 solve_limit(int limit) {
    Tribonacci tribonacci;
    i128 total = 0;

    for (int n = 1; n <= limit; ++n) {
        long long r[13];
        for (int i = 1; i <= 12; ++i) {
            r[i] = tribonacci.next();
        }

        Vec v{{r[1] - r[2], r[3] + r[4], (i128)r[5] * r[6]}};
        Vec w{{r[7] - r[8], r[9] + r[10], (i128)r[11] * r[12]}};
        total += shortest(v, w);
    }

    return total;
}

int main(int argc, char** argv) {
    for (int i = 1; i < argc; ++i) {
        cout << to_string128(solve_limit(atoi(argv[i]))) << '\n';
    }
    return 0;
}
"""


def run_limits(*limits):
    with tempfile.TemporaryDirectory(prefix="p507_") as tmp:
        tmp_path = Path(tmp)
        cpp = tmp_path / "p507.cpp"
        exe = tmp_path / "p507"
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
    sample, answer = run_limits(10, 20_000_000)
    assert sample == "130762273722"
    return answer


if __name__ == "__main__":
    print(solve())
