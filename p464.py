#!/usr/bin/env python3

import subprocess
import tempfile
from pathlib import Path


SOURCE = r"""
#include <bits/stdc++.h>
using namespace std;

using i64 = long long;

struct Block {
    int left;
    int right;
    vector<int> c_values;
    vector<int> d_values;
    vector<int> c_bit;
    vector<int> d_bit;
};

void bit_add(vector<int>& bit, int index) {
    for (int n = (int)bit.size(); index < n; index += index & -index) {
        ++bit[index];
    }
}

int bit_sum(const vector<int>& bit, int index) {
    int result = 0;
    while (index > 0) {
        result += bit[index];
        index -= index & -index;
    }
    return result;
}

i64 solve_limit(int limit) {
    vector<int> mu(limit + 1), least_prime(limit + 1), primes;
    mu[1] = 1;

    for (int i = 2; i <= limit; ++i) {
        if (least_prime[i] == 0) {
            least_prime[i] = i;
            primes.push_back(i);
            mu[i] = -1;
        }
        for (int p : primes) {
            long long value = 1LL * p * i;
            if (value > limit) break;
            least_prime[value] = p;
            if (p == least_prime[i]) {
                mu[value] = 0;
                break;
            }
            mu[value] = -mu[i];
        }
    }

    vector<int> mertens(limit + 1), squarefree_count(limit + 1);
    int min_mertens = 0;
    int max_mertens = 0;
    for (int i = 1; i <= limit; ++i) {
        mertens[i] = mertens[i - 1] + mu[i];
        squarefree_count[i] = squarefree_count[i - 1] + (mu[i] != 0);
        min_mertens = min(min_mertens, mertens[i]);
        max_mertens = max(max_mertens, mertens[i]);
    }

    int range = max_mertens - min_mertens + 1;
    int block_size = max(1, (int)sqrt(range) + 1);
    int block_count = (range + block_size - 1) / block_size;
    vector<Block> blocks(block_count);
    for (int b = 0; b < block_count; ++b) {
        blocks[b].left = b * block_size;
        blocks[b].right = min(range - 1, (b + 1) * block_size - 1);
    }

    for (int i = 0; i <= limit; ++i) {
        int s = mertens[i] - min_mertens;
        int b = s / block_size;
        blocks[b].c_values.push_back(squarefree_count[i] - 199 * mertens[i]);
        blocks[b].d_values.push_back(squarefree_count[i] + 199 * mertens[i]);
    }
    for (Block& block : blocks) {
        sort(block.c_values.begin(), block.c_values.end());
        block.c_values.erase(unique(block.c_values.begin(), block.c_values.end()), block.c_values.end());
        block.c_bit.assign(block.c_values.size() + 1, 0);

        sort(block.d_values.begin(), block.d_values.end());
        block.d_values.erase(unique(block.d_values.begin(), block.d_values.end()), block.d_values.end());
        block.d_bit.assign(block.d_values.size() + 1, 0);
    }

    vector<vector<int>> by_mertens(range);

    auto insert_prefix = [&](int s_original, int t) {
        int s = s_original - min_mertens;
        int b = s / block_size;
        Block& block = blocks[b];
        int c = t - 199 * s_original;
        int d = t + 199 * s_original;
        int c_index = lower_bound(block.c_values.begin(), block.c_values.end(), c) - block.c_values.begin() + 1;
        int d_index = lower_bound(block.d_values.begin(), block.d_values.end(), d) - block.d_values.begin() + 1;
        bit_add(block.c_bit, c_index);
        bit_add(block.d_bit, d_index);
        by_mertens[s].push_back(t);
    };

    auto count_bucket = [&](int s, int threshold) {
        const vector<int>& values = by_mertens[s];
        return (int)(upper_bound(values.begin(), values.end(), threshold) - values.begin());
    };

    auto query_left = [&](int s_index, int threshold) {
        i64 result = 0;
        int b = s_index / block_size;
        for (int bb = 0; bb < b; ++bb) {
            const Block& block = blocks[bb];
            int pos = upper_bound(block.c_values.begin(), block.c_values.end(), threshold) - block.c_values.begin();
            result += bit_sum(block.c_bit, pos);
        }
        for (int s = blocks[b].left; s <= s_index; ++s) {
            int s_original = s + min_mertens;
            result += count_bucket(s, threshold + 199 * s_original);
        }
        return result;
    };

    auto query_right = [&](int s_index, int threshold) {
        if (s_index >= range) return 0LL;

        i64 result = 0;
        int b = s_index / block_size;
        for (int s = s_index; s <= blocks[b].right; ++s) {
            int s_original = s + min_mertens;
            result += count_bucket(s, threshold - 199 * s_original);
        }
        for (int bb = b + 1; bb < block_count; ++bb) {
            const Block& block = blocks[bb];
            int pos = upper_bound(block.d_values.begin(), block.d_values.end(), threshold) - block.d_values.begin();
            result += bit_sum(block.d_bit, pos);
        }
        return result;
    };

    i64 answer = 0;
    insert_prefix(mertens[0], squarefree_count[0]);
    for (int j = 1; j <= limit; ++j) {
        int s_index = mertens[j] - min_mertens;
        answer += query_left(s_index, squarefree_count[j] - 199 * mertens[j]);
        answer += query_right(s_index + 1, squarefree_count[j] + 199 * mertens[j]);
        insert_prefix(mertens[j], squarefree_count[j]);
    }
    return answer;
}

int main(int argc, char** argv) {
    for (int i = 1; i < argc; ++i) {
        cout << solve_limit(atoi(argv[i])) << '\n';
    }
    return 0;
}
"""


def run_limits(*limits):
    with tempfile.TemporaryDirectory(prefix="p464_") as tmp:
        tmp_path = Path(tmp)
        cpp = tmp_path / "p464.cpp"
        exe = tmp_path / "p464"
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
    sample_10, sample_500, sample_10000, answer = run_limits(
        10, 500, 10_000, 20_000_000
    )
    assert sample_10 == "13"
    assert sample_500 == "16676"
    assert sample_10000 == "20155319"
    return answer


if __name__ == "__main__":
    print(solve())
