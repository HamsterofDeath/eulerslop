#include <cstdint>
#include <iostream>
#include <numeric>
#include <vector>

using u64 = std::uint64_t;

namespace {

u64 password_count(int rows, int columns) {
    const int spots = rows * columns;
    const int mask_count = 1 << spots;

    // required[from][to] contains every grid spot strictly inside the
    // segment.  A move may be adjacent in the password exactly when all
    // these spots have disappeared already.
    std::vector<std::vector<int>> required(
        spots,
        std::vector<int>(spots, 0)
    );
    for (int from = 0; from < spots; ++from) {
        const int from_row = from / columns;
        const int from_column = from % columns;
        for (int to = 0; to < spots; ++to) {
            const int row_delta = to / columns - from_row;
            const int column_delta = to % columns - from_column;
            const int divisor = std::gcd(
                std::abs(row_delta),
                std::abs(column_delta)
            );
            if (divisor <= 1) {
                continue;
            }
            const int row_step = row_delta / divisor;
            const int column_step = column_delta / divisor;
            for (int step = 1; step < divisor; ++step) {
                const int row = from_row + step * row_step;
                const int column = from_column + step * column_step;
                required[from][to] |= 1 << (row * columns + column);
            }
        }
    }

    std::vector<u64> paths(static_cast<std::size_t>(mask_count) * spots);
    for (int spot = 0; spot < spots; ++spot) {
        paths[(1 << spot) * spots + spot] = 1;
    }

    u64 result = 0;
    for (int mask = 1; mask < mask_count; ++mask) {
        for (int last = 0; last < spots; ++last) {
            const u64 ways = paths[mask * spots + last];
            if (ways == 0) {
                continue;
            }
            if ((mask & (mask - 1)) != 0) {
                result += ways;
            }

            for (int next = 0; next < spots; ++next) {
                const int next_bit = 1 << next;
                if (
                    (mask & next_bit) == 0
                    && (required[last][next] & ~mask) == 0
                ) {
                    paths[(mask | next_bit) * spots + next] += ways;
                }
            }
        }
    }
    return result;
}

}  // namespace

int main(int argc, char** argv) {
    const int rows = argc > 1 ? std::stoi(argv[1]) : 4;
    const int columns = argc > 2 ? std::stoi(argv[2]) : rows;
    std::cout << password_count(rows, columns) << '\n';
}
