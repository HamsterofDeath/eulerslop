#include <algorithm>
#include <cassert>
#include <cmath>
#include <cstdint>
#include <functional>
#include <iostream>
#include <numeric>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

using i64 = long long;
using i128 = __int128_t;
using u64 = unsigned long long;

struct Graph {
    std::vector<int> value;
    std::vector<std::pair<int, int>> edges;
    std::vector<std::vector<std::pair<int, int>>> adj;
};

struct Block {
    std::vector<int> vertices;
    std::vector<std::pair<int, int>> edges;
};

i64 isqrt(i64 x) {
    i64 r = std::sqrt(static_cast<long double>(x));
    while ((r + 1) * (r + 1) <= x) ++r;
    while (r * r > x) --r;
    return r;
}

Graph build_graph(int limit) {
    std::vector<int> spf(limit + 1);
    std::iota(spf.begin(), spf.end(), 0);
    for (int i = 2; i * i <= limit; ++i) {
        if (spf[i] == i) {
            for (i64 j = 1LL * i * i; j <= limit; j += i) {
                if (spf[j] == j) spf[j] = i;
            }
        }
    }

    std::vector<char> allowed(limit + 1, false);
    allowed[1] = allowed[2] = true;
    for (int p = 3; p <= limit; ++p) {
        if (spf[p] == p) {
            for (i64 v = p; v <= limit; v *= p) {
                allowed[v] = true;
                if (2 * v <= limit) allowed[2 * v] = true;
            }
        }
    }

    Graph graph;
    std::vector<int> id(limit + 1, -1);
    for (int n = 1; n <= limit; ++n) {
        if (allowed[n]) {
            id[n] = static_cast<int>(graph.value.size());
            graph.value.push_back(n);
        }
    }

    auto add_edge = [&](int a, int b) {
        if (a == b || b < 1 || b > limit || id[a] < 0 || id[b] < 0) return;
        i64 z = 1LL * a * b - 1;
        i64 root = isqrt(z);
        if (root * root != z) return;
        int u = id[a], v = id[b];
        if (u > v) std::swap(u, v);
        graph.edges.push_back({u, v});
    };

    for (i64 x = 1; x * x + 1 <= limit; ++x) {
        add_edge(1, static_cast<int>(x * x + 1));
    }
    for (i64 x = 1; x * x + 1 <= 2LL * limit; x += 2) {
        add_edge(2, static_cast<int>((x * x + 1) / 2));
    }

    for (int a : graph.value) {
        if (a <= 2) continue;

        int odd_part = a;
        while (odd_part % 2 == 0) odd_part /= 2;
        int p = spf[odd_part];
        if (p % 4 != 1) continue;

        int exponent = 0;
        int rest = odd_part;
        while (rest % p == 0) {
            ++exponent;
            rest /= p;
        }
        if (rest != 1) continue;

        i64 prime_power = 1;
        for (int i = 0; i < exponent; ++i) prime_power *= p;

        int root_mod_p = 0;
        for (int x = 1; x < p; ++x) {
            if (1LL * x * x % p == p - 1) {
                root_mod_p = x;
                break;
            }
        }

        i64 root = root_mod_p;
        i64 modulus = p;
        for (int level = 1; level < exponent; ++level) {
            i64 next_modulus = modulus * p;
            for (int j = 0; j < p; ++j) {
                i64 candidate = root + j * modulus;
                if (static_cast<i128>(candidate) * candidate % next_modulus == next_modulus - 1) {
                    root = candidate;
                    break;
                }
            }
            modulus = next_modulus;
        }

        std::vector<i64> roots{root, (prime_power - root) % prime_power};
        if (a == 2 * prime_power) {
            roots.push_back(root + prime_power);
            roots.push_back((prime_power - root) % prime_power + prime_power);
        }
        std::sort(roots.begin(), roots.end());
        roots.erase(std::unique(roots.begin(), roots.end()), roots.end());

        i64 xmax = isqrt(1LL * a * limit - 1);
        for (i64 residue : roots) {
            if (residue == 0) residue += a;
            for (i64 x = residue; x <= xmax; x += a) {
                i64 value = x * x + 1;
                if (value % a != 0) continue;
                i64 b = value / a;
                if (b <= limit) add_edge(a, static_cast<int>(b));
            }
        }
    }

    std::sort(graph.edges.begin(), graph.edges.end());
    graph.edges.erase(std::unique(graph.edges.begin(), graph.edges.end()), graph.edges.end());
    graph.adj.assign(graph.value.size(), {});
    for (int i = 0; i < static_cast<int>(graph.edges.size()); ++i) {
        auto [u, v] = graph.edges[i];
        graph.adj[u].push_back({v, i});
        graph.adj[v].push_back({u, i});
    }
    return graph;
}

