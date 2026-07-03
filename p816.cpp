// Project Euler 816: sweep-line closest pair for the generated points.
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <iomanip>
#include <iostream>
#include <set>
#include <vector>

using namespace std;

struct Point {
    int x;
    int y;
};

static vector<Point> points(int count) {
    vector<Point> pts;
    pts.reserve(count);
    uint64_t s = 290797;
    for (int i = 0; i < count; ++i) {
        int x = (int)s;
        s = s * s % 50515093;
        int y = (int)s;
        s = s * s % 50515093;
        pts.push_back({x, y});
    }
    return pts;
}

static inline int64_t dist2(const Point& a, const Point& b) {
    int64_t dx = (int64_t)a.x - b.x;
    int64_t dy = (int64_t)a.y - b.y;
    return dx * dx + dy * dy;
}

static int64_t closest_squared(vector<Point> pts) {
    sort(pts.begin(), pts.end(), [](const Point& a, const Point& b) {
        return a.x == b.x ? a.y < b.y : a.x < b.x;
    });

    int64_t best = dist2(pts[0], pts[1]);
    for (size_t i = 1; i < pts.size(); ++i)
        best = min(best, dist2(pts[i - 1], pts[i]));

    set<pair<int, int>> active;  // (y, x)
    size_t left = 0;
    for (const Point& p : pts) {
        int64_t limit = (int64_t)sqrt((long double)best) + 1;
        while (left < pts.size()) {
            int64_t dx = (int64_t)p.x - pts[left].x;
            if (dx * dx <= best) break;
            active.erase({pts[left].y, pts[left].x});
            ++left;
        }

        auto lo = active.lower_bound({(int)(p.y - limit), -1000000000});
        auto hi = active.upper_bound({(int)(p.y + limit), 1000000000});
        for (auto it = lo; it != hi; ++it) {
            Point q{it->second, it->first};
            best = min(best, dist2(p, q));
        }
        active.insert({p.y, p.x});
    }
    return best;
}

int main() {
    double sample = sqrt((long double)closest_squared(points(14)));
    if (fabsl(sample - 546446.466846479L) > 1e-6L) {
        fprintf(stderr, "self-test failed: %.12f\n", sample);
        return 1;
    }

    long double answer = sqrt((long double)closest_squared(points(2000000)));
    cout << fixed << setprecision(9) << (double)answer << "\n";
    return 0;
}
