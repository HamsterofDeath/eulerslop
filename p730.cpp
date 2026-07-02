// Project Euler 730: k-shifted Pythagorean triples, S(100, 1e8).
//
// For fixed k the solutions of p^2 + q^2 - r^2 = -k with p,q >= 1 form a
// forest under the three Berggren matrices (elements of O(2,1;Z), so they
// preserve the form and, being unimodular, the gcd).  Along every forward
// edge both r and p+q+r strictly increase, so the descent by inverse
// matrices terminates in "roots" (no positive preimage), which all live in
// a small box.  Starting from the primitive roots the forest enumerates
// each ordered positive solution exactly once (validated against brute
// force below); unordered triples are the nodes with p <= q.
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <atomic>
#include <numeric>
#include <thread>
#include <vector>

using namespace std;
typedef long long i64;

static const i64 T[3][3][3] = {
    {{1, -2, 2}, {2, -1, 2}, {2, -2, 3}},
    {{1, 2, 2}, {2, 1, 2}, {2, 2, 3}},
    {{-1, 2, 2}, {-2, 1, 2}, {-2, 2, 3}},
};
static const i64 TI[3][3][3] = {
    {{1, 2, -2}, {-2, -1, 2}, {-2, -2, 3}},
    {{1, 2, -2}, {2, 1, -2}, {-2, -2, 3}},
    {{-1, -2, 2}, {2, 1, -2}, {-2, -2, 3}},
};

struct Node { i64 p, q, r; };

static inline Node emul(const i64 M[3][3], const Node& v) {
    return {M[0][0] * v.p + M[0][1] * v.q + M[0][2] * v.r,
            M[1][0] * v.p + M[1][1] * v.q + M[1][2] * v.r,
            M[2][0] * v.p + M[2][1] * v.q + M[2][2] * v.r};
}

static bool is_root(const Node& v) {
    for (int i = 0; i < 3; ++i) {
        Node w = emul(TI[i], v);
        if (w.p >= 1 && w.q >= 1 && w.r >= 1) return false;
    }
    return true;
}

static i64 isqrt64(i64 x) {
    i64 r = (i64)sqrtl((long double)x);
    while (r * r > x) --r;
    while ((r + 1) * (r + 1) <= x) ++r;
    return r;
}

// all primitive roots for shift k (ordered pairs)
static vector<Node> roots(i64 k, i64 bound = 1000) {
    vector<Node> res;
    for (i64 p = 1; p <= bound; ++p)
        for (i64 q = 1; q <= bound; ++q) {
            i64 r = isqrt64(p * p + q * q + k);
            if (r * r != p * p + q * q + k) continue;
            if (gcd(p, gcd(q, r)) != 1) continue;
            Node v{p, q, r};
            if (is_root(v)) {
                if (p > bound / 2 || q > bound / 2) {
                    fprintf(stderr, "root near scan bound: k=%lld %lld %lld %lld\n",
                            k, p, q, r);
                    exit(1);
                }
                res.push_back(v);
            }
        }
    return res;
}

// count unordered solutions (p<=q) with p+q+r <= n in the subtree at v,
// including v itself
static i64 dfs_count(Node v, i64 n) {
    vector<Node> stk{v};
    i64 cnt = 0;
    while (!stk.empty()) {
        Node w = stk.back();
        stk.pop_back();
        if (w.p + w.q + w.r > n) continue;
        if (w.p <= w.q) ++cnt;
        for (int i = 0; i < 3; ++i) stk.push_back(emul(T[i], w));
    }
    return cnt;
}

static i64 count_forest(i64 kmax, i64 n) {
    // build work items: (root nodes over all k), split a few levels deep
    vector<Node> work;
    i64 base = 0;
    for (i64 k = 0; k <= kmax; ++k)
        for (const Node& v : roots(k)) work.push_back(v);
    // expand frontier for load balancing
    for (int lvl = 0; lvl < 6; ++lvl) {
        vector<Node> next;
        for (const Node& w : work) {
            if (w.p + w.q + w.r > n) continue;
            if (w.p <= w.q) ++base;
            for (int i = 0; i < 3; ++i) next.push_back(emul(T[i], w));
        }
        work.swap(next);
    }
    atomic<size_t> idx{0};
    int nth = max(1u, thread::hardware_concurrency());
    vector<i64> part(nth, 0);
    vector<thread> ths;
    for (int ti = 0; ti < nth; ++ti)
        ths.emplace_back([&, ti]() {
            i64 acc = 0;
            for (;;) {
                size_t i = idx.fetch_add(1);
                if (i >= work.size()) break;
                acc += dfs_count(work[i], n);
            }
            part[ti] = acc;
        });
    for (auto& t : ths) t.join();
    i64 s = base;
    for (i64 v : part) s += v;
    return s;
}

// brute force count of primitive k-shifted triples with p<=q, p+q+r<=n
static i64 brute(i64 k, i64 n) {
    i64 cnt = 0;
    for (i64 p = 1; 2 * p < n; ++p)
        for (i64 q = p;; ++q) {
            i64 r = isqrt64(p * p + q * q + k);
            if (p + q + r > n) break;
            if (r * r == p * p + q * q + k && r >= 1 &&
                gcd(p, gcd(q, r)) == 1)
                ++cnt;
        }
    return cnt;
}

static i64 forest_single(i64 k, i64 n) {
    i64 s = 0;
    for (const Node& v : roots(k)) s += dfs_count(v, n);
    return s;
}

int main() {
    // self-tests: given values and brute-force cross-checks
    if (forest_single(0, 10000) != 703 || forest_single(20, 10000) != 1979) {
        fprintf(stderr, "given-value test failed\n");
        return 1;
    }
    i64 s10 = 0;
    for (i64 k = 0; k <= 10; ++k) s10 += forest_single(k, 10000);
    if (s10 != 10956) {
        fprintf(stderr, "S(10,1e4)=%lld != 10956\n", s10);
        return 1;
    }
    for (i64 k : {0, 1, 2, 3, 4, 5, 7, 25, 36, 50, 99, 100}) {
        i64 f = forest_single(k, 3000), b = brute(k, 3000);
        if (f != b) {
            fprintf(stderr, "mismatch k=%lld forest=%lld brute=%lld\n", k, f, b);
            return 1;
        }
    }
    printf("%lld\n", count_forest(100, 100000000LL));
    return 0;
}
