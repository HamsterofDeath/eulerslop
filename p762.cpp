// Project Euler 762: amoebas on a 4-row cylinder, C(100000) mod 1e9.
//
// Reachable arrangements are exactly the leaf-sets of division trees
// (scheduling is always feasible; verified by BFS up to N = 14).  Reading
// a leaf-set column by column, the vector m of tree-node counts per row
// evolves deterministically: m' = A(m - l), A(v)_y = v_y + v_{y-1} (mod-4
// rows), where l in {0,1}^4 marks which rows hold leaves in this column.
// Hence arrangements correspond bijectively to leaf-choice sequences.
// A live state must keep sum(m) <= 8: each column removes at most 4
// leaves and doubles the rest, so sum > 8 can never return to zero.
// That leaves ~500 states; count sequences from m0 = (1,0,0,0) that
// terminate with exactly N+1 leaves.  l = 0 moves stay within a leaf
// layer but strictly increase sum(m), so layers resolve in decreasing-sum
// order.  Verified: C(2)=2, C(10)=1301, C(20)=5895236, C(100) mod 1e9 =
// 125923036.
#include <cstdint>
#include <cstdio>
#include <algorithm>
#include <array>
#include <map>
#include <vector>

using namespace std;
typedef unsigned long long u64;
typedef array<int, 4> St;

static const u64 MOD = 1000000000ULL;

int main() {
    // enumerate states 0 < sum <= 8
    vector<St> states;
    map<St, int> idx;
    for (int a = 0; a <= 8; ++a)
        for (int b = 0; b <= 8; ++b)
            for (int c = 0; c <= 8; ++c)
                for (int d = 0; d <= 8; ++d) {
                    int s = a + b + c + d;
                    if (s > 0 && s <= 8) {
                        St st{a, b, c, d};
                        idx[st] = states.size();
                        states.push_back(st);
                    }
                }
    int S = states.size();
    struct Tr { int j, k; };            // j = -1 means terminal
    vector<vector<Tr>> trans(S);
    vector<int> zero_next(S, -2);
    for (int i = 0; i < S; ++i) {
        const St& m = states[i];
        for (int lm = 0; lm < 16; ++lm) {
            St l{lm & 1, (lm >> 1) & 1, (lm >> 2) & 1, (lm >> 3) & 1};
            bool ok = true;
            St r;
            for (int y = 0; y < 4; ++y) {
                if (l[y] > m[y]) { ok = false; break; }
                r[y] = m[y] - l[y];
            }
            if (!ok) continue;
            St nx{r[0] + r[3], r[1] + r[0], r[2] + r[1], r[3] + r[2]};
            int k = l[0] + l[1] + l[2] + l[3];
            int sum = nx[0] + nx[1] + nx[2] + nx[3];
            if (sum == 0) {
                if (k > 0) trans[i].push_back({-1, k});
                continue;
            }
            if (sum > 8) continue;
            int j = idx[nx];
            if (k == 0)
                zero_next[i] = j;
            else
                trans[i].push_back({j, k});
        }
    }
    vector<int> order(S);
    for (int i = 0; i < S; ++i) order[i] = i;
    sort(order.begin(), order.end(), [&](int a, int b) {
        auto s = [&](int i) {
            return states[i][0] + states[i][1] + states[i][2] + states[i][3];
        };
        return s(a) > s(b);
    });

    auto run = [&](long long N) {
        long long L = N + 1;  // leaves
        vector<vector<u64>> F(5, vector<u64>(S, 0));  // ring buffer of layers
        int start = idx[St{1, 0, 0, 0}];
        u64 ans = 0;
        for (long long n = 1; n <= L; ++n) {
            vector<u64>& Fn = F[n % 5];
            fill(Fn.begin(), Fn.end(), 0);
            for (int i : order) {
                u64 acc = 0;
                for (const Tr& t : trans[i]) {
                    if (t.k > n) continue;
                    if (t.j == -1) {
                        if (t.k == n) acc += 1;
                    } else
                        acc += F[(n - t.k) % 5][t.j];
                }
                if (zero_next[i] >= 0) acc += Fn[zero_next[i]];
                Fn[i] = acc % MOD;
            }
            if (n == L) ans = Fn[start];
        }
        return ans;
    };

    if (run(2) != 2 || run(10) != 1301 || run(20) != 5895236ULL ||
        run(100) != 125923036ULL) {
        fprintf(stderr, "self-test failed: %llu %llu %llu %llu\n", run(2),
                run(10), run(20), run(100));
        return 1;
    }
    printf("%llu\n", run(100000));
    return 0;
}
