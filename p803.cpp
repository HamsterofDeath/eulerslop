// Project Euler 803: recover Rand48 states from output residues, then use
// baby-step/giant-step on the affine 48-bit LCG cycle.
#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <limits>
#include <string>
#include <utility>
#include <vector>

using namespace std;

static const uint64_t A = 25214903917ULL;
static const uint64_t C = 11ULL;
static const uint64_t MASK = (1ULL << 48) - 1;
static const uint64_t HIGH = 1ULL << 32;

static inline uint64_t step(uint64_t x) {
    return (uint64_t)(((__uint128_t)A * x + C) & MASK);
}

static inline int output(uint64_t x) {
    return (int)((x >> 16) % 52);
}

static int code(char ch) {
    if ('a' <= ch && ch <= 'z') return ch - 'a';
    if ('A' <= ch && ch <= 'Z') return 26 + ch - 'A';
    fprintf(stderr, "bad character: %c\n", ch);
    exit(1);
}

static vector<int> codes(const string& s) {
    vector<int> b;
    for (char ch : s) b.push_back(code(ch));
    return b;
}

static bool has_prefix(uint64_t state, const vector<int>& b) {
    for (int want : b) {
        if (output(state) != want) return false;
        state = step(state);
    }
    return true;
}

static vector<uint64_t> states_for_prefix(const string& s) {
    vector<int> b = codes(s);
    vector<uint16_t> low_candidates;

    for (uint32_t low0 = 0; low0 < (1U << 16); ++low0) {
        uint64_t low = low0;
        int high_mod4 = b[0] & 3;
        bool ok = true;
        for (size_t i = 1; i < b.size(); ++i) {
            uint64_t prod = A * low + C;
            uint64_t carry = prod >> 16;
            low = prod & 0xffffU;
            high_mod4 = (high_mod4 + (int)(carry & 3)) & 3;  // A == 1 mod 4.
            if (high_mod4 != (b[i] & 3)) {
                ok = false;
                break;
            }
        }
        if (ok) low_candidates.push_back((uint16_t)low0);
    }

    vector<uint64_t> result;
    for (uint16_t low0 : low_candidates) {
        for (uint64_t high = (uint64_t)b[0]; high < HIGH; high += 52) {
            uint64_t state = (high << 16) | low0;
            if (has_prefix(state, b)) result.push_back(state);
        }
    }
    sort(result.begin(), result.end());
    result.erase(unique(result.begin(), result.end()), result.end());
    return result;
}

struct Affine {
    uint64_t mul;
    uint64_t add;
};

static inline uint64_t apply_affine(const Affine& f, uint64_t x) {
    return (uint64_t)(((__uint128_t)f.mul * x + f.add) & MASK);
}

static Affine compose(const Affine& f, const Affine& g) {
    return {
        (uint64_t)((__uint128_t)f.mul * g.mul & MASK),
        (uint64_t)(((__uint128_t)f.mul * g.add + f.add) & MASK),
    };
}

static Affine power(Affine base, uint64_t exponent) {
    Affine result{1, 0};
    while (exponent) {
        if (exponent & 1) result = compose(base, result);
        base = compose(base, base);
        exponent >>= 1;
    }
    return result;
}

static uint64_t inverse_odd_mod_2_48(uint64_t x) {
    uint64_t inv = 1;
    for (int i = 0; i < 6; ++i) inv *= 2 - x * inv;
    return inv & MASK;
}

static uint64_t first_hit(uint64_t start, const vector<uint64_t>& targets) {
    const uint32_t m = 1U << 24;
    vector<pair<uint64_t, uint32_t>> baby;
    baby.reserve(m);

    uint64_t state = start;
    for (uint32_t j = 0; j < m; ++j) {
        baby.push_back({state, j});
        state = step(state);
    }
    sort(baby.begin(), baby.end());

    uint64_t inv_a = inverse_odd_mod_2_48(A);
    Affine inverse_step{inv_a, (uint64_t)((-(__int128)inv_a * C) & MASK)};
    Affine back = power(inverse_step, m);

    uint64_t best = numeric_limits<uint64_t>::max();
    for (uint64_t target : targets) {
        uint64_t cur = target;
        for (uint32_t i = 0; i < m; ++i) {
            auto it = lower_bound(
                baby.begin(), baby.end(), make_pair(cur, (uint32_t)0));
            if (it != baby.end() && it->first == cur) {
                uint64_t candidate = (uint64_t)i * m + it->second;
                if (candidate < best) best = candidate;
            }
            cur = apply_affine(back, cur);
        }
    }
    if (best == numeric_limits<uint64_t>::max()) {
        fprintf(stderr, "target prefix is not on the Rand48 cycle\n");
        exit(1);
    }
    return best;
}

static uint64_t nth_state(uint64_t start, uint64_t n) {
    return apply_affine(power({A, C}, n), start);
}

int main() {
    vector<uint64_t> euler = states_for_prefix("EULERcats");
    if (euler.size() != 1 || euler[0] != 78580612777175ULL) {
        fprintf(stderr, "EULERcats self-test failed\n");
        return 1;
    }

    vector<int> rxq = codes("RxqLBfWzv");
    uint64_t example = 123456;
    for (int i = 0; i < 100; ++i) {
        if (has_prefix(example, rxq)) {
            fprintf(stderr, "index-100 self-test found early hit at %d\n", i);
            return 1;
        }
        example = step(example);
    }
    if (!has_prefix(example, rxq)) {
        fprintf(stderr, "index-100 self-test failed\n");
        return 1;
    }

    vector<uint64_t> starts = states_for_prefix("PuzzleOne");
    vector<uint64_t> targets = states_for_prefix("LuckyText");
    if (starts.size() != 1 || targets.empty()) {
        fprintf(stderr, "unexpected prefix state count: %zu %zu\n",
                starts.size(), targets.size());
        return 1;
    }

    uint64_t answer = first_hit(starts[0], targets);
    if (!has_prefix(nth_state(starts[0], answer), codes("LuckyText"))) {
        fprintf(stderr, "answer state self-test failed\n");
        return 1;
    }
    printf("%llu\n", (unsigned long long)answer);
    return 0;
}
