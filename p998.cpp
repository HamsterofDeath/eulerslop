// Project Euler 998: Squaring the Triangle.
//
// The minimum bounding square of a triangle always has a triangle vertex at a
// square corner.  The side is the minimum over the three corner
// configurations.  For a triangle to have integer square side k, the
// minimum must come from either
//   * an integer altitude h = k > L onto side L (flush configuration), or
//   * a crossing value k at a vertex.
// Both force Heronian triangles whose sides come from two Pythagorean
// triples sharing the leg h = k:
//   ALT:   third side L = |p1 +- p2|            (h >= L)
//   CROSS: third side o = sqrt((h-p1)^2+(h-p2)^2)
// (p, A) = (other leg, hypotenuse) of the right triangles (h, p, A).
//
// Enumerate all such triangles with h <= 10^6 and sides <= sqrt(2)*10^6,
// verify the minimal square side exactly with integer arithmetic, and sum
// the perimeters of those with integer square side k <= 10^6.

#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <cmath>
#include <numeric>
#include <unordered_set>
#include <vector>

namespace {

using u64 = std::uint64_t;
using u32 = std::uint32_t;
using i128 = __int128;

long long N = 1'000'000;
long long MAXSIDE = 1'414'213;

i128 A2g;  // area squared of the triangle being checked

i128 isqrt128(i128 x) {
    long double r = std::sqrt((long double)x);
    i128 s = (i128)r;
    while (s > 0 && s * s > x) --s;
    while ((s + 1) * (s + 1) <= x) ++s;
    return s;
}

// 256-bit unsigned helpers (4 x u64 limbs).
struct U256 {
    u64 w[4] = {0, 0, 0, 0};
};

// out = a * b (a, b up to 4 limbs; out up to 8 limbs).
void mul256(const u64* a, const u64* b, u64* out) {
    for (int i = 0; i < 8; ++i) out[i] = 0;
    for (int i = 0; i < 4; ++i) {
        u64 carry = 0;
        for (int j = 0; j < 4; ++j) {
            __uint128_t t = (__uint128_t)a[i] * b[j] + out[i + j] + carry;
            out[i + j] = (u64)t;
            carry = (u64)(t >> 64);
        }
        // propagate into out[i+4]
        int k = i + 4;
        while (carry && k < 8) {
            __uint128_t t = (__uint128_t)out[k] + carry;
            out[k] = (u64)t;
            carry = (u64)(t >> 64);
            ++k;
        }
    }
}

// sign of A + B*sqrt(A2g)
int cmpR(i128 A, i128 B) {
    if (A == 0 && B == 0) return 0;
    if (A >= 0 && B >= 0) return 1;
    if (A <= 0 && B <= 0) return -1;
    bool aneg = A < 0;
    i128 P = aneg ? -A : A, Q = B < 0 ? -B : B;
    // compare P vs Q*sqrt(A2g)  <=>  P^2 vs Q^2*A2g (both fit in 256 bits)
    u64 a[4] = {(u64)P, (u64)((i128)P >> 64), 0, 0};
    u64 bq[4] = {(u64)Q, (u64)((i128)Q >> 64), 0, 0};
    u64 q2[8], pa2[8];
    mul256(bq, bq, q2);
    u64 aa[4] = {(u64)A2g, (u64)((i128)A2g >> 64), 0, 0};
    mul256(q2, aa, pa2);
    u64 p2[8];
    mul256(a, a, p2);
    for (int i = 7; i >= 0; --i) {
        if (p2[i] != pa2[i]) {
            bool gt = p2[i] > pa2[i];
            if (gt) return aneg ? -1 : 1;
            return aneg ? 1 : -1;
        }
    }
    return 0;
}

struct Cand {
    int t;      // 0 INT(L), 1 ALT(L), 2 DIAG(L), 3 CROSS(X2, E)
    i128 L, X2, E;
};

int cmpCand(const Cand& c1, const Cand& c2) {
    if (c1.t == 0 && c2.t == 0) return c1.L > c2.L ? 1 : (c1.L < c2.L ? -1 : 0);
    if (c1.t == 0 && c2.t == 1) {
        i128 k = c1.L, L = c2.L;
        i128 lhs = k * k * L * L, rhs = 4 * A2g;
        return lhs > rhs ? 1 : (lhs < rhs ? -1 : 0);
    }
    if (c1.t == 1 && c2.t == 0) return -cmpCand(c2, c1);
    if (c1.t == 0 && c2.t == 2) {
        i128 lhs = 2 * c1.L * c1.L, rhs = c2.L * c2.L;
        return lhs > rhs ? 1 : (lhs < rhs ? -1 : 0);
    }
    if (c1.t == 2 && c2.t == 0) return -cmpCand(c2, c1);
    if (c1.t == 0 && c2.t == 3) {
        i128 k = c1.L;
        return cmpR(4 * k * k * c2.E - c2.X2, -16 * k * k);
    }
    if (c1.t == 3 && c2.t == 0) return -cmpCand(c2, c1);
    if (c1.t == 1 && c2.t == 1)
        return c1.L > c2.L ? -1 : (c1.L < c2.L ? 1 : 0);
    if (c1.t == 1 && c2.t == 2) {
        i128 lhs = 8 * A2g, rhs = c1.L * c1.L * c2.L * c2.L;
        return lhs > rhs ? 1 : (lhs < rhs ? -1 : 0);
    }
    if (c1.t == 2 && c2.t == 1) return -cmpCand(c2, c1);
    if (c1.t == 1 && c2.t == 3) {
        return cmpR(16 * A2g * c2.E - c2.X2 * c1.L * c1.L, -64 * A2g);
    }
    if (c1.t == 3 && c2.t == 1) return -cmpCand(c2, c1);
    if (c1.t == 2 && c2.t == 2)
        return c1.L > c2.L ? 1 : (c1.L < c2.L ? -1 : 0);
    if (c1.t == 2 && c2.t == 3) {
        return cmpR(2 * c1.L * c1.L * c2.E - c2.X2, -8 * c1.L * c1.L);
    }
    if (c1.t == 3 && c2.t == 2) return -cmpCand(c2, c1);
    return cmpR(c1.X2 * c2.E - c2.X2 * c1.E, 4 * (c2.X2 - c1.X2));
}

// integer value of a candidate, or -1 if not an integer
i128 candInt(const Cand& c) {
    if (c.t == 0) return c.L;
    if (c.t == 1) {
        i128 d = isqrt128(A2g);
        if (d * d != A2g) return -1;
        if ((2 * d) % c.L != 0) return -1;
        return 2 * d / c.L;
    }
    if (c.t == 2) return -1;
    i128 d = isqrt128(A2g);
    if (d * d != A2g) return -1;
    i128 D = c.E - 4 * d;
    if (D <= 0) return -1;
    i128 den = 4 * D;
    if (c.X2 % den != 0) return -1;
    i128 k2 = c.X2 / den;
    i128 k = isqrt128(k2);
    if (k * k != k2) return -1;
    return k;
}

void vertex(i128 L1, i128 L2, i128 o, Cand* buf, int& n) {
    i128 C = L1 * L1 + L2 * L2 - o * o;
    if (C < 0) return;
    if (C == 0) {
        buf[n++] = {0, L1 > L2 ? L1 : L2, 0, 0};
        return;
    }
    i128 E = L1 * L1 + L2 * L2, C2 = C * C;
    bool le45 = C2 >= 2 * L1 * L1 * L2 * L2;
    bool cross_ok = false;
    if (!le45) {
        i128 t0 = L1 * L1 * L1 * L1 - 4 * A2g;
        i128 tB = 4 * A2g - L2 * L2 * L2 * L2;
        cross_ok = t0 >= 0 && tB <= 0;
    } else {
        i128 w1 = 2 * L1 * L1 - C, w2 = 2 * L2 * L2 - C;
        bool ok1 = w1 <= 0 || 16 * A2g >= w1 * w1;
        bool ok2 = w2 <= 0 || 16 * A2g >= w2 * w2;
        cross_ok = ok1 && ok2;
    }
    if (cross_ok) {
        buf[n++] = {3, 0, C2, E};
    } else if (!le45) {
        i128 l1 = L1 * L1 * L1 * L1, l2 = L2 * L2 * L2 * L2;
        if (l1 >= 4 * A2g) buf[n++] = {0, L1, 0, 0};
        else buf[n++] = {1, L1, 0, 0};
        if (l2 >= 4 * A2g) buf[n++] = {0, L2, 0, 0};
        else buf[n++] = {1, L2, 0, 0};
    } else {
        i128 w1 = 2 * L1 * L1 - C, w2 = 2 * L2 * L2 - C;
        bool ok1 = w1 <= 0 || 16 * A2g >= w1 * w1;
        bool ok2 = w2 <= 0 || 16 * A2g >= w2 * w2;
        if (!ok2) buf[n++] = {2, L2, 0, 0};
        if (!ok1) buf[n++] = {2, L1, 0, 0};
    }
}

std::unordered_set<u64> seen;
i128 total;

// Check triangle (a, b, c): if its minimum bounding square has integer side
// k in [1, N], add the perimeter (once).
void checkAcc(i128 a, i128 b, i128 c) {
    if (a + b <= c || a + c <= b || b + c <= a) return;
    i128 s = a + b + c;
    A2g = s * (b + c - a) * (a + c - b) * (a + b - c) / 16;
    if (A2g <= 0) return;
    Cand buf[12];
    int n = 0;
    vertex(a, b, c, buf, n);
    vertex(b, c, a, buf, n);
    vertex(c, a, b, buf, n);
    if (n == 0) return;
    Cand mn = buf[0];
    for (int i = 1; i < n; ++i)
        if (cmpCand(buf[i], mn) < 0) mn = buf[i];
    i128 k = candInt(mn);
    if (k < 1 || k > N) return;
    i128 x = a, y = b, z = c;
    if (x > y) std::swap(x, y);
    if (y > z) std::swap(y, z);
    if (x > y) std::swap(x, y);
    u64 key = (u64)x << 42 | (u64)y << 21 | (u64)z;
    if (seen.insert(key).second) total += a + b + c;
}

std::vector<std::vector<std::pair<u32, u32>>> groups;

}  // namespace

