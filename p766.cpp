// Project Euler 766: sliding block puzzle reachable configurations.
//
// Plain BFS over configurations.  Pieces of equal shape and colour are
// interchangeable, so a state is, per (shape,colour) class, the sorted list
// of piece anchor cells; packed 5 bits per piece into a u64 key.
//
// Board layout read off the problem images:
//   example (4 wide x 3 tall, 208 reachable):
//     G G r .        G = green corner tromino (cells 00,01,10)
//     G r r .        r = unit squares, . = empty
//     r r r r
//   target (6 wide x 5 tall):
//     . R R G R R    R = red tromino {00,01,10} (x2)
//     . R G G R Y    G = green tromino {01,10,11} (x2)
//     m m B B y Y    Y,y = two vertical dominoes (yellow)
//     m m B B y g    B = 2x2 block, c = horizontal domino (cyan)
//     m m c c g g    g = green tromino, m = unit squares (x6)
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <unordered_set>
#include <vector>
#include <algorithm>

using namespace std;
typedef unsigned long long u64;
typedef __uint128_t u128;

struct H128 {
    size_t operator()(u128 x) const {
        u64 a = (u64)x, b = (u64)(x >> 64);
        a ^= b * 0x9e3779b97f4a7c15ULL;
        a ^= a >> 30; a *= 0xbf58476d1ce4e5b9ULL;
        a ^= a >> 27; a *= 0x94d049bb133111ebULL;
        return a ^ (a >> 31);
    }
};

struct Shape { vector<pair<int, int>> cells; };

struct Puzzle {
    int W, H;
    vector<Shape> shapes;            // one entry per class
    vector<vector<int>> anchors0;    // initial anchors (cell = r*W+c) per class
};

static u64 count_reachable(const Puzzle& pz) {
    const int W = pz.W, H = pz.H;
    int npieces = 0;
    for (auto& a : pz.anchors0) npieces += a.size();

    // per class: precomputed cell lists per anchor, and move deltas
    struct Cls { int cnt; vector<vector<int>> cells; };
    vector<Cls> cls(pz.shapes.size());
    for (size_t s = 0; s < pz.shapes.size(); ++s) {
        cls[s].cnt = pz.anchors0[s].size();
        cls[s].cells.assign(W * H, {});
        for (int a = 0; a < W * H; ++a) {
            int ar = a / W, ac = a % W;
            bool ok = true;
            vector<int> cs;
            for (auto [dr, dc] : pz.shapes[s].cells) {
                int r = ar + dr, c = ac + dc;
                if (r >= H || c >= W) { ok = false; break; }
                cs.push_back(r * W + c);
            }
            if (ok) cls[s].cells[a] = cs;
        }
    }

    auto encode = [&](const vector<vector<int>>& anch) {
        u128 key = 0;
        for (auto& v : anch) {
            vector<int> w(v);
            sort(w.begin(), w.end());
            for (int a : w) key = key << 5 | (u128)(unsigned)a;
        }
        return key;
    };
    auto decode = [&](u128 key, vector<vector<int>>& anch) {
        for (int s = (int)cls.size() - 1; s >= 0; --s) {
            anch[s].resize(cls[s].cnt);
            for (int i = cls[s].cnt - 1; i >= 0; --i) {
                anch[s][i] = key & 31;
                key >>= 5;
            }
        }
    };

    vector<vector<int>> anch = pz.anchors0;
    u128 start = encode(anch);
    unordered_set<u128, H128> seen{start};
    vector<u128> queue{start};
    seen.reserve(1 << 22);
    vector<char> occ(W * H);
    const int DR[4] = {0, 0, 1, -1}, DC[4] = {1, -1, 0, 0};

    for (size_t qi = 0; qi < queue.size(); ++qi) {
        u128 key = queue[qi];
        decode(key, anch);
        memset(occ.data(), 0, occ.size());
        for (size_t s = 0; s < cls.size(); ++s)
            for (int a : anch[s])
                for (int c : cls[s].cells[a]) occ[c] = 1;
        for (size_t s = 0; s < cls.size(); ++s)
            for (int i = 0; i < cls[s].cnt; ++i) {
                int a = anch[s][i];
                int ar = a / W, ac = a % W;
                for (int d = 0; d < 4; ++d) {
                    int nr = ar + DR[d], nc = ac + DC[d];
                    if (nr < 0 || nc < 0 || nr >= H || nc >= W) continue;
                    int na = nr * W + nc;
                    if (cls[s].cells[na].empty()) continue;
                    // all new cells must be empty or belong to this piece
                    bool ok = true;
                    for (int c : cls[s].cells[na]) {
                        if (!occ[c]) continue;
                        bool own = false;
                        for (int c0 : cls[s].cells[a])
                            if (c0 == c) { own = true; break; }
                        if (!own) { ok = false; break; }
                    }
                    if (!ok) continue;
                    int old = anch[s][i];
                    anch[s][i] = na;
                    u128 nk = encode(anch);
                    if (seen.insert(nk).second) queue.push_back(nk);
                    anch[s][i] = old;
                }
            }
    }
    return (u64)seen.size();
}

int main() {
    Shape cornerNW{{{0, 0}, {0, 1}, {1, 0}}};   // missing bottom-right
    Shape cornerSE{{{0, 1}, {1, 0}, {1, 1}}};   // missing top-left
    Shape unit{{{0, 0}}};
    Shape vdom{{{0, 0}, {1, 0}}};
    Shape hdom{{{0, 0}, {0, 1}}};
    Shape square2{{{0, 0}, {0, 1}, {1, 0}, {1, 1}}};

    Puzzle example;
    example.W = 4; example.H = 3;
    example.shapes = {cornerNW, unit};
    example.anchors0 = {{0}, {2, 5, 6, 8, 9, 10, 11}};
    u64 ex = count_reachable(example);
    if (ex != 208) {
        fprintf(stderr, "example gives %llu, expected 208\n", ex);
        return 1;
    }

    Puzzle target;
    target.W = 6; target.H = 5;
    // cell index r*6+c
    target.shapes = {cornerNW, cornerSE, vdom, square2, hdom, unit};
    target.anchors0 = {
        {1, 4},              // red trominoes at (0,1),(0,4)
        {2, 22},             // green trominoes anchored (0,2),(3,4)
        {11, 16},            // yellow vertical dominoes (1,5),(2,4)
        {14},                // blue 2x2 at (2,2)
        {26},                // cyan horizontal domino (4,2)
        {12, 13, 18, 19, 24, 25},  // magenta unit squares
    };
    printf("%llu\n", count_reachable(target));
    return 0;
}
