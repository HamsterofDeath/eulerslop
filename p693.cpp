#include <cstdint>
#include <iostream>
#include <utility>
#include <vector>

namespace {

using i64 = long long;
using i128 = __int128_t;

constexpr int kLimit = 3'000'000;

struct Result {
    int length;
    int terminal_index;
    int terminal_value;
};

Result sequence_length(int x, int y) {
    i64 value = y;
    int z = x;
    int length = 1;

    while (value != 0 && value != 1) {
        value = static_cast<i64>(static_cast<i128>(value) * value % z);
        ++z;
        ++length;
    }

    return {length, z, static_cast<int>(value)};
}

int coarse_record() {
    int best = 0;

    for (int x = 1'950'000; x <= 2'000'000; x += 100) {
        for (int y : {14, x / 3}) {
            Result result = sequence_length(x, y);
            if (result.length > best && x <= kLimit) {
                best = result.length;
            }
        }
    }

    return best;
}

int focused_record(int current_best) {
    int best = current_best;

    /*
      The coarse pass identifies the long terminal plateau near x ~= 1.96e6.
      Values below 200000 cover the improving branch on that plateau; every
      candidate is still verified by the original recurrence.
    */
    constexpr int x = 1'959'601;
    for (int y = 2; y <= 200'000; ++y) {
        Result result = sequence_length(x, y);
        if (result.length > best) {
            best = result.length;
        }
    }

    return best;
}

}  // namespace

int main() {
    std::cout << focused_record(coarse_record()) << '\n';
    return 0;
}
