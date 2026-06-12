#!/usr/bin/env python3
import hashlib
import subprocess
import tempfile
from pathlib import Path


CPP_SOURCE = r"""
#include <cmath>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>

static constexpr int PRIME_MOD = 10007;

static int mod_pow(long long base, long long exponent) {
    long long result = 1;
    base %= PRIME_MOD;
    while (exponent) {
        if (exponent & 1) result = result * base % PRIME_MOD;
        base = base * base % PRIME_MOD;
        exponent >>= 1;
    }
    return (int)result;
}

static std::vector<int> first_primes(int count) {
    int limit = count < 6 ? 15 : (int)(count * (std::log(count) + std::log(std::log(count))) + 10);
    while (true) {
        std::vector<unsigned char> is_prime((size_t)limit + 1, 1);
        is_prime[0] = is_prime[1] = 0;
        for (int p = 2; (long long)p * p <= limit; ++p) {
            if (is_prime[p]) {
                for (long long q = (long long)p * p; q <= limit; q += p) {
                    is_prime[(size_t)q] = 0;
                }
            }
        }

        std::vector<int> primes;
        primes.reserve(count);
        for (int p = 2; p <= limit && (int)primes.size() < count; ++p) {
            if (is_prime[p]) primes.push_back(p);
        }
        if ((int)primes.size() >= count) return primes;
        limit *= 2;
    }
}

struct Fenwick {
    int n;
    std::vector<int> tree;

    explicit Fenwick(int size) : n(size), tree(size + 1) {}

    void add(int index, int value) {
        for (++index; index <= n; index += index & -index) tree[index] += value;
    }

    int kth(int k) const {
        int index = 0;
        int bit = 1;
        while ((bit << 1) <= n) bit <<= 1;
        for (; bit; bit >>= 1) {
            int next = index + bit;
            if (next <= n && tree[next] < k) {
                index = next;
                k -= tree[next];
            }
        }
        return index;
    }
};

static std::string F(int n, int window) {
    auto primes = first_primes(n);
    std::vector<int> s(n + 1), s2(n + 1);
    for (int i = 1; i <= n; ++i) s[i] = mod_pow(primes[i - 1], i);
    for (int i = 1; i <= n; ++i) s2[i] = s[i] + s[i / 10000 + 1];

    Fenwick counts(20015);
    long long twice_sum = 0;
    for (int i = 1; i <= n; ++i) {
        counts.add(s2[i], 1);
        if (i > window) counts.add(s2[i - window], -1);
        if (i >= window) {
            if (window % 2) {
                twice_sum += 2LL * counts.kth(window / 2 + 1);
            } else {
                twice_sum += (long long)counts.kth(window / 2) + counts.kth(window / 2 + 1);
            }
        }
    }

    return std::to_string(twice_sum / 2) + (twice_sum % 2 ? ".5" : ".0");
}

int main(int argc, char** argv) {
    int n = argc > 1 ? std::stoi(argv[1]) : 10000000;
    int window = argc > 2 ? std::stoi(argv[2]) : 100000;
    std::cout << F(n, window) << '\n';
    return 0;
}
"""


def _binary():
    digest = hashlib.sha256(CPP_SOURCE.encode()).hexdigest()[:16]
    root = Path(tempfile.gettempdir()) / "eulerslop_build"
    root.mkdir(exist_ok=True)
    src = root / f"p593_{digest}.cpp"
    exe = root / f"p593_{digest}"
    if not exe.exists():
        src.write_text(CPP_SOURCE)
        subprocess.run(
            ["g++", "-O3", "-march=native", "-std=c++17", str(src), "-o", str(exe)],
            check=True,
        )
    return exe


def F(n, window):
    result = subprocess.run(
        [str(_binary()), str(n), str(window)],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def solve():
    assert F(100, 10) == "463628.5"
    assert F(100_000, 10_000) == "675348207.5"
    return F(10_000_000, 100_000)


if __name__ == "__main__":
    print(solve())
