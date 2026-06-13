#include <array>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <unordered_map>
#include <vector>

using namespace std;

struct Key {
    uint32_t labels;
    uint64_t sizes;
    uint8_t best;

    bool operator==(const Key &other) const {
        return labels == other.labels && sizes == other.sizes && best == other.best;
    }
};

struct KeyHash {
    size_t operator()(const Key &key) const {
        uint64_t x = key.sizes ^ (uint64_t(key.labels) << 32) ^ uint64_t(key.best);
        x ^= x >> 30;
        x *= 0xbf58476d1ce4e5b9ULL;
        x ^= x >> 27;
        x *= 0x94d049bb133111ebULL;
        x ^= x >> 31;
        return size_t(x);
    }
};

static int find_root(array<int, 16> &parent, int x) {
    while (parent[x] != x) {
        parent[x] = parent[parent[x]];
        x = parent[x];
    }
    return x;
}

static void unite(array<int, 16> &parent, array<int, 16> &size, int a, int b) {
    int ra = find_root(parent, a);
    int rb = find_root(parent, b);
    if (ra == rb) return;
    if (rb < ra) swap(ra, rb);
    parent[rb] = ra;
    size[ra] += size[rb];
}

static Key step_state(const Key &state, int mask) {
    constexpr int W = 7;
    array<int, W> old_labels{};
    int max_label = 0;
    for (int i = 0; i < W; ++i) {
        old_labels[i] = (state.labels >> (3 * i)) & 7;
        max_label = max(max_label, old_labels[i]);
    }

    array<int, 16> parent{};
    array<int, 16> comp_size{};
    for (int i = 0; i < 16; ++i) parent[i] = i;
    for (int label = 1; label <= max_label; ++label) {
        comp_size[label] = (state.sizes >> (6 * (label - 1))) & 63;
    }

    array<int, W> next_labels{};
    int next_id = max_label + 1;
    for (int col = 0; col < W; ++col) {
        if (((mask >> col) & 1) == 0) continue;
        int label = next_id++;
        comp_size[label] = 1;
        if (old_labels[col]) unite(parent, comp_size, label, old_labels[col]);
        if (col > 0 && next_labels[col - 1]) unite(parent, comp_size, label, next_labels[col - 1]);
        next_labels[col] = find_root(parent, label);
    }

    array<bool, 16> active{};
    for (int col = 0; col < W; ++col) {
        if (next_labels[col]) {
            next_labels[col] = find_root(parent, next_labels[col]);
            active[next_labels[col]] = true;
        }
    }

    int best = state.best;
    for (int label = 1; label <= max_label; ++label) {
        int root = find_root(parent, label);
        if (!active[root]) best = max(best, comp_size[root]);
    }

    array<int, 16> remap{};
    uint32_t packed_labels = 0;
    uint64_t packed_sizes = 0;
    int compact_count = 0;
    for (int col = 0; col < W; ++col) {
        int root = next_labels[col];
        if (!root) continue;
        if (!remap[root]) {
            remap[root] = ++compact_count;
            packed_sizes |= uint64_t(comp_size[root]) << (6 * (compact_count - 1));
        }
        packed_labels |= uint32_t(remap[root]) << (3 * col);
    }
    return Key{packed_labels, packed_sizes, uint8_t(best)};
}

int main() {
    constexpr int W = 7;
    constexpr int H = 7;
    unordered_map<Key, uint64_t, KeyHash> states;
    states.reserve(1 << 16);
    states.emplace(Key{0, 0, 0}, 1);

    for (int row = 0; row < H; ++row) {
        unordered_map<Key, uint64_t, KeyHash> next;
        next.reserve(states.size() * 8);
        for (const auto &[state, count] : states) {
            for (int mask = 0; mask < (1 << W); ++mask) {
                next[step_state(state, mask)] += count;
            }
        }
        states.swap(next);
    }

    unsigned __int128 numerator = 0;
    for (const auto &[state, count] : states) {
        int best = state.best;
        for (int label = 0; label < 7; ++label) {
            best = max(best, int((state.sizes >> (6 * label)) & 63));
        }
        numerator += static_cast<unsigned __int128>(best) * count;
    }

    long double expected = static_cast<long double>(numerator) / static_cast<long double>(1ULL << 49);
    cout << fixed << setprecision(8) << double(expected) << '\n';
    return 0;
}
