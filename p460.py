#!/usr/bin/env python3

import subprocess
import tempfile
from pathlib import Path


SOURCE = r"""
#include <bits/stdc++.h>
using namespace std;

struct Node {
    int x;
    int y;
};

double segment_time(const Node& a, const Node& b) {
    double dx = b.x - a.x;
    double dy = b.y - a.y;
    double distance = hypot(dx, dy);
    if (dy == 0.0) return distance / a.y;
    return distance * log((double)b.y / a.y) / dy;
}

double quickest_time(int d, int band, int max_dx) {
    double radius = sqrt((d / 2.0) * (d / 2.0) + 1.0);
    double center_x = d / 2.0;

    vector<Node> nodes;
    vector<vector<int>> by_x(d + 1);
    unordered_map<unsigned long long, int> index;
    index.reserve((size_t)(d + 1) * (2 * band + 8));

    for (int x = 0; x <= d; ++x) {
        double on_geodesic = sqrt(max(0.0, radius * radius - (x - center_x) * (x - center_x)));
        int middle = (int)llround(on_geodesic);
        vector<int> heights;
        heights.push_back(1);
        for (int y = max(1, middle - band); y <= middle + band; ++y) {
            heights.push_back(y);
        }
        if (x == 0 || x == d) {
            int top = *max_element(heights.begin(), heights.end());
            for (int y = 1; y <= top; ++y) heights.push_back(y);
        }
        sort(heights.begin(), heights.end());
        heights.erase(unique(heights.begin(), heights.end()), heights.end());

        for (int y : heights) {
            int id = (int)nodes.size();
            nodes.push_back({x, y});
            by_x[x].push_back(id);
            index[((unsigned long long)(unsigned int)x << 32) | (unsigned int)y] = id;
        }
    }

    int start = index[1U];
    int target = index[((unsigned long long)(unsigned int)d << 32) | 1U];
    vector<double> distance(nodes.size(), 1e100);
    distance[start] = 0.0;
    priority_queue<pair<double, int>, vector<pair<double, int>>, greater<pair<double, int>>> queue;
    queue.push({0.0, start});

    while (!queue.empty()) {
        auto [current_distance, id] = queue.top();
        queue.pop();
        if (current_distance != distance[id]) continue;
        if (id == target) return current_distance;

        Node here = nodes[id];
        for (int next : by_x[here.x]) {
            if (abs(nodes[next].y - here.y) == 1) {
                double candidate = current_distance + segment_time(here, nodes[next]);
                if (candidate < distance[next]) {
                    distance[next] = candidate;
                    queue.push({candidate, next});
                }
            }
        }

        int last_x = min(d, here.x + max_dx);
        for (int x = here.x + 1; x <= last_x; ++x) {
            for (int next : by_x[x]) {
                double candidate = current_distance + segment_time(here, nodes[next]);
                if (candidate < distance[next]) {
                    distance[next] = candidate;
                    queue.push({candidate, next});
                }
            }
        }
    }
    return distance[target];
}

int main() {
    cout.setf(ios::fixed);
    cout << setprecision(12);
    cout << quickest_time(4, 2, 5) << '\n';
    cout << quickest_time(10, 2, 5) << '\n';
    cout << quickest_time(100, 4, 10) << '\n';
    cout << quickest_time(10000, 30, 80) << '\n';
    cout << quickest_time(10000, 40, 80) << '\n';
    return 0;
}
"""


def rounded(value):
    return f"{float(value):.9f}"


def run_solver():
    with tempfile.TemporaryDirectory(prefix="p460_") as tmp:
        tmp_path = Path(tmp)
        cpp = tmp_path / "p460.cpp"
        exe = tmp_path / "p460"
        cpp.write_text(SOURCE)
        subprocess.run(
            ["g++", "-O3", "-std=c++17", str(cpp), "-o", str(exe)],
            check=True,
        )
        result = subprocess.run(
            [str(exe)],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        )
    return result.stdout.strip().splitlines()


def solve():
    sample_4, sample_10, sample_100, target_30, target_40 = run_solver()
    assert rounded(sample_4) == "2.960516287"
    assert rounded(sample_10) == "4.668187834"
    assert rounded(sample_100) == "9.217221972"
    assert rounded(target_30) == rounded(target_40)
    return rounded(target_30)


if __name__ == "__main__":
    print(solve())