int main(int argc, char** argv) {
    if (argc > 1) {
        N = atoll(argv[1]);
        MAXSIDE = (long long)(N * std::sqrt(2.0));
    }
    groups.resize(N + 1);
    for (long long m = 1; m * m <= MAXSIDE; ++m) {
        for (long long n = 1; n < m; ++n) {
            if ((m - n) % 2 == 0) continue;
            if (std::gcd(m, n) != 1) continue;
            long long u = m * m - n * n, v = 2 * m * n, hyp = m * m + n * n;
            if (hyp > MAXSIDE) continue;
            long long maxd = MAXSIDE / hyp;
            for (long long d = 1; d <= maxd; ++d) {
                long long x = d * u, y = d * v, A = d * hyp;
                if (x <= N) groups[x].emplace_back((u32)y, (u32)A);
                if (y <= N) groups[y].emplace_back((u32)x, (u32)A);
            }
        }
    }
    std::fprintf(stderr, "groups built\n");

    seen.reserve(8'000'000);
    total = 0;
    for (long long h = 1; h <= N; ++h) {
        auto& g = groups[h];
        if (g.empty()) continue;
        g.emplace_back(0u, (u32)h);
        std::sort(g.begin(), g.end());
        int sz = (int)g.size();
        for (int i = 0; i < sz; ++i) {
            i128 p1 = g[i].first, A1 = g[i].second;
            for (int j = i; j < sz; ++j) {
                i128 p2 = g[j].first, A2 = g[j].second;
                // ALT: L = p1+p2
                i128 L = p1 + p2;
                if (L >= 1 && L <= h && L <= MAXSIDE)
                    checkAcc(A1, A2, L);
                // ALT: L = |p1-p2|
                L = p1 > p2 ? p1 - p2 : p2 - p1;
                if (L >= 1 && L <= h && L <= MAXSIDE)
                    checkAcc(A1, A2, L);
                // CROSS: o^2 = (h-p1)^2 + (h-p2)^2
                i128 w1 = h - p1, w2 = h - p2;
                i128 o2 = w1 * w1 + w2 * w2;
                if (o2 >= 1) {
                    i128 o = isqrt128(o2);
                    if (o * o == o2 && o <= MAXSIDE)
                        checkAcc(A1, A2, o);
                }
            }
        }
        if (h % 100000 == 0)
            std::fprintf(stderr, "h=%lld total=%lld seen=%zu\n", h,
                         (long long)total, seen.size());
    }
    std::printf("%lld\n", (long long)total);
    return 0;
}
