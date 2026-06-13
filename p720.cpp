#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>

namespace {

constexpr int DEFAULT_POWER = 25;
constexpr int MOD = 1'000'000'007;

std::vector<int> unpredictable_order(int power) {
    if (power == 1) {
        return {0, 1};
    }
    if (power == 2) {
        return {0, 2, 1, 3};
    }

    std::vector<int> current{0, 2, 1, 3};
    for (int p = 3; p <= power; ++p) {
        const int previous_size = static_cast<int>(current.size());
        std::vector<int> next;
        next.reserve(previous_size * 2);

        for (int i = 0; i + 1 < previous_size; ++i) {
            next.push_back(2 * current[i]);
        }
        next.push_back(1);
        next.push_back(2 * current.back());
        for (int i = 1; i < previous_size; ++i) {
            next.push_back(2 * current[i] + 1);
        }

        current.swap(next);
    }
    return current;
}

class Fenwick {
public:
    explicit Fenwick(int n) : tree_(n + 1, 0) {}

    void add(int index, int delta) {
        for (++index; index < static_cast<int>(tree_.size()); index += index & -index) {
            tree_[index] += delta;
        }
    }

    int sum_prefix(int index) const {
        int total = 0;
        for (++index; index > 0; index -= index & -index) {
            total += tree_[index];
        }
        return total;
    }

private:
    std::vector<int> tree_;
};

int rank_mod(const std::vector<int>& permutation) {
    const int n = static_cast<int>(permutation.size());
    std::vector<int> factorial(n + 1, 1);
    for (int i = 1; i <= n; ++i) {
        factorial[i] = static_cast<int>((1LL * factorial[i - 1] * i) % MOD);
    }

    Fenwick unused(n);
    for (int i = 0; i < n; ++i) {
        unused.add(i, 1);
    }

    int rank = 1;
    for (int position = 0; position < n; ++position) {
        const int value = permutation[position];
        const int smaller_unused = value == 0 ? 0 : unused.sum_prefix(value - 1);
        rank = static_cast<int>((rank + 1LL * smaller_unused * factorial[n - 1 - position]) % MOD);
        unused.add(value, -1);
    }
    return rank;
}

int parse_power(int argc, char** argv) {
    return argc > 1 ? std::atoi(argv[1]) : DEFAULT_POWER;
}

}  // namespace

int main(int argc, char** argv) {
    std::cout << rank_mod(unpredictable_order(parse_power(argc, argv))) << '\n';
    return 0;
}
