#!/usr/bin/env python3

import subprocess
import tempfile
from pathlib import Path


SOURCE = r"""
#include <bits/stdc++.h>
using namespace std;

using i128 = __int128_t;
using u64 = unsigned long long;

struct Candidate {
    u64 maximum_term;
    u64 sum;
};

string to_string128(i128 value) {
    if (value == 0) return "0";
    bool negative = value < 0;
    if (negative) value = -value;
    string text;
    while (value > 0) {
        text.push_back(char('0' + value % 10));
        value /= 10;
    }
    if (negative) text.push_back('-');
    reverse(text.begin(), text.end());
    return text;
}

vector<Candidate> make_candidates(u64 limit) {
    vector<Candidate> candidates;

    for (u64 p = 2; p * p <= limit && p * p < 6264ULL; ++p) {
        u64 maximum_term = p * p;
        u64 sum = p * p * p - (p - 1) * (p - 1) * (p - 1);
        candidates.push_back({maximum_term, sum});
    }

    for (u64 p = 2; p * p * p <= limit && p * p * p < 430000ULL; ++p) {
        u64 maximum_term = p * p * p;
        u64 sum = p * p * p * p - (p - 1) * (p - 1) * (p - 1) * (p - 1);
        candidates.push_back({maximum_term, sum});
    }

    for (u64 p = 2;; ++p) {
        __uint128_t maximum_term = (__uint128_t)p * p * p * p;
        if (maximum_term > limit) break;

        int exponent = 4;
        while (maximum_term <= limit) {
            __uint128_t high = 1;
            __uint128_t low = 1;
            for (int i = 0; i <= exponent; ++i) {
                high *= p;
                low *= p - 1;
            }
            candidates.push_back({(u64)maximum_term, (u64)(high - low)});

            if (maximum_term > limit / p) break;
            maximum_term *= p;
            ++exponent;
        }
    }

    sort(candidates.begin(), candidates.end(), [](const Candidate& a, const Candidate& b) {
        if (a.maximum_term != b.maximum_term) return a.maximum_term < b.maximum_term;
        return a.sum < b.sum;
    });
    return candidates;
}

int alternating_count(u64 left, u64 right) {
    if (left > right) return 0;
    if (((right - left + 1) & 1) == 0) return 0;
    return (left & 1) ? -1 : 1;
}

pair<i128, Candidate> best_at(u64 k, const vector<Candidate>& candidates) {
    i128 best_value = -1;
    Candidate best{0, 0};
    for (const Candidate& candidate : candidates) {
        if (candidate.maximum_term > k) break;
        i128 value = (i128)(k / candidate.maximum_term) * candidate.sum;
        if (value > best_value) {
            best_value = value;
            best = candidate;
        }
    }
    return {best_value, best};
}

i128 t_value(u64 limit) {
    vector<Candidate> candidates = make_candidates(limit);
    u64 k = 4;
    i128 answer = 0;

    while (k <= limit) {
        auto [value, best] = best_at(k, candidates);
        u64 quotient = k / best.maximum_term;
        u64 end = min<u64>(limit, (quotient + 1) * best.maximum_term - 1);

        for (const Candidate& candidate : candidates) {
            u64 needed_quotient = (u64)(value / candidate.sum) + 1;
            __uint128_t first_better = (__uint128_t)needed_quotient * candidate.maximum_term;
            if (first_better < k) first_better = k;
            if (first_better <= end &&
                (i128)((u64)(first_better / candidate.maximum_term)) * candidate.sum > value) {
                end = (u64)first_better - 1;
            }
        }

        int alternating = alternating_count(k, end);
        if (alternating != 0) answer += (i128)alternating * value;
        k = end + 1;
    }

    return answer;
}

int main(int argc, char** argv) {
    for (int i = 1; i < argc; ++i) {
        u64 limit = strtoull(argv[i], nullptr, 10);
        cout << to_string128(t_value(limit)) << '\n';
    }
    return 0;
}
"""


def run_limits(*limits):
    with tempfile.TemporaryDirectory(prefix="p542_") as tmp:
        tmp_path = Path(tmp)
        cpp = tmp_path / "p542.cpp"
        exe = tmp_path / "p542"
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
    sample, answer = run_limits(1000, 100_000_000_000_000_000)
    assert sample == "2268"
    return answer


if __name__ == "__main__":
    print(solve())
