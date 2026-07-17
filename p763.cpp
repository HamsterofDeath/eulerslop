// Project Euler 763: amoebas in a 3D grid.
//
// A reachable arrangement is the exposed boundary of a finite order ideal in
// the positive cubic lattice.  Slice that stepped surface diagonally and encode
// its boundary by a path.  The two possible end types are stored in u[n][k]
// and v[n][k], where n is the active boundary length and 1 <= k <= n.  The
// local path extensions give the recurrence below.  Only n with triangular
// offset (n+1)(n+2)/2 <= N-1 can occur, so the state count is O(N^2).

#include <algorithm>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <vector>

using namespace std;

static constexpr uint64_t MOD = 1'000'000'000ULL;

static uint32_t arrangements(int divisions) {
    if (divisions < 1) throw invalid_argument("divisions must be positive");

    // a[m] is D(m+1), so the requested final index is divisions-1.
    const int last = divisions - 1;
    int first_inactive = 0;
    while ((first_inactive + 1LL) * (first_inactive + 2) / 2 <= last) {
        ++first_inactive;
    }
    const int max_active = first_inactive - 1;
    const int state_limit = max_active + 3;

    vector<int> offset(state_limit + 2);
    vector<int> length(state_limit + 2);
    for (int n = 0; n < state_limit + 2; ++n) {
        offset[n] = (n + 1) * (n + 2) / 2;
        length[n] = max(0, last - offset[n] + 1);
    }

    vector<vector<uint32_t>> u(state_limit + 2);
    vector<vector<uint32_t>> v(state_limit + 2);
    for (int n = 1; n < state_limit + 2; ++n) {
        u[n].resize((size_t)n * length[n]);
        v[n].resize((size_t)n * length[n]);
    }

    vector<uint32_t> boundary(last + 1);
    vector<uint32_t> a(last + 1);
    a[0] = 1;

    int active = 0;
    for (int m = 0; m <= last; ++m) {
        while (active + 1 < state_limit + 1 &&
               offset[active + 1] <= m) {
            ++active;
        }

        for (int n = 1; n <= active; ++n) {
            const int len = length[n];
            const int current = m - offset[n];
            const int previous = current - n - 2;
            const int upper_previous = current - 2 * n - 5;
            const int lower_current = current;
            const int upper_len = length[n + 1];
            const int lower_len = length[n - 1];

            if (n == 1) {
                uint64_t next_u = 0;
                if (previous >= 0) {
                    next_u += 2ULL * u[1][previous] + v[1][previous];
                }
                if (upper_previous >= 0 && upper_len > 0) {
                    next_u += v[2][upper_previous];
                    next_u += u[2][upper_len + upper_previous];
                }
                const int boundary_index = m - 2;
                if (boundary_index >= 0) next_u += boundary[boundary_index];
                u[1][current] = next_u % MOD;

                uint64_t next_v = 0;
                if (previous >= 0) {
                    next_v += 2ULL * v[1][previous];
                    next_v += 2ULL * u[1][previous];
                }
                if (upper_previous >= 0 && upper_len > 0) {
                    next_v += v[2][upper_len + upper_previous];
                    next_v += 2ULL * u[2][upper_previous];
                }
                if (boundary_index >= 0) next_v += boundary[boundary_index];
                v[1][current] = next_v % MOD;
                continue;
            }

            auto& un = u[n];
            auto& vn = v[n];
            const auto& up = u[n + 1];
            const auto& vp = v[n + 1];
            const auto& down_u = u[n - 1];
            const auto& down_v = v[n - 1];

            const uint32_t first_u =
                previous >= 0 ? un[previous] : 0;
            const uint32_t first_v =
                previous >= 0 ? vn[previous] : 0;
            const uint32_t upper_first_u =
                upper_previous >= 0 && upper_len > 0
                    ? up[upper_previous]
                    : 0;
            const uint32_t upper_first_v =
                upper_previous >= 0 && upper_len > 0
                    ? vp[upper_previous]
                    : 0;

            size_t row = 0;
            size_t next_row = len;
            size_t upper_row = upper_len;
            size_t lower_row = 0;

            if (previous < 0) {
                // Before this boundary length can recurse into itself, only
                // the state with one shorter boundary contributes.
                for (int k = 1; k < n; ++k) {
                    un[row + current] =
                        down_u[lower_row + lower_current];
                    vn[row + current] =
                        down_v[lower_row + lower_current];
                    row = next_row;
                    next_row += len;
                    lower_row += lower_len;
                }
                const size_t final_row = (size_t)(n - 1) * len;
                const size_t lower_final = (size_t)(n - 2) * lower_len;
                un[final_row + current] =
                    down_u[lower_final + lower_current];
                vn[final_row + current] =
                    down_v[lower_final + lower_current];
                continue;
            }

            if (upper_previous >= 0 && upper_len > 0) {
                for (int k = 1; k < n; ++k) {
                    uint64_t next_u =
                        (uint64_t)un[row + previous] + upper_first_v +
                        up[upper_row + upper_previous] +
                        down_u[lower_row + lower_current] + first_v +
                        un[next_row + previous];
                    uint64_t next_v =
                        (uint64_t)vn[row + previous] +
                        vp[upper_row + upper_previous] + upper_first_u +
                        down_v[lower_row + lower_current] +
                        vn[next_row + previous] + first_u;
                    un[row + current] = next_u % MOD;
                    vn[row + current] = next_v % MOD;
                    row = next_row;
                    next_row += len;
                    upper_row += upper_len;
                    lower_row += lower_len;
                }

                const size_t final_row = (size_t)(n - 1) * len;
                const size_t lower_final = (size_t)(n - 2) * lower_len;
                uint64_t next_u =
                    2ULL * un[final_row + previous] + first_v +
                    upper_first_v + up[upper_row + upper_previous] +
                    down_u[lower_final + lower_current];
                uint64_t next_v =
                    2ULL * vn[final_row + previous] + 2ULL * first_u +
                    vp[upper_row + upper_previous] +
                    2ULL * upper_first_u +
                    down_v[lower_final + lower_current];
                un[final_row + current] = next_u % MOD;
                vn[final_row + current] = next_v % MOD;
            } else {
                for (int k = 1; k < n; ++k) {
                    uint64_t next_u =
                        (uint64_t)un[row + previous] +
                        down_u[lower_row + lower_current] + first_v +
                        un[next_row + previous];
                    uint64_t next_v =
                        (uint64_t)vn[row + previous] +
                        down_v[lower_row + lower_current] +
                        vn[next_row + previous] + first_u;
                    un[row + current] = next_u % MOD;
                    vn[row + current] = next_v % MOD;
                    row = next_row;
                    next_row += len;
                    lower_row += lower_len;
                }

                const size_t final_row = (size_t)(n - 1) * len;
                const size_t lower_final = (size_t)(n - 2) * lower_len;
                uint64_t next_u =
                    2ULL * un[final_row + previous] + first_v +
                    down_u[lower_final + lower_current];
                uint64_t next_v =
                    2ULL * vn[final_row + previous] + 2ULL * first_u +
                    down_v[lower_final + lower_current];
                un[final_row + current] = next_u % MOD;
                vn[final_row + current] = next_v % MOD;
            }
        }

        uint64_t next_boundary = 0;
        if (m >= 1) next_boundary += a[m - 1];
        if (m >= 2) next_boundary += 4ULL * boundary[m - 2];
        const int one_boundary_index = m - 3 - offset[1];
        if (one_boundary_index >= 0 && length[1] > 0) {
            next_boundary += 2ULL * u[1][one_boundary_index];
            next_boundary += v[1][one_boundary_index];
        }
        boundary[m] = next_boundary % MOD;

        if (m >= 1) {
            uint64_t next_a = 3ULL * a[m - 1];
            if (m >= 2) next_a += 3ULL * boundary[m - 2];
            a[m] = next_a % MOD;
        }
    }

    if (divisions >= 2) assert(a[1] == 3);
    if (divisions >= 10) assert(a[9] == 44'499);
    if (divisions >= 20) assert(a[19] == 204'559'704);
    if (divisions >= 100) assert(a[99] == 780'166'455);
    return a[last];
}

int main(int argc, char** argv) {
    const int divisions = argc > 1 ? atoi(argv[1]) : 10'000;
    cout << arrangements(divisions) << '\n';
    return 0;
}
