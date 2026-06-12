#!/usr/bin/env python3
import hashlib
import subprocess
import tempfile
from pathlib import Path


CPP_SOURCE = r"""
#include <algorithm>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <queue>
#include <utility>
#include <vector>

struct Interval {
    long double start;
    long double end;
    int prime_index;
    int step;
};

static std::vector<int> primes_upto(int limit) {
    std::vector<int> primes;
    for (int n = 2; n <= limit; ++n) {
        bool prime = true;
        for (int p : primes) {
            if (p * p > n) break;
            if (n % p == 0) {
                prime = false;
                break;
            }
        }
        if (prime) primes.push_back(n);
    }
    return primes;
}

static bool covers_all_starts(int prime, long double gap, int steps) {
    const long double jump = 1.0L / std::sqrt((long double)prime);
    const long double high = 1.0L - gap;
    std::vector<std::pair<long double, long double>> intervals;
    intervals.reserve((size_t)steps);

    long double position = 0.0L;
    for (int k = 1; k <= steps; ++k) {
        position += jump;
        position -= std::floor(position);
        const long double start = std::max(0.0L, position - gap);
        const long double end = std::min(position, high);
        if (start <= end) intervals.push_back({start, end});
    }

    std::sort(intervals.begin(), intervals.end());
    long double covered = 0.0L;
    const long double eps = 1e-18L;
    for (auto [start, end] : intervals) {
        if (start > covered + eps) return false;
        if (end > covered) covered = end;
        if (covered >= high - eps) return true;
    }
    return covered >= high - eps;
}

static int covering_steps(int prime, long double gap) {
    int high = 1;
    while (!covers_all_starts(prime, gap, high)) high *= 2;

    int low = high / 2 + 1;
    while (low < high) {
        const int mid = low + (high - low) / 2;
        if (covers_all_starts(prime, gap, mid)) {
            high = mid;
        } else {
            low = mid + 1;
        }
    }
    return low;
}

static long double M(int prime_limit, long double gap) {
    const auto primes = primes_upto(prime_limit);
    const long double high = 1.0L - gap;

    std::vector<Interval> intervals;
    std::vector<long double> coordinates;
    coordinates.push_back(0.0L);
    coordinates.push_back(high);

    for (int i = 0; i < (int)primes.size(); ++i) {
        const int prime = primes[i];
        const int steps = covering_steps(prime, gap);
        const long double jump = 1.0L / std::sqrt((long double)prime);

        long double position = 0.0L;
        for (int k = 1; k <= steps; ++k) {
            position += jump;
            position -= std::floor(position);
            const long double start = std::max(0.0L, position - gap);
            const long double end = std::min(position, high);
            if (start <= end) {
                intervals.push_back({start, end, i, k});
                coordinates.push_back(start);
                coordinates.push_back(end);
            }
        }
    }

    std::sort(intervals.begin(), intervals.end(),
              [](const Interval& a, const Interval& b) {
                  return a.start < b.start;
              });
    std::sort(coordinates.begin(), coordinates.end());
    coordinates.erase(std::unique(coordinates.begin(), coordinates.end()),
                      coordinates.end());

    using HeapItem = std::pair<int, long double>; // first hit step, interval end
    std::vector<std::priority_queue<HeapItem, std::vector<HeapItem>, std::greater<HeapItem>>>
        active(primes.size());

    long double best = 0.0L;
    size_t next_interval = 0;
    const long double eps = 1e-18L;

    auto update_best = [&](long double coordinate, bool include_endpoint) {
        long double value = 0.0L;
        for (int i = 0; i < (int)primes.size(); ++i) {
            auto& heap = active[i];
            while (!heap.empty() &&
                   (include_endpoint ? heap.top().second < coordinate - eps
                                     : heap.top().second <= coordinate + eps)) {
                heap.pop();
            }
            if (heap.empty()) return;
            value += (long double)heap.top().first / std::sqrt((long double)primes[i]);
        }
        if (value > best) best = value;
    };

    for (long double coordinate : coordinates) {
        while (next_interval < intervals.size() &&
               intervals[next_interval].start <= coordinate + eps) {
            const auto& interval = intervals[next_interval++];
            active[(size_t)interval.prime_index].push({interval.step, interval.end});
        }

        update_best(coordinate, true);
        update_best(coordinate, false);
    }

    return best;
}

int main(int argc, char** argv) {
    int prime_limit = argc > 1 ? std::stoi(argv[1]) : 100;
    long double gap = argc > 2 ? std::stold(argv[2]) : 0.00002L;
    std::cout << std::fixed << std::setprecision(4) << M(prime_limit, gap) << '\n';
    return 0;
}
"""


def _binary():
    digest = hashlib.sha256(CPP_SOURCE.encode()).hexdigest()[:16]
    root = Path(tempfile.gettempdir()) / "eulerslop_build"
    root.mkdir(exist_ok=True)
    src = root / f"p576_{digest}.cpp"
    exe = root / f"p576_{digest}"
    if not exe.exists():
        src.write_text(CPP_SOURCE)
        subprocess.run(
            ["g++", "-O3", "-march=native", "-std=c++17", str(src), "-o", str(exe)],
            check=True,
        )
    return exe


def M(prime_limit, gap):
    result = subprocess.run(
        [str(_binary()), str(prime_limit), str(gap)],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def solve():
    assert M(10, "0.01") == "266.9010"
    return M(100, "0.00002")


if __name__ == "__main__":
    print(solve())
