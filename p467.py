#!/usr/bin/env python3
import subprocess
from pathlib import Path


CPP = r'''
#include <bits/stdc++.h>
using namespace std;

const int MOD = 1000000007;

int digital_root(int x) {
    int r = x % 9;
    return r ? r : 9;
}

vector<unsigned char> sequence(int n, bool want_prime) {
    int limit = 300000;
    vector<char> is_prime(limit + 1, true);
    is_prime[0] = is_prime[1] = false;
    for (int p = 2; p * p <= limit; ++p) {
        if (is_prime[p]) {
            for (long long q = 1LL * p * p; q <= limit; q += p) {
                is_prime[(int)q] = false;
            }
        }
    }
    vector<unsigned char> out;
    out.reserve(n);
    for (int x = 2; (int)out.size() < n && x <= limit; ++x) {
        if ((bool)is_prime[x] == want_prime) {
            out.push_back((unsigned char)digital_root(x));
        }
    }
    return out;
}

long long solve(int n) {
    vector<unsigned char> p = sequence(n, true);
    vector<unsigned char> c = sequence(n, false);
    int w = n + 1;
    vector<unsigned short> dp(1LL * w * w);

    for (int i = 0; i <= n; ++i) dp[1LL * i * w + n] = n - i;
    for (int j = 0; j <= n; ++j) dp[1LL * n * w + j] = n - j;

    for (int i = n - 1; i >= 0; --i) {
        long long row = 1LL * i * w;
        long long next = 1LL * (i + 1) * w;
        for (int j = n - 1; j >= 0; --j) {
            if (p[i] == c[j]) {
                dp[row + j] = 1 + dp[next + j + 1];
            } else {
                dp[row + j] = 1 + min(dp[next + j], dp[row + j + 1]);
            }
        }
    }

    int i = 0, j = 0;
    long long answer = 0;
    while (i < n || j < n) {
        unsigned short cur = dp[1LL * i * w + j];
        int digit = -1, ni = -1, nj = -1;
        for (int d = 1; d <= 9 && digit < 0; ++d) {
            if (i < n && j < n && p[i] == d && c[j] == d
                    && 1 + dp[1LL * (i + 1) * w + j + 1] == cur) {
                digit = d; ni = i + 1; nj = j + 1;
            } else if (i < n && p[i] == d
                    && 1 + dp[1LL * (i + 1) * w + j] == cur) {
                digit = d; ni = i + 1; nj = j;
            } else if (j < n && c[j] == d
                    && 1 + dp[1LL * i * w + j + 1] == cur) {
                digit = d; ni = i; nj = j + 1;
            }
        }
        answer = (answer * 10 + digit) % MOD;
        i = ni; j = nj;
    }
    return answer;
}

int main() {
    cout << solve(10000) << "\n";
}
'''


def _binary():
    src = Path("/tmp/eulerslop_p467.cpp")
    exe = Path("/tmp/eulerslop_p467")
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
