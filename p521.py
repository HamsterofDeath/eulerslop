#!/usr/bin/env python3
import hashlib
import subprocess
import tempfile
from pathlib import Path


CPP_SOURCE = r"""
#include <bits/stdc++.h>
using namespace std;

static const long long MOD = 1000000000LL;

struct PrimeData {
    int limit;
    vector<int> primes;
    vector<int> pi_small;
    vector<long long> prefix_mod;

    explicit PrimeData(int n) : limit(n), pi_small(n + 1, 0) {
        vector<unsigned char> composite(n + 1, 0);
        for (int i = 2; i <= n; ++i) {
            if (!composite[i]) {
                primes.push_back(i);
                if ((long long)i * i <= n) {
                    for (long long j = (long long)i * i; j <= n; j += i) {
                        composite[(size_t)j] = 1;
                    }
                }
            }
            pi_small[i] = (int)primes.size();
        }

        prefix_mod.assign(primes.size() + 1, 0);
        for (size_t i = 0; i < primes.size(); ++i) {
            prefix_mod[i + 1] = (prefix_mod[i] + primes[i]) % MOD;
        }
    }
};

struct PrimeTable {
    unsigned long long n;
    int root;
    vector<unsigned long long> vals;
    vector<long long> prime_count;
    vector<long long> prime_sum_mod;
    vector<int> id_small;
    vector<int> id_large;

    PrimeTable(unsigned long long n_, const PrimeData& pd) : n(n_) {
        root = (int)sqrtl((long double)n);
        while ((unsigned long long)(root + 1) * (root + 1) <= n) ++root;
        while ((unsigned long long)root * root > n) --root;

        id_small.assign(root + 2, -1);
        id_large.assign(root + 2, -1);

        for (unsigned long long l = 1, r; l <= n; l = r + 1) {
            unsigned long long v = n / l;
            r = n / v;

            int index = (int)vals.size();
            vals.push_back(v);
            if (v <= (unsigned long long)root) {
                id_small[(int)v] = index;
            } else {
                id_large[(int)(n / v)] = index;
            }

            prime_count.push_back((long long)v - 1);

            unsigned long long a = v;
            unsigned long long b = v + 1;
            if ((a & 1ULL) == 0) {
                a >>= 1;
            } else {
                b >>= 1;
            }
            long long triangular =
                (long long)((__int128)(a % MOD) * (b % MOD) % MOD);
            prime_sum_mod.push_back((triangular - 1 + MOD) % MOD);
        }

        for (size_t j = 0; j < pd.primes.size(); ++j) {
            long long p = pd.primes[j];
            if (p * p > (long long)n) break;

            long long previous_count = (long long)j;
            long long previous_sum = pd.prefix_mod[j];
            unsigned long long square = (unsigned long long)p * p;

            for (size_t i = 0; i < vals.size() && vals[i] >= square; ++i) {
                unsigned long long v = vals[i];
                int quotient_id = id(v / p);

                prime_count[i] -= prime_count[quotient_id] - previous_count;

                long long remaining_sum =
                    (prime_sum_mod[quotient_id] - previous_sum) % MOD;
                if (remaining_sum < 0) remaining_sum += MOD;
                prime_sum_mod[i] =
                    (prime_sum_mod[i] - (p % MOD) * remaining_sum) % MOD;
                if (prime_sum_mod[i] < 0) prime_sum_mod[i] += MOD;
            }
        }
    }

    int id(unsigned long long x) const {
        if (x <= (unsigned long long)root) return id_small[(int)x];
        return id_large[(int)(n / x)];
    }

    long long pi(unsigned long long x) const {
        return prime_count[id(x)];
    }

    long long sum_primes(unsigned long long x) const {
        return prime_sum_mod[id(x)];
    }
};

struct PhiCounter {
    static const int BASE = 6;

    const vector<int>& primes;
    unordered_map<unsigned long long, unsigned long long> memo;
    array<vector<int>, BASE + 1> table;
    array<int, BASE + 1> period{};

    explicit PhiCounter(const vector<int>& prime_list) : primes(prime_list) {
        period[0] = 1;
        for (int s = 1; s <= BASE; ++s) {
            period[s] = period[s - 1] * primes[s - 1];
        }

        for (int s = 0; s <= BASE; ++s) {
            table[s].assign(period[s], 0);
            for (int i = 0; i < period[s]; ++i) {
                int count = 0;
                for (int k = 1; k <= i; ++k) {
                    bool coprime = true;
                    for (int j = 0; j < s; ++j) {
                        if (k % primes[j] == 0) {
                            coprime = false;
                            break;
                        }
                    }
                    if (coprime) ++count;
                }
                table[s][i] = count;
            }
        }

        memo.reserve(5000000);
    }

    unsigned long long phi(unsigned long long x, int s) {
        if (s == 0) return x;
        if (s <= BASE) {
            unsigned long long quotient = x / period[s];
            int remainder = (int)(x % period[s]);
            return quotient * (unsigned long long)table[s][period[s] - 1]
                + (unsigned long long)table[s][remainder];
        }
        if (x <= 1) return x;

        unsigned long long key = (x << 16) ^ (unsigned long long)s;
        auto found = memo.find(key);
        if (found != memo.end()) return found->second;

        unsigned long long answer =
            phi(x, s - 1) - phi(x / (unsigned long long)primes[s - 1], s - 1);
        memo.emplace(key, answer);
        return answer;
    }
};

static unsigned long long integer_cuberoot(unsigned long long n) {
    unsigned long long low = 0;
    unsigned long long high = 2000000;
    while (low + 1 < high) {
        unsigned long long mid = (low + high) / 2;
        if ((__int128)mid * mid * mid <= n) {
            low = mid;
        } else {
            high = mid;
        }
    }
    return low;
}

static long long S(unsigned long long n) {
    int root = (int)sqrtl((long double)n);
    while ((unsigned long long)(root + 1) * (root + 1) <= n) ++root;
    while ((unsigned long long)root * root > n) --root;

    PrimeData pd(root);
    PrimeTable prime_table(n, pd);
    PhiCounter phi_counter(pd.primes);
    unsigned long long cube_root = integer_cuberoot(n);

    long long answer = prime_table.sum_primes(n) % MOD;
    for (size_t index = 0; index < pd.primes.size(); ++index) {
        unsigned long long p = pd.primes[index];
        if (p * p > n) break;

        unsigned long long extra_count;
        if (p <= cube_root) {
            extra_count = phi_counter.phi(n / p, (int)index) - 1;
        } else {
            extra_count =
                (unsigned long long)(prime_table.pi(n / p) - (long long)index);
        }

        answer = (answer
            + (long long)((__int128)(p % MOD) * (extra_count % MOD) % MOD))
            % MOD;
    }
    return answer;
}

int main(int argc, char** argv) {
    unsigned long long limit = 1000000000000ULL;
    if (argc > 1) limit = strtoull(argv[1], nullptr, 10);
    cout << S(limit) << '\n';
    return 0;
}
"""


def _binary():
    digest = hashlib.sha256(CPP_SOURCE.encode()).hexdigest()[:16]
    root = Path(tempfile.gettempdir()) / "eulerslop_build"
    root.mkdir(exist_ok=True)
    src = root / f"p521_{digest}.cpp"
    exe = root / f"p521_{digest}"
    if not exe.exists():
        src.write_text(CPP_SOURCE)
        subprocess.run(
            ["g++", "-O3", "-march=native", "-std=c++17", str(src), "-o", str(exe)],
            check=True,
        )
    return exe


def S(limit):
    result = subprocess.run(
        [str(_binary()), str(limit)],
        check=True,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.strip())


def solve():
    assert S(100) == 1257
    return S(10**12)


if __name__ == "__main__":
    print(solve())
