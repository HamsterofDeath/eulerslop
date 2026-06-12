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
#include <map>
#include <vector>

struct Transition {
    int next;
    int count;
    long double weight;
};

static long double factorial(int n) {
    long double result = 1.0L;
    for (int i = 2; i <= n; ++i) result *= i;
    return result;
}

static void enumerate_states(int position,
                             int length,
                             int cap,
                             int sum,
                             std::vector<int>& current,
                             std::vector<std::vector<int>>& states) {
    if (position == length) {
        states.push_back(current);
        return;
    }
    for (int count = 0; sum + count <= cap; ++count) {
        current.push_back(count);
        enumerate_states(position + 1, length, cap, sum + count, current, states);
        current.pop_back();
    }
}

static long double expected_people(int days, int distance, int target) {
    const int window = distance + 1;
    const int cap = target - 1;
    const int state_length = window - 1;
    const int max_degree = cap * days;

    std::vector<std::vector<int>> states;
    std::vector<int> current;
    enumerate_states(0, state_length, cap, 0, current, states);

    std::map<std::vector<int>, int> state_index;
    for (int i = 0; i < (int)states.size(); ++i) state_index[states[i]] = i;

    std::vector<std::vector<Transition>> transitions(states.size());
    for (int i = 0; i < (int)states.size(); ++i) {
        int sum = 0;
        for (int x : states[i]) sum += x;
        for (int count = 0; sum + count <= cap; ++count) {
            std::vector<int> next;
            if (state_length > 0) {
                next.insert(next.end(), states[i].begin() + 1, states[i].end());
                next.push_back(count);
            }
            transitions[i].push_back({state_index[next], count, 1.0L / factorial(count)});
        }
    }

    std::vector<long double> coefficients((size_t)max_degree + 1, 0.0L);
    const int state_count = (int)states.size();

    for (int start = 0; start < state_count; ++start) {
        std::vector<std::vector<long double>> dp(
            state_count, std::vector<long double>((size_t)max_degree + 1, 0.0L));
        std::vector<std::vector<long double>> next(
            state_count, std::vector<long double>((size_t)max_degree + 1, 0.0L));
        dp[start][0] = 1.0L;

        for (int step = 0; step < days; ++step) {
            for (auto& row : next) std::fill(row.begin(), row.end(), 0.0L);
            const int degree_limit = std::min(max_degree, cap * step);

            for (int state = 0; state < state_count; ++state) {
                for (int degree = 0; degree <= degree_limit; ++degree) {
                    const long double value = dp[state][degree];
                    if (value == 0.0L) continue;
                    for (const auto& transition : transitions[state]) {
                        next[transition.next][degree + transition.count] +=
                            value * transition.weight;
                    }
                }
            }
            dp.swap(next);
        }

        for (int degree = 0; degree <= max_degree; ++degree) {
            coefficients[degree] += dp[start][degree];
        }
    }

    long double expectation = 0.0L;
    long double fact = 1.0L;
    long double day_power = 1.0L;
    for (int people = 0; people <= max_degree; ++people) {
        if (people > 0) {
            fact *= people;
            day_power *= days;
        }
        expectation += coefficients[people] * fact / day_power;
    }
    return expectation;
}

int main(int argc, char** argv) {
    int days = argc > 1 ? std::stoi(argv[1]) : 365;
    int distance = argc > 2 ? std::stoi(argv[2]) : 7;
    int target = argc > 3 ? std::stoi(argv[3]) : 4;
    std::cout << std::fixed << std::setprecision(8)
              << expected_people(days, distance, target) << '\n';
    return 0;
}
"""


def _binary():
    digest = hashlib.sha256(CPP_SOURCE.encode()).hexdigest()[:16]
    root = Path(tempfile.gettempdir()) / "eulerslop_build"
    root.mkdir(exist_ok=True)
    src = root / f"p584_{digest}.cpp"
    exe = root / f"p584_{digest}"
    if not exe.exists():
        src.write_text(CPP_SOURCE)
        subprocess.run(
            ["g++", "-O3", "-march=native", "-std=c++17", str(src), "-o", str(exe)],
            check=True,
        )
    return exe


def expected_people(days, distance, target):
    result = subprocess.run(
        [str(_binary()), str(days), str(distance), str(target)],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def solve():
    assert expected_people(10, 1, 3) == "5.78688636"
    assert expected_people(100, 7, 3) == "8.48967364"
    return expected_people(365, 7, 4)


if __name__ == "__main__":
    print(solve())
