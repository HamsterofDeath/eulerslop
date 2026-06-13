#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <utility>
#include <vector>

namespace {

using i64 = long long;
using u32 = std::uint32_t;
using u64 = unsigned long long;
using i128 = __int128_t;
using u128 = __uint128_t;

constexpr i64 MOD = 1'000'000'000LL;

struct Node {
    int left = 0;
    int right = 0;
    u32 priority = 0;
    bool reversed = false;
    u64 len = 0;
    u64 size = 0;
    i64 first = 0;
    i64 step = 1;
    i64 sum = 0;
    i64 weighted = 0;
};

std::vector<Node> tree(1);
u32 rng_state = 0x9e3779b9U;

u32 next_priority() {
    rng_state ^= rng_state << 13;
    rng_state ^= rng_state >> 17;
    rng_state ^= rng_state << 5;
    return rng_state;
}

i64 norm_mod(i128 value) {
    i64 result = static_cast<i64>(value % MOD);
    if (result < 0) {
        result += MOD;
    }
    return result;
}

i64 mul_mod_u(u64 a, u64 b) {
    return static_cast<i64>((static_cast<u128>(a % MOD) * (b % MOD)) % MOD);
}

i64 sum_i(u64 n) {
    u64 a = n;
    u64 b = n - 1;
    if ((a & 1ULL) == 0) {
        a /= 2;
    } else {
        b /= 2;
    }
    return mul_mod_u(a, b);
}

i64 sum_i2(u64 n) {
    u64 a = n;
    u64 b = n - 1;
    u64 c = 2 * n - 1;

    if ((a & 1ULL) == 0) {
        a /= 2;
    } else if ((b & 1ULL) == 0) {
        b /= 2;
    } else {
        c /= 2;
    }

    if (a % 3 == 0) {
        a /= 3;
    } else if (b % 3 == 0) {
        b /= 3;
    } else {
        c /= 3;
    }

    return static_cast<i64>(
        (((static_cast<u128>(a % MOD) * (b % MOD)) % MOD) * (c % MOD)) % MOD
    );
}

i64 run_sum(u64 len, i64 first, i64 step) {
    return norm_mod(static_cast<i128>(first) * (len % MOD)
                    + static_cast<i128>(step) * sum_i(len));
}

i64 run_weighted(u64 len, i64 first, i64 step) {
    return norm_mod(static_cast<i128>(first) * sum_i(len)
                    + static_cast<i128>(step) * sum_i2(len));
}

u64 subtree_size(int root) {
    return root == 0 ? 0 : tree[root].size;
}

i64 subtree_sum(int root) {
    return root == 0 ? 0 : tree[root].sum;
}

i64 subtree_weighted(int root) {
    return root == 0 ? 0 : tree[root].weighted;
}

int new_node(u64 len, i64 first, i64 step) {
    Node node;
    node.priority = next_priority();
    node.len = len;
    node.size = len;
    node.first = first;
    node.step = step;
    node.sum = run_sum(len, first, step);
    node.weighted = run_weighted(len, first, step);
    tree.push_back(node);
    return static_cast<int>(tree.size()) - 1;
}

void refresh(int root) {
    Node& node = tree[root];
    const int left = node.left;
    const int right = node.right;
    const u64 left_size = subtree_size(left);
    const i64 node_sum = run_sum(node.len, node.first, node.step);
    const i64 node_weighted = run_weighted(node.len, node.first, node.step);

    node.size = left_size + node.len + subtree_size(right);
    node.sum = norm_mod(static_cast<i128>(subtree_sum(left)) + node_sum
                        + subtree_sum(right));
    node.weighted = norm_mod(
        static_cast<i128>(subtree_weighted(left))
        + static_cast<i128>(left_size % MOD) * node_sum
        + node_weighted
        + static_cast<i128>((left_size + node.len) % MOD) * subtree_sum(right)
        + subtree_weighted(right)
    );
}

void apply_reverse(int root) {
    if (root == 0) {
        return;
    }

    Node& node = tree[root];
    std::swap(node.left, node.right);
    node.reversed = !node.reversed;
    node.first = static_cast<i64>(
        static_cast<i128>(node.first) + static_cast<i128>(node.step) * (node.len - 1)
    );
    node.step = -node.step;
    node.weighted = norm_mod(static_cast<i128>((node.size - 1) % MOD) * node.sum
                             - node.weighted);
}

void push(int root) {
    if (root == 0 || !tree[root].reversed) {
        return;
    }
    apply_reverse(tree[root].left);
    apply_reverse(tree[root].right);
    tree[root].reversed = false;
}

int merge(int left, int right) {
    if (left == 0) {
        return right;
    }
    if (right == 0) {
        return left;
    }

    if (tree[left].priority < tree[right].priority) {
        push(left);
        tree[left].right = merge(tree[left].right, right);
        refresh(left);
        return left;
    }

    push(right);
    tree[right].left = merge(left, tree[right].left);
    refresh(right);
    return right;
}

std::pair<int, int> split(int root, u64 left_count) {
    if (root == 0) {
        return {0, 0};
    }

    push(root);
    const u64 left_size = subtree_size(tree[root].left);
    if (left_count <= left_size) {
        auto parts = split(tree[root].left, left_count);
        tree[root].left = parts.second;
        refresh(root);
        return {parts.first, root};
    }

    const u64 through_node = left_size + tree[root].len;
    if (left_count >= through_node) {
        auto parts = split(tree[root].right, left_count - through_node);
        tree[root].right = parts.first;
        refresh(root);
        return {root, parts.second};
    }

    const int old_left = tree[root].left;
    const int old_right = tree[root].right;
    const u64 left_len = left_count - left_size;
    const u64 right_len = tree[root].len - left_len;
    const i64 old_first = tree[root].first;
    const i64 old_step = tree[root].step;

    tree[root].left = 0;
    tree[root].right = 0;
    tree[root].len = left_len;
    refresh(root);

    const i64 right_first = static_cast<i64>(
        static_cast<i128>(old_first) + static_cast<i128>(old_step) * left_len
    );
    const int right_node = new_node(right_len, right_first, old_step);

    return {merge(old_left, root), merge(right_node, old_right)};
}

u64 parse_u64(const char* text) {
    return static_cast<u64>(std::strtoull(text, nullptr, 10));
}

i64 solve(u64 n, int operations) {
    tree.clear();
    tree.reserve(static_cast<std::size_t>(2 * operations + 5));
    tree.push_back(Node{});
    rng_state = 0x9e3779b9U;

    int root = new_node(n, 0, 1);
    u64 previous = 1 % n;
    u64 current = 1 % n;

    for (int j = 1; j <= operations; ++j) {
        const u64 s = previous;
        const u64 t = current;
        const u64 low = std::min(s, t);
        const u64 high = std::max(s, t);

        auto left_mid_right = split(root, low);
        auto mid_right = split(left_mid_right.second, high - low + 1);
        apply_reverse(mid_right.first);
        root = merge(left_mid_right.first, merge(mid_right.first, mid_right.second));

        const u64 next_odd = (previous + current) % n;
        const u64 next_even = (current + next_odd) % n;
        previous = next_odd;
        current = next_even;
    }

    return tree[root].weighted;
}

}  // namespace

int main(int argc, char** argv) {
    u64 n = 1'000'000'000'000'000'000ULL;
    int operations = 1'000'000;
    if (argc >= 2) {
        n = parse_u64(argv[1]);
    }
    if (argc >= 3) {
        operations = static_cast<int>(parse_u64(argv[2]));
    }

    std::cout << solve(n, operations) << '\n';
    return 0;
}
