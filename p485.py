#!/usr/bin/env python3
import subprocess
from pathlib import Path


CPP = r'''
#include <bits/stdc++.h>
using namespace std;

unsigned long long S(int u, int k) {
    vector<unsigned short> divisors(u + 1);
    for (int d = 1; d <= u; ++d) {
        for (int m = d; m <= u; m += d) {
            ++divisors[m];
        }
    }

    deque<int> window;
    unsigned long long total = 0;
    for (int i = 1; i <= u; ++i) {
        while (!window.empty() && divisors[window.back()] <= divisors[i]) {
            window.pop_back();
        }
        window.push_back(i);
        int start = i - k + 1;
        if (window.front() < start) {
            window.pop_front();
        }
        if (i >= k) {
            total += divisors[window.front()];
        }
    }
    return total;
}

int main() {
    assert(S(1000, 10) == 17176);
    cout << S(100000000, 100000) << "\n";
}
'''


def _binary():
    src = Path("/tmp/eulerslop_p485.cpp")
    exe = Path("/tmp/eulerslop_p485")
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
