#!/usr/bin/env python3

import subprocess
import tempfile
from pathlib import Path


SOURCE = r"""
#include <bits/stdc++.h>
using namespace std;

static const int MOD = 1000000000;

struct State {
    array<int, 3> degree;
    array<int, 3> label;
    bool operator<(const State& other) const {
        return tie(degree, label) < tie(other.degree, other.label);
    }
};

struct VState {
    vector<int> degree;
    vector<int> label;
    bool operator<(const VState& other) const {
        return tie(degree, label) < tie(other.degree, other.label);
    }
};

VState canonical(vector<int> degree, vector<int> label) {
    map<int, int> remap;
    int next = 0;
    for (int& value : label) {
        if (!remap.count(value)) remap[value] = next++;
        value = remap[value];
    }
    return {degree, label};
}

State to_fixed(const VState& state) {
    State result;
    for (int i = 0; i < 3; ++i) {
        result.degree[i] = state.degree[i];
        result.label[i] = state.label[i];
    }
    return result;
}

vector<VState> transition_state(const VState& state, int i, int n) {
    vector<int> degree = state.degree;
    vector<int> label = state.label;
    if (i + 3 <= n) {
        degree.push_back(0);
        label.push_back(label.empty() ? 0 : *max_element(label.begin(), label.end()) + 1);
    }

    int length = (int)degree.size();
    int target_degree = (i == 1 || i == n) ? 1 : 2;
    int need = target_degree - degree[0];
    vector<VState> result;
    if (need < 0 || need > length - 1) return result;

    for (int mask = 0; mask < (1 << (length - 1)); ++mask) {
        if (__builtin_popcount((unsigned)mask) != need) continue;
        vector<int> next_degree = degree;
        vector<int> next_label = label;
        bool ok = true;
        next_degree[0] += need;

        for (int bit = 0; bit < length - 1 && ok; ++bit) {
            if (((mask >> bit) & 1) == 0) continue;
            int offset = bit + 1;
            int vertex = i + offset;
            int future_target = (vertex == 1 || vertex == n) ? 1 : 2;
            ++next_degree[offset];
            if (next_degree[offset] > future_target || next_label[0] == next_label[offset]) {
                ok = false;
                break;
            }
            int old_label = next_label[offset];
            int new_label = next_label[0];
            for (int& value : next_label) {
                if (value == old_label) value = new_label;
            }
        }
        if (!ok) continue;

        int component = next_label[0];
        bool component_survives = false;
        for (int j = 1; j < length; ++j) {
            if (next_label[j] == component) component_survives = true;
        }

        vector<int> reduced_degree(next_degree.begin() + 1, next_degree.end());
        vector<int> reduced_label(next_label.begin() + 1, next_label.end());
        if (!component_survives && i < n) continue;
        if (i == n && !reduced_degree.empty()) continue;
        result.push_back(canonical(reduced_degree, reduced_label));
    }
    return result;
}

vector<State> middle_transition(const State& state) {
    vector<int> degree = {state.degree[0], state.degree[1], state.degree[2], 0};
    vector<int> label = {
        state.label[0], state.label[1], state.label[2],
        max({state.label[0], state.label[1], state.label[2]}) + 1
    };

    int need = 2 - degree[0];
    vector<State> result;
    if (need < 0 || need > 3) return result;

    for (int mask = 0; mask < 8; ++mask) {
        if (__builtin_popcount((unsigned)mask) != need) continue;
        vector<int> next_degree = degree;
        vector<int> next_label = label;
        bool ok = true;
        next_degree[0] += need;

        for (int bit = 0; bit < 3 && ok; ++bit) {
            if (((mask >> bit) & 1) == 0) continue;
            int offset = bit + 1;
            ++next_degree[offset];
            if (next_degree[offset] > 2 || next_label[0] == next_label[offset]) {
                ok = false;
                break;
            }
            int old_label = next_label[offset];
            int new_label = next_label[0];
            for (int& value : next_label) {
                if (value == old_label) value = new_label;
            }
        }
        if (!ok) continue;

        int component = next_label[0];
        bool component_survives = false;
        for (int j = 1; j < 4; ++j) {
            if (next_label[j] == component) component_survives = true;
        }
        if (!component_survives) continue;

        result.push_back(to_fixed(canonical(
            {next_degree[1], next_degree[2], next_degree[3]},
            {next_label[1], next_label[2], next_label[3]}
        )));
    }
    return result;
}

using Matrix = vector<vector<int>>;

Matrix multiply(const Matrix& a, const Matrix& b) {
    int n = (int)a.size();
    Matrix result(n, vector<int>(n));
    for (int i = 0; i < n; ++i) {
        for (int k = 0; k < n; ++k) {
            if (a[i][k] == 0) continue;
            long long left = a[i][k];
            for (int j = 0; j < n; ++j) {
                if (b[k][j]) result[i][j] = (result[i][j] + left * b[k][j]) % MOD;
            }
        }
    }
    return result;
}

vector<int> multiply_vector(const Matrix& matrix, const vector<int>& vector_) {
    int n = (int)matrix.size();
    vector<int> result(n);
    for (int i = 0; i < n; ++i) {
        long long total = 0;
        for (int j = 0; j < n; ++j) {
            if (matrix[i][j] && vector_[j]) {
                total = (total + 1LL * matrix[i][j] * vector_[j]) % MOD;
            }
        }
        result[i] = (int)total;
    }
    return result;
}

vector<int> power_apply(Matrix matrix, unsigned long long exponent, vector<int> vector_) {
    while (exponent) {
        if (exponent & 1ULL) vector_ = multiply_vector(matrix, vector_);
        exponent >>= 1ULL;
        if (exponent) matrix = multiply(matrix, matrix);
    }
    return vector_;
}

long long direct_f(int n) {
    if (n == 1) return 1;
    map<VState, long long> states;
    states[canonical({0, 0, 0}, {0, 1, 2})] = 1;
    for (int i = 1; i <= n; ++i) {
        map<VState, long long> next;
        for (auto const& [state, count] : states) {
            for (const VState& out : transition_state(state, i, n)) {
                next[out] += count;
            }
        }
        states.swap(next);
    }
    long long result = 0;
    for (auto const& [state, count] : states) result += count;
    return result;
}

int solve_limit(unsigned long long limit) {
    VState initial = canonical({0, 0, 0}, {0, 1, 2});
    vector<VState> after_start = transition_state(initial, 1, 100);

    set<State> seen;
    queue<State> pending;
    for (const VState& state : after_start) {
        State fixed = to_fixed(state);
        if (seen.insert(fixed).second) pending.push(fixed);
    }
    while (!pending.empty()) {
        State current = pending.front();
        pending.pop();
        for (const State& next : middle_transition(current)) {
            if (seen.insert(next).second) pending.push(next);
        }
    }

    vector<State> states(seen.begin(), seen.end());
    map<State, int> state_index;
    for (int i = 0; i < (int)states.size(); ++i) state_index[states[i]] = i;
    int state_count = (int)states.size();

    vector<vector<pair<int, int>>> transition(state_count);
    for (int i = 0; i < state_count; ++i) {
        map<int, int> counts;
        for (const State& next : middle_transition(states[i])) {
            ++counts[state_index[next]];
        }
        transition[i].assign(counts.begin(), counts.end());
    }

    vector<int> start_vector(state_count);
    for (const VState& state : after_start) ++start_vector[state_index[to_fixed(state)]];

    vector<int> tail(state_count);
    for (int i = 0; i < state_count; ++i) {
        VState state = {
            {states[i].degree[0], states[i].degree[1], states[i].degree[2]},
            {states[i].label[0], states[i].label[1], states[i].label[2]}
        };
        map<VState, long long> dp;
        dp[state] = 1;
        for (int step : {98, 99, 100}) {
            map<VState, long long> next;
            for (auto const& [current, count] : dp) {
                for (const VState& out : transition_state(current, step, 100)) {
                    next[out] += count;
                }
            }
            dp.swap(next);
        }
        for (auto const& [unused, count] : dp) tail[i] += (int)count;
    }

    vector<array<int, 3>> basis;
    map<array<int, 3>, int> basis_index;
    for (int i = 0; i < state_count; ++i) {
        for (int j = i; j < state_count; ++j) {
            for (int k = j; k < state_count; ++k) {
                basis_index[{i, j, k}] = (int)basis.size();
                basis.push_back({i, j, k});
            }
        }
    }

    int basis_count = (int)basis.size();
    int matrix_size = basis_count + 1;
    Matrix matrix(matrix_size, vector<int>(matrix_size));

    vector<vector<int>> dense_transition(state_count, vector<int>(state_count));
    for (int source = 0; source < state_count; ++source) {
        for (auto [target, count] : transition[source]) dense_transition[target][source] = count;
    }

    for (int target = 0; target < basis_count; ++target) {
        auto [a, b, c] = basis[target];
        for (int source = 0; source < basis_count; ++source) {
            array<int, 3> base = basis[source];
            sort(base.begin(), base.end());
            long long coeff = 0;
            do {
                coeff += (
                    1LL * dense_transition[a][base[0]]
                    * dense_transition[b][base[1]] % MOD
                    * dense_transition[c][base[2]]
                );
            } while (next_permutation(base.begin(), base.end()));
            matrix[target][source] = coeff % MOD;
        }
    }

    for (int source = 0; source < basis_count; ++source) {
        auto [i, j, k] = basis[source];
        long long coeff = 1LL * tail[i] * tail[j] % MOD * tail[k] % MOD;
        int multiplicity = (i == k) ? 1 : ((i == j || j == k) ? 3 : 6);
        matrix[basis_count][source] = coeff * multiplicity % MOD;
    }
    matrix[basis_count][basis_count] = 1;

    vector<int> vector_(matrix_size);
    for (int i = 0; i < state_count; ++i) {
        for (int j = i; j < state_count; ++j) {
            for (int k = j; k < state_count; ++k) {
                vector_[basis_index[{i, j, k}]] =
                    1LL * start_vector[i] * start_vector[j] % MOD * start_vector[k] % MOD;
            }
        }
    }

    if (limit <= 3) return (int)limit;
    vector<int> result = power_apply(matrix, limit - 3, vector_);
    return (3 + result[basis_count]) % MOD;
}

int main() {
    if (direct_f(6) != 14) return 1;
    if (direct_f(10) != 254) return 2;
    if (direct_f(40) != 1439682432976LL) return 3;
    cout << solve_limit(10) << '\n';
    cout << solve_limit(20) << '\n';
    cout << solve_limit(1000) << '\n';
    cout << solve_limit(1000000) << '\n';
    cout << solve_limit(100000000000000ULL) << '\n';
    return 0;
}
"""


def run_solver():
    with tempfile.TemporaryDirectory(prefix="p490_") as tmp:
        tmp_path = Path(tmp)
        cpp = tmp_path / "p490.cpp"
        exe = tmp_path / "p490"
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
    sample_10, sample_20, sample_1000, sample_1000000, answer = run_solver()
    assert sample_10 == "18230635"
    assert sample_20 == "192114219"
    assert sample_1000 == "225031475"
    assert sample_1000000 == "363486179"
    return answer


if __name__ == "__main__":
    print(solve())
