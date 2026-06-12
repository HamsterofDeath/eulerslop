#!/usr/bin/env python3
import hashlib
import subprocess
import tempfile
from pathlib import Path


CPP_SOURCE = r"""
#include <bits/stdc++.h>
using namespace std;

static long long floor_div(long long a, long long b) {
    if (a >= 0) return a / b;
    return -((-a + b - 1) / b);
}

static int count_strictly_right(int order, int x1, int y1, int x2, int y2) {
    int dx = x2 - x1;
    int dy = y2 - y1;
    int total = 0;

    for (int y = 0; y <= order; ++y) {
        long long a = (long long)dx * (y - y1) + (long long)dy * x1;
        if (dy == 0) {
            if (a < 0) total += order + 1;
        } else if (dy > 0) {
            long long min_x = floor_div(a, dy) + 1;
            if (min_x < 0) min_x = 0;
            if (min_x <= order) total += order - (int)min_x + 1;
        } else {
            long long b = -dy;
            long long c = -a;
            if (c > 0) {
                long long max_x = (c - 1) / b;
                if (max_x > order) max_x = order;
                total += (int)max_x + 1;
            }
        }
    }

    return total;
}

static int collinear_outside_segment(int order, int x1, int y1, int x2, int y2) {
    int dx = x2 - x1;
    int dy = y2 - y1;
    int g = gcd(abs(dx), abs(dy));
    int sx = dx / g;
    int sy = dy / g;

    auto steps_inside = [order](int x, int y, int step_x, int step_y) {
        int limit = INT_MAX;
        if (step_x > 0) limit = min(limit, (order - x) / step_x);
        if (step_x < 0) limit = min(limit, x / (-step_x));
        if (step_y > 0) limit = min(limit, (order - y) / step_y);
        if (step_y < 0) limit = min(limit, y / (-step_y));
        return limit == INT_MAX ? 0 : limit;
    };

    int forward = steps_inside(x1, y1, sx, sy);
    int backward = steps_inside(x1, y1, -sx, -sy);
    int points_on_line = forward + backward + 1;
    return points_on_line - (g + 1);
}

static long double expected_area(int order) {
    vector<pair<int, int>> points;
    for (int x = 0; x <= order; ++x) {
        for (int y = 0; y <= order; ++y) {
            points.push_back({x, y});
        }
    }

    int point_count = (int)points.size();
    long double pin_probability = 1.0L / (order + 1);
    long double absent_probability = 1.0L - pin_probability;

    vector<long double> absent_power(point_count + 1, 1.0L);
    for (int i = 1; i <= point_count; ++i) {
        absent_power[i] = absent_power[i - 1] * absent_probability;
    }

    long double double_area = 0.0L;
    for (auto [x1, y1] : points) {
        for (auto [x2, y2] : points) {
            if (x1 == x2 && y1 == y2) continue;

            int right = count_strictly_right(order, x1, y1, x2, y2);
            int outside = collinear_outside_segment(order, x1, y1, x2, y2);
            long double determinant = (long double)x1 * y2 - (long double)y1 * x2;
            long double probability =
                pin_probability * pin_probability * absent_power[right + outside];
            double_area += determinant * probability;
        }
    }

    return double_area / 2.0L;
}

int main(int argc, char** argv) {
    int order = 100;
    if (argc > 1) order = stoi(argv[1]);
    cout.setf(ios::fixed);
    cout << setprecision(5) << (double)expected_area(order) << '\n';
    return 0;
}
"""


def _binary():
    digest = hashlib.sha256(CPP_SOURCE.encode()).hexdigest()[:16]
    root = Path(tempfile.gettempdir()) / "eulerslop_build"
    root.mkdir(exist_ok=True)
    src = root / f"p514_{digest}.cpp"
    exe = root / f"p514_{digest}"
    if not exe.exists():
        src.write_text(CPP_SOURCE)
        subprocess.run(
            ["g++", "-O3", "-march=native", "-std=c++17", str(src), "-o", str(exe)],
            check=True,
        )
    return exe


def E(order):
    result = subprocess.run(
        [str(_binary()), str(order)],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def solve():
    assert E(1) == "0.18750"
    assert E(2) == "0.94335"
    assert E(10) == "55.03013"
    return E(100)


if __name__ == "__main__":
    print(solve())
