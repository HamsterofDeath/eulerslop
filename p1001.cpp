// Project Euler 1001: Connections I.
//
// A chosen set of value pairs is connectable iff the arcs drawn above the
// row do not cross, i.e. the intervals [l_v, r_v] of the chosen values
// form a laminar family (nested or disjoint).  Let F(l, r) be the number
// of laminar families inside [l, r].  Splitting a family at its leftmost
// chosen pair (l_v, r_v) - everything left of l_v, the pair itself, and an
// arbitrary family strictly inside - gives
//
//     F(l, r) = 1 + sum_{l <= l_v, r_v <= r} B_v * F(r_v + 1, r)
//     B_v     = F(l_v + 1, r_v - 1)          (families strictly inside v)
//
// For a fixed left end a define X[a][b] = F(a, b).  Scanning b gives
//
//     X[a][b] = X[a][b-1] + [b closes v and l_v >= a] B_v * X[a][l_v - 1]
//
// B_v depends only on values whose left occurrence is > l_v, so computing
// the sequences X[a][*] for a = l_v + 1 in decreasing order of a yields
// every B_v with one O(2n) pass per value.  Answer = X[1][2n] mod
// 1_003_443_221.

#include <cstdint>
#include <cstdio>
#include <fstream>
#include <string>
#include <vector>

namespace {

using u32 = std::uint32_t;
using u64 = std::uint64_t;

constexpr u64 MOD = 1'003'443'221;

}  // namespace

int main(int argc, char** argv) {
    std::ifstream in(argv[1]);
    std::string token;
    std::vector<u32> arr;
    while (std::getline(in, token, ',')) {
        u32 v = 0;
        for (char c : token) v = v * 10 + (u32)(c - '0');
        arr.push_back(v);
    }
    const u32 n = (u32)arr.size() / 2;
    const u32 M = (u32)arr.size();

    std::vector<u32> pos1(n, 0), pos2(n, 0);
    for (u32 i = 0; i < M; ++i) {
        u32 v = arr[i];
        if (pos1[v] == 0)
            pos1[v] = i + 1;
        else
            pos2[v] = i + 1;
    }
    // left occurrence of the value closing at b (0 when b opens a value);
    // B_of_pos[b] = B of the value at position b (0 for opening positions).
    std::vector<u32> lv(M + 1, 0);
    std::vector<u64> B_of_pos(M + 1, 0);
    std::vector<u64> B(n, 0);
    for (u32 v = 0; v < n; ++v) lv[pos2[v]] = pos1[v];

    std::vector<u64> x(M + 1);
    for (u32 a = M; a >= 2; --a) {
        u32 v = arr[a - 2];
        if (pos1[v] != a - 1) continue;
        for (u32 b = 0; b < a; ++b) x[b] = 1;
        for (u32 b = a; b <= M; ++b) {
            u32 l = lv[b];
            u64 cur = x[b - 1];
            if (l >= a) cur = (cur + B_of_pos[b] * x[l - 1]) % MOD;
            x[b] = cur;
        }
        B[v] = x[pos2[v] - 1];
        B_of_pos[pos2[v]] = B[v];
    }
    for (u32 b = 0; b < 1; ++b) x[b] = 1;
    for (u32 b = 1; b <= M; ++b) {
        u32 l = lv[b];
        u64 cur = x[b - 1];
        if (l >= 1) cur = (cur + B_of_pos[b] * x[l - 1]) % MOD;
        x[b] = cur;
    }
    std::printf("%llu\n", (unsigned long long)x[M]);
    return 0;
}
