#!/usr/bin/env python3

import subprocess
import tempfile
from pathlib import Path


SOURCE = r"""
#include <bits/stdc++.h>
using namespace std;

using i64 = long long;
static const int SIEVE_LIMIT = 5000000;
static const int PHI_N = 100000;
static const int PHI_M = 100;

vector<int> primes;
vector<int> prime_pi;
int phi_table[PHI_M][PHI_N];
unordered_map<unsigned long long, i64> phi_cache;
unordered_map<i64, i64> lehmer_cache;

i64 isqrt64(i64 x) {
    i64 r = sqrt((long double)x);
    while ((r + 1) <= x / (r + 1)) ++r;
    while (r > x / r) --r;
    return r;
}

i64 icbrt64(i64 x) {
    i64 r = cbrt((long double)x);
    while ((r + 1) <= x / ((r + 1) * (r + 1))) ++r;
    while (r > x / (r * r)) --r;
    return r;
}

i64 iroot4(i64 x) {
    i64 r = sqrt(sqrt((long double)x));
    auto ok = [&](i64 y) {
        __int128 z = y;
        z *= y;
        z *= y;
        z *= y;
        return z <= x;
    };
    while (ok(r + 1)) ++r;
    while (!ok(r)) --r;
    return r;
}

void initialize() {
    vector<bool> sieve(SIEVE_LIMIT + 1, true);
    sieve[0] = sieve[1] = false;
    for (int i = 2; i * i <= SIEVE_LIMIT; ++i) {
        if (!sieve[i]) continue;
        for (long long j = 1LL * i * i; j <= SIEVE_LIMIT; j += i) sieve[(int)j] = false;
    }

    prime_pi.assign(SIEVE_LIMIT + 1, 0);
    int count = 0;
    for (int i = 0; i <= SIEVE_LIMIT; ++i) {
        if (sieve[i]) {
            primes.push_back(i);
            ++count;
        }
        prime_pi[i] = count;
    }

    for (int n = 0; n < PHI_N; ++n) phi_table[0][n] = n;
    for (int m = 1; m < PHI_M; ++m) {
        int p = primes[m - 1];
        for (int n = 0; n < PHI_N; ++n) {
            phi_table[m][n] = phi_table[m - 1][n] - phi_table[m - 1][n / p];
        }
    }
}

i64 phi(i64 x, int s) {
    if (s == 0) return x;
    if (s < PHI_M && x < PHI_N) return phi_table[s][x];
    if (s == 1) return x - x / 2;

    if (s >= PHI_M) {
        unsigned long long key = ((unsigned long long)x << 20) | (unsigned int)s;
        auto found = phi_cache.find(key);
        if (found != phi_cache.end()) return found->second;

        i64 result = phi(x, PHI_M - 1);
        for (int i = PHI_M - 1; i < s; ++i) {
            result -= phi(x / primes[i], i);
        }
        phi_cache[key] = result;
        return result;
    }

    return phi(x, s - 1) - phi(x / primes[s - 1], s - 1);
}

i64 lehmer_pi(i64 x) {
    if (x < SIEVE_LIMIT) return prime_pi[x];
    auto found = lehmer_cache.find(x);
    if (found != lehmer_cache.end()) return found->second;

    i64 a = lehmer_pi(iroot4(x));
    i64 b = lehmer_pi(isqrt64(x));
    i64 c = lehmer_pi(icbrt64(x));

    i64 result = phi(x, (int)a) + (b + a - 2) * (b - a + 1) / 2;
    for (i64 i = a; i < b; ++i) {
        i64 w = x / primes[i];
        result -= lehmer_pi(w);
        if (i < c) {
            i64 limit = lehmer_pi(isqrt64(w));
            for (i64 j = i; j < limit; ++j) {
                result -= lehmer_pi(w / primes[j]) - j;
            }
        }
    }

    lehmer_cache[x] = result;
    return result;
}

i64 squarefree_tail(i64 limit, int start_prime_index) {
    if (limit < 1) return 0;

    i64 prime_count = lehmer_pi(limit) - start_prime_index;
    i64 total = 1 + max<i64>(0, prime_count);

    i64 root = isqrt64(limit);
    for (int i = start_prime_index; i < (int)primes.size() && primes[i] <= root; ++i) {
        total += squarefree_tail(limit / primes[i], i + 1) - 1;
    }
    return total;
}

i64 count_decreasing_prime_powers(i64 limit) {
    i64 total = squarefree_tail(limit, 0);
    int max_exp = 0;
    for (i64 power = 2; power <= limit; power *= 2) ++max_exp;

    function<void(int, int, i64, int)> dfs = [&](int start, int max_allowed_exp, i64 product, int last_index) {
        total += squarefree_tail(limit / product, last_index + 1);
        i64 remaining = limit / product;

        for (int i = start; i < (int)primes.size() && 1LL * primes[i] * primes[i] <= remaining; ++i) {
            i64 prime = primes[i];
            i64 value = prime * prime;
            for (int exponent = 2; exponent <= max_allowed_exp && value <= remaining; ++exponent) {
                dfs(i + 1, exponent, product * value, i);
                if (value > remaining / prime) break;
                value *= prime;
            }
        }
    };

    for (int i = 0; i < (int)primes.size() && 1LL * primes[i] * primes[i] <= limit; ++i) {
        i64 prime = primes[i];
        i64 value = prime * prime;
        for (int exponent = 2; exponent <= max_exp && value <= limit; ++exponent) {
            dfs(i + 1, exponent, value, i);
            if (value > limit / prime) break;
            value *= prime;
        }
    }

    return total;
}

int main() {
    initialize();
    cout << count_decreasing_prime_powers(100) << '\n';
    cout << count_decreasing_prime_powers(1000000) << '\n';
    cout << count_decreasing_prime_powers(10000000000000LL) << '\n';
    return 0;
}
"""


def run_solver():
    with tempfile.TemporaryDirectory(prefix="p578_") as tmp:
        tmp_path = Path(tmp)
        cpp = tmp_path / "p578.cpp"
        exe = tmp_path / "p578"
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
    return result.stdout.strip().splitlines()


def solve():
    sample_100, sample_million, answer = run_solver()
    assert sample_100 == "94"
    assert sample_million == "922052"
    return answer


if __name__ == "__main__":
    print(solve())
