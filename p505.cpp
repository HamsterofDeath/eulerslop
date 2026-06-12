
#include <bits/stdc++.h>
using namespace std;

static const unsigned long long MASK = (1ULL << 60) - 1;

static inline unsigned long long combine(
    unsigned long long a,
    unsigned long long b,
    unsigned long long c,
    unsigned long long d
) {
    return (a * b + c * d) & MASK;
}

pair<unsigned long long, unsigned long long> state_at(unsigned long long k) {
    if (k == 0) return {0, 0};
    unsigned long long x = 1;
    unsigned long long parent = 0;
    int bits = 63 - __builtin_clzll(k);
    for (int bit = bits - 1; bit >= 0; --bit) {
        unsigned long long next_x;
        if ((k >> bit) & 1ULL) {
            next_x = combine(2, x, 3, parent);
        } else {
            next_x = combine(3, x, 2, parent);
        }
        parent = x;
        x = next_x;
    }
    return {x, parent};
}

unsigned long long minimax_subtree(
    unsigned long long x,
    unsigned long long parent,
    int depth,
    unsigned long long alpha,
    unsigned long long beta
) {
    if (depth == 0) return x;

    unsigned long long left = combine(3, x, 2, parent);
    unsigned long long right = combine(2, x, 3, parent);

    if (depth & 1) {
        if (left < right) swap(left, right);
        if (depth == 1) return left;

        unsigned long long value = minimax_subtree(left, x, depth - 1, alpha, beta);
        if (value > alpha) alpha = value;
        if (alpha >= beta) return alpha;

        value = minimax_subtree(right, x, depth - 1, alpha, beta);
        return value > alpha ? value : alpha;
    }

    if (left > right) swap(left, right);
    if (depth == 1) return left;

    unsigned long long value = minimax_subtree(left, x, depth - 1, alpha, beta);
    if (value < beta) beta = value;
    if (alpha >= beta) return beta;

    value = minimax_subtree(right, x, depth - 1, alpha, beta);
    return value < beta ? value : beta;
}

unsigned long long evaluate_subtree(unsigned long long k, int depth) {
    auto [x, parent] = state_at(k);
    return minimax_subtree(x, parent, depth, 0, MASK);
}

void collect_blocks(
    unsigned long long start,
    int depth,
    unsigned long long left_length,
    vector<tuple<unsigned long long, int, bool>>& blocks
) {
    unsigned long long size = 1ULL << depth;
    if (start + size <= left_length) {
        blocks.emplace_back(start, depth, false);
        return;
    }
    if (start >= left_length) {
        blocks.emplace_back(start, depth, true);
        return;
    }
    unsigned long long half = size >> 1;
    collect_blocks(start, depth - 1, left_length, blocks);
    collect_blocks(start + half, depth - 1, left_length, blocks);
}

unsigned long long block_value(
    unsigned long long start,
    int depth,
    bool right_side,
    unsigned long long base
) {
    unsigned long long leaf_start = base + start;

    if (!right_side) {
        return evaluate_subtree(leaf_start >> depth, depth);
    }
    if (depth == 0) {
        auto [x, parent] = state_at(leaf_start >> 1);
        (void)parent;
        return MASK - x;
    }
    return MASK - evaluate_subtree(leaf_start >> depth, depth - 1);
}

unsigned long long A(unsigned long long n) {
    if (n == 1) return 1;

    unsigned long long total_nodes = 2 * n - 1;
    int height = 63 - __builtin_clzll(total_nodes);
    unsigned long long base = 1ULL << height;
    unsigned long long boundary = 2 * n;
    unsigned long long left_length = boundary - base;

    vector<tuple<unsigned long long, int, bool>> blocks;
    collect_blocks(0, height, left_length, blocks);

    unordered_map<unsigned long long, unsigned long long> values;
    values.reserve(blocks.size() * 4 + 100);
    for (auto [start, depth, right_side] : blocks) {
        values[(start << 6) | (unsigned long long)depth] =
            block_value(start, depth, right_side, base);
    }

    function<unsigned long long(unsigned long long, int)> fold =
        [&](unsigned long long start, int depth) -> unsigned long long {
            unsigned long long key = (start << 6) | (unsigned long long)depth;
            auto it = values.find(key);
            if (it != values.end()) return it->second;

            unsigned long long half = 1ULL << (depth - 1);
            unsigned long long left = fold(start, depth - 1);
            unsigned long long right = fold(start + half, depth - 1);
            unsigned long long res = (depth & 1) ? max(left, right) : min(left, right);
            values[key] = res;
            return res;
        };

    unsigned long long value = fold(0, height);
    return (height & 1) ? MASK - value : value;
}

int main() {
    if (A(4) != 8) return 1;
    if (A(10) != ((1ULL << 60) - 34)) return 2;
    if (A(1000) != 101881) return 3;
    cout << A(1000000000000ULL) << '\n';
}
