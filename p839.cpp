// Project Euler 839: moving one bean right increases the index-weighted sum by
// one.  The stable state is the integer-slope greatest convex minorant of the
// prefix sums, computed by pool-adjacent-violators.
#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

struct Block {
    uint32_t len;
    uint64_t sum;
};

static uint64_t index_sum(uint64_t start, uint64_t len) {
    return (start + start + len - 1) * len / 2;
}

static string to_string_u128(unsigned __int128 value) {
    if (value == 0) return "0";
    string out;
    while (value) {
        out.push_back(char('0' + value % 10));
        value /= 10;
    }
    reverse(out.begin(), out.end());
    return out;
}

static unsigned __int128 b_value(int n) {
    vector<Block> blocks;
    blocks.reserve(n);

    uint64_t s = 290797;
    unsigned __int128 initial_moment = 0;
    for (int i = 0; i < n; ++i) {
        initial_moment += (unsigned __int128)i * s;
        blocks.push_back({1, s});
        while (blocks.size() >= 2) {
            const Block& a = blocks[blocks.size() - 2];
            const Block& b = blocks[blocks.size() - 1];
            if ((unsigned __int128)a.sum * b.len <=
                (unsigned __int128)b.sum * a.len)
                break;
            Block merged{a.len + b.len, a.sum + b.sum};
            blocks.pop_back();
            blocks.back() = merged;
        }
        s = s * s % 50515093ULL;
    }

    unsigned __int128 final_moment = 0;
    uint64_t pos = 0;
    for (const Block& block : blocks) {
        uint64_t q = block.sum / block.len;
        uint64_t r = block.sum % block.len;
        uint64_t low_len = block.len - r;
        final_moment += (unsigned __int128)q * index_sum(pos, low_len);
        final_moment += (unsigned __int128)(q + 1) * index_sum(pos + low_len, r);
        pos += block.len;
    }
    return final_moment - initial_moment;
}

int main() {
    if (b_value(5) != 0 || b_value(6) != 14263289ULL ||
        b_value(100) != 3284417556ULL) {
        fprintf(stderr, "self-test failed\n");
        return 1;
    }
    cout << to_string_u128(b_value(10000000)) << "\n";
    return 0;
}
