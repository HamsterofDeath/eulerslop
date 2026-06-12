#!/usr/bin/env python3
import hashlib
import subprocess
import tempfile
from pathlib import Path


CPP_SOURCE = r"""
#include <bits/stdc++.h>
using namespace std;

static const int MOD = 1000000007;
static const int WINDOW_MASK = (1 << 11) - 1;

static int transition_state(int state, int digit) {
    int all_prefixes = state & WINDOW_MASK;
    int covered_prefixes = (state >> 11) & WINDOW_MASK;

    int shifted_covered = (covered_prefixes << digit) & WINDOW_MASK;
    int shifted_all = (all_prefixes << digit) & WINDOW_MASK;
    bool covered_now = (shifted_covered >> 10) & 1;
    shifted_all |= 1;

    if (covered_now) {
        return (1 << 22) | (shifted_all << 11) | shifted_all;
    }
    return (shifted_covered << 11) | shifted_all;
}

static vector<int> berlekamp_massey(const vector<int>& sequence) {
    auto mod_pow = [](long long a, long long e) {
        long long r = 1;
        while (e) {
            if (e & 1LL) r = r * a % MOD;
            a = a * a % MOD;
            e >>= 1LL;
        }
        return r;
    };

    vector<long long> C(1, 1), B(1, 1);
    int length = 0;
    int shift = 1;
    long long last_discrepancy = 1;

    for (int n = 0; n < (int)sequence.size(); ++n) {
        long long discrepancy = sequence[n];
        for (int i = 1; i <= length; ++i) {
            discrepancy = (discrepancy + C[i] * sequence[n - i]) % MOD;
        }

        if (discrepancy == 0) {
            ++shift;
            continue;
        }

        vector<long long> old_C = C;
        long long coefficient =
            discrepancy * mod_pow(last_discrepancy, MOD - 2) % MOD;
        if (C.size() < B.size() + shift) C.resize(B.size() + shift, 0);

        for (int j = 0; j < (int)B.size(); ++j) {
            C[j + shift] = (C[j + shift] - coefficient * B[j]) % MOD;
            if (C[j + shift] < 0) C[j + shift] += MOD;
        }

        if (2 * length <= n) {
            length = n + 1 - length;
            B = old_C;
            last_discrepancy = discrepancy;
            shift = 1;
        } else {
            ++shift;
        }
    }

    vector<int> recurrence;
    for (size_t i = 1; i < C.size(); ++i) {
        recurrence.push_back((MOD - (int)C[i]) % MOD);
    }
    return recurrence;
}

static vector<int> combine(
    const vector<int>& a,
    const vector<int>& b,
    const vector<int>& recurrence
) {
    int k = (int)recurrence.size();
    vector<long long> tmp(2 * k, 0);

    for (int i = 0; i < k; ++i) {
        if (!a[i]) continue;
        for (int j = 0; j < k; ++j) {
            if (b[j]) tmp[i + j] = (tmp[i + j] + (long long)a[i] * b[j]) % MOD;
        }
    }

    for (int i = 2 * k - 2; i >= k; --i) {
        if (!tmp[i]) continue;
        for (int j = 0; j < k; ++j) {
            tmp[i - 1 - j] = (tmp[i - 1 - j] + tmp[i] * recurrence[j]) % MOD;
        }
    }

    vector<int> reduced(k);
    for (int i = 0; i < k; ++i) reduced[i] = (int)tmp[i];
    return reduced;
}

static int linear_recurrence_value(
    const vector<int>& recurrence,
    const vector<int>& initial,
    unsigned long long n
) {
    int k = (int)recurrence.size();
    if (n <= initial.size()) return initial[(size_t)n - 1];

    vector<int> polynomial(k, 0), power_polynomial(k, 0);
    polynomial[0] = 1;
    if (k == 1) {
        power_polynomial[0] = recurrence[0];
    } else {
        power_polynomial[1] = 1;
    }

    unsigned long long exponent = n - 1;
    while (exponent) {
        if (exponent & 1ULL) {
            polynomial = combine(polynomial, power_polynomial, recurrence);
        }
        power_polynomial = combine(power_polynomial, power_polynomial, recurrence);
        exponent >>= 1ULL;
    }

    long long answer = 0;
    for (int i = 0; i < k; ++i) {
        answer = (answer + (long long)polynomial[i] * initial[i]) % MOD;
    }
    return (int)answer;
}

struct Solver {
    vector<int> recurrence;
    vector<int> initial;

    Solver() {
        int start = (1 << 22) | (1 << 11) | 1;
        unordered_map<int, int> id;
        vector<int> states;
        queue<int> pending;

        for (int digit = 1; digit <= 9; ++digit) {
            int state = transition_state(start, digit);
            if (!id.count(state)) {
                id[state] = (int)states.size();
                states.push_back(state);
                pending.push(state);
            }
        }

        while (!pending.empty()) {
            int state = pending.front();
            pending.pop();
            for (int digit = 0; digit <= 9; ++digit) {
                int next = transition_state(state, digit);
                if (!id.count(next)) {
                    id[next] = (int)states.size();
                    states.push_back(next);
                    pending.push(next);
                }
            }
        }

        int state_count = (int)states.size();
        vector<vector<pair<int, int>>> transitions(state_count);
        for (int i = 0; i < state_count; ++i) {
            map<int, int> counts;
            for (int digit = 0; digit <= 9; ++digit) {
                ++counts[id[transition_state(states[i], digit)]];
            }
            for (auto [next, count] : counts) transitions[i].push_back({next, count});
        }

        vector<int> accepting(state_count);
        for (int i = 0; i < state_count; ++i) accepting[i] = states[i] >> 22;

        vector<int> current(state_count, 0);
        for (int digit = 1; digit <= 9; ++digit) {
            ++current[id[transition_state(start, digit)]];
        }

        int terms = 2 * (state_count + 1) + 20;
        vector<int> sequence;
        sequence.reserve(terms);
        long long total = 0;

        for (int length = 1; length <= terms; ++length) {
            long long exact = 0;
            for (int i = 0; i < state_count; ++i) {
                if (accepting[i]) exact += current[i];
            }
            total = (total + exact) % MOD;
            sequence.push_back((int)total);

            vector<int> next(state_count, 0);
            for (int i = 0; i < state_count; ++i) {
                if (!current[i]) continue;
                for (auto [j, count] : transitions[i]) {
                    next[j] = (next[j] + (long long)current[i] * count) % MOD;
                }
            }
            current.swap(next);
        }

        recurrence = berlekamp_massey(sequence);
        initial.assign(sequence.begin(), sequence.begin() + recurrence.size());
    }

    int value(unsigned long long n) const {
        return linear_recurrence_value(recurrence, initial, n);
    }
};

int main(int argc, char** argv) {
    Solver solver;
    if (argc > 1) {
        cout << solver.value(strtoull(argv[1], nullptr, 10)) << '\n';
        return 0;
    }

    if (solver.value(2) != 9 || solver.value(5) != 3492) return 1;
    cout << solver.value(1000000000000000000ULL) << '\n';
    return 0;
}
"""


def _binary():
    digest = hashlib.sha256(CPP_SOURCE.encode()).hexdigest()[:16]
    root = Path(tempfile.gettempdir()) / "eulerslop_build"
    root.mkdir(exist_ok=True)
    src = root / f"p529_{digest}.cpp"
    exe = root / f"p529_{digest}"
    if not exe.exists():
        src.write_text(CPP_SOURCE)
        subprocess.run(
            ["g++", "-O3", "-march=native", "-std=c++17", str(src), "-o", str(exe)],
            check=True,
        )
    return exe


def T(limit):
    result = subprocess.run(
        [str(_binary()), str(limit)],
        check=True,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.strip())


def solve():
    result = subprocess.run(
        [str(_binary())],
        check=True,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.strip())


if __name__ == "__main__":
    print(solve())
