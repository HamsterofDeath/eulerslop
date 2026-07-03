// Project Euler 818: sum over ordered quadruples of SET lines.  A collection
// contributes once for every ordered 4-tuple of contained lines, so a tuple
// with union size u contributes C(81-u, n-u).
#include <array>
#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>

using namespace std;

struct Mask {
    uint64_t lo;
    uint64_t hi;
    bool operator==(const Mask& other) const {
        return lo == other.lo && hi == other.hi;
    }
};

struct HashMask {
    size_t operator()(const Mask& m) const {
        uint64_t x = m.lo ^ (m.hi + 0x9e3779b97f4a7c15ULL + (m.lo << 6) + (m.lo >> 2));
        x ^= x >> 33;
        x *= 0xff51afd7ed558ccdULL;
        x ^= x >> 33;
        return (size_t)x;
    }
};

static inline Mask unite(const Mask& a, const Mask& b) {
    return {a.lo | b.lo, a.hi | b.hi};
}

static inline int popcount(const Mask& m) {
    return __builtin_popcountll(m.lo) + __builtin_popcountll(m.hi);
}

static int point_index(const array<int, 4>& p) {
    return p[0] + 3 * p[1] + 9 * p[2] + 27 * p[3];
}

static vector<Mask> set_lines() {
    vector<array<int, 4>> points;
    for (int d = 0; d < 3; ++d)
        for (int c = 0; c < 3; ++c)
            for (int b = 0; b < 3; ++b)
                for (int a = 0; a < 3; ++a) points.push_back({a, b, c, d});

    vector<array<int, 4>> dirs;
    for (const auto& v : points) {
        if (v == array<int, 4>{0, 0, 0, 0}) continue;
        for (int x : v) {
            if (x == 0) continue;
            if (x == 1) dirs.push_back(v);
            break;
        }
    }

    unordered_map<Mask, int, HashMask> seen;
    for (const auto& p : points) {
        for (const auto& v : dirs) {
            Mask m{0, 0};
            for (int t = 0; t < 3; ++t) {
                array<int, 4> q;
                for (int i = 0; i < 4; ++i) q[i] = (p[i] + t * v[i]) % 3;
                int idx = point_index(q);
                if (idx < 64)
                    m.lo |= 1ULL << idx;
                else
                    m.hi |= 1ULL << (idx - 64);
            }
            seen[m] = 1;
        }
    }

    vector<Mask> lines;
    lines.reserve(seen.size());
    for (const auto& item : seen) lines.push_back(item.first);
    return lines;
}

static unsigned long long binom(int n, int k) {
    if (k < 0 || k > n) return 0;
    if (k > n - k) k = n - k;
    unsigned long long result = 1;
    for (int i = 1; i <= k; ++i) {
        result *= n - k + i;
        result /= i;
    }
    return result;
}

static array<unsigned long long, 13> ordered_quad_union_distribution() {
    vector<Mask> lines = set_lines();
    if (lines.size() != 1080) {
        fprintf(stderr, "bad line count: %zu\n", lines.size());
        exit(1);
    }

    Mask first = lines[0];
    unordered_map<Mask, unsigned int, HashMask> pair_unions;
    pair_unions.reserve(700000);
    for (const Mask& b : lines) {
        Mask fb = unite(first, b);
        for (const Mask& c : lines) {
            ++pair_unions[unite(fb, c)];
        }
    }

    array<unsigned long long, 13> dist{};
    for (const auto& item : pair_unions) {
        const Mask& base = item.first;
        unsigned long long ways = item.second;
        for (const Mask& d : lines) {
            dist[popcount(unite(base, d))] += ways;
        }
    }

    for (auto& x : dist) x *= lines.size();
    return dist;
}

static unsigned __int128 f_value(int n) {
    static array<unsigned long long, 13> dist = ordered_quad_union_distribution();
    unsigned __int128 total = 0;
    for (int u = 0; u <= 12; ++u) {
        if (dist[u] == 0) continue;
        total += (unsigned __int128)dist[u] * binom(81 - u, n - u);
    }
    return total;
}

static string to_string_u128(unsigned __int128 value) {
    if (value == 0) return "0";
    string out;
    while (value) {
        out.push_back(char('0' + value % 10));
        value /= 10;
    }
    reverse(out.begin(), out.end());
    return out;
}

int main() {
    if (f_value(3) != 1080 || f_value(6) != 159690960) {
        cerr << "self-test failed\n";
        return 1;
    }
    cout << to_string_u128(f_value(12)) << "\n";
    return 0;
}