std::vector<Block> biconnected_blocks(const Graph& graph) {
    int n = static_cast<int>(graph.value.size());
    std::vector<int> disc(n, -1), low(n), edge_stack;
    std::vector<Block> blocks;
    int timer = 0;

    std::function<void(int, int)> dfs = [&](int u, int parent_edge) {
        disc[u] = low[u] = ++timer;
        for (auto [v, edge_id] : graph.adj[u]) {
            if (edge_id == parent_edge) continue;
            if (disc[v] == -1) {
                edge_stack.push_back(edge_id);
                dfs(v, edge_id);
                low[u] = std::min(low[u], low[v]);
                if (low[v] >= disc[u]) {
                    std::vector<int> component_edges;
                    int top;
                    do {
                        top = edge_stack.back();
                        edge_stack.pop_back();
                        component_edges.push_back(top);
                    } while (top != edge_id);

                    std::unordered_map<int, int> local;
                    Block block;
                    for (int edge : component_edges) {
                        auto [a, b] = graph.edges[edge];
                        if (!local.count(a)) {
                            local[a] = static_cast<int>(block.vertices.size());
                            block.vertices.push_back(a);
                        }
                        if (!local.count(b)) {
                            local[b] = static_cast<int>(block.vertices.size());
                            block.vertices.push_back(b);
                        }
                        block.edges.push_back({local[a], local[b]});
                    }
                    blocks.push_back(std::move(block));
                }
            } else if (disc[v] < disc[u]) {
                edge_stack.push_back(edge_id);
                low[u] = std::min(low[u], disc[v]);
            }
        }
    };

    for (int i = 0; i < n; ++i) {
        if (disc[i] == -1) dfs(i, -1);
    }
    return blocks;
}

u64 cycle_sum_for_block(const Block& block, const std::vector<int>& values) {
    int m = static_cast<int>(block.vertices.size());
    if (static_cast<int>(block.edges.size()) < m) return 0;
    assert(m <= 63);

    std::vector<int> order(m), rank(m);
    std::iota(order.begin(), order.end(), 0);
    std::sort(order.begin(), order.end(), [&](int a, int b) {
        return block.vertices[a] < block.vertices[b];
    });
    for (int i = 0; i < m; ++i) rank[order[i]] = i;

    std::vector<std::vector<int>> adj(m);
    std::vector<u64> weight(m);
    for (int old = 0; old < m; ++old) weight[rank[old]] = values[block.vertices[old]];
    for (auto [u, v] : block.edges) {
        u = rank[u];
        v = rank[v];
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    for (auto& list : adj) std::sort(list.begin(), list.end());

    u64 total = 0;
    std::function<void(int, int, int, u64, u64)> dfs =
        [&](int start, int u, int second, u64 mask, u64 path_sum) {
            for (int v : adj[u]) {
                if (v == start) {
                    if (__builtin_popcountll(mask) >= 3 && second < u) total += path_sum;
                } else if (v > start && ((mask >> v) & 1ULL) == 0) {
                    dfs(start, v, second < 0 ? v : second, mask | (1ULL << v), path_sum + weight[v]);
                }
            }
        };

    for (int start = 0; start < m; ++start) {
        dfs(start, start, -1, 1ULL << start, weight[start]);
    }
    return total;
}

u64 solve_limit(int limit) {
    Graph graph = build_graph(limit);
    std::vector<Block> blocks = biconnected_blocks(graph);
    u64 total = 0;
    for (const Block& block : blocks) {
        total += cycle_sum_for_block(block, graph.value);
    }
    return total;
}

int main() {
    assert(solve_limit(20) == 258);
    assert(solve_limit(100) == 538768);
    std::cout << solve_limit(1000000) << '\n';
}
