#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <unordered_map>
#include <vector>

namespace {

using i64 = long long;
using u64 = unsigned long long;
using i128 = __int128_t;

constexpr u64 kDefaultN = 100'000'000'000'000ULL;
constexpr int kDivisorTableLimit = 10'000'000;

std::vector<int> primes_up_to(int limit) {
    std::vector<bool> composite(limit + 1);
    std::vector<int> primes;
    for (int n = 2; n <= limit; ++n) {
        if (!composite[n]) {
            primes.push_back(n);
            if (static_cast<i64>(n) * n <= limit) {
                for (i64 m = static_cast<i64>(n) * n; m <= limit; m += n) {
                    composite[static_cast<std::size_t>(m)] = true;
                }
            }
        }
    }
    return primes;
}

std::vector<u64> divisor_summatory_table(int limit) {
    std::vector<int> divisor_count(limit + 1);
    for (int d = 1; d <= limit; ++d) {
        for (int m = d; m <= limit; m += d) {
            ++divisor_count[m];
        }
    }

    std::vector<u64> prefix(limit + 1);
    for (int n = 1; n <= limit; ++n) {
        prefix[n] = prefix[n - 1] + static_cast<u64>(divisor_count[n]);
    }
    return prefix;
}

class Solver {
public:
    explicit Solver(u64 n)
        : n_(n),
          primes_(primes_up_to(static_cast<int>(isqrt(n)))),
          divisor_sum_(divisor_summatory_table(kDivisorTableLimit)) {}

    u64 run() {
        visit(0, 1, 1);
        return static_cast<u64>(answer_);
    }

private:
    static u64 isqrt(u64 n) {
        u64 lo = 0;
        u64 hi = 1;
        while (hi <= n / hi) {
            hi <<= 1;
        }
        while (lo + 1 < hi) {
            const u64 mid = lo + (hi - lo) / 2;
            if (mid <= n / mid) {
                lo = mid;
            } else {
                hi = mid;
            }
        }
        return lo;
    }

    u64 divisor_summatory(u64 n) {
        if (n <= kDivisorTableLimit) {
            return divisor_sum_[static_cast<std::size_t>(n)];
        }

        auto found = divisor_cache_.find(n);
        if (found != divisor_cache_.end()) {
            return found->second;
        }

        u64 total = 0;
        for (u64 left = 1, right; left <= n; left = right + 1) {
            const u64 quotient = n / left;
            right = n / quotient;
            total += quotient * (right - left + 1);
        }

        divisor_cache_.emplace(n, total);
        return total;
    }

    void visit(std::size_t prime_index, u64 current, u64 weight) {
        answer_ += static_cast<i128>(weight) * divisor_summatory(n_ / current);

        for (std::size_t i = prime_index; i < primes_.size(); ++i) {
            const u64 p = static_cast<u64>(primes_[i]);
            if (p > n_ / current / p) {
                break;
            }

            u64 next = current * p * p;
            u64 next_weight = weight;
            while (next <= n_) {
                visit(i + 1, next, next_weight);
                if (next > n_ / p) {
                    break;
                }
                next *= p;
                next_weight *= 2;
            }
        }
    }

    u64 n_;
    std::vector<int> primes_;
    std::vector<u64> divisor_sum_;
    std::unordered_map<u64, u64> divisor_cache_;
    i128 answer_ = 0;
};

u64 parse_n(int argc, char** argv) {
    if (argc == 1) {
        return kDefaultN;
    }
    return static_cast<u64>(std::strtoull(argv[1], nullptr, 10));
}

}  // namespace

int main(int argc, char** argv) {
    Solver solver(parse_n(argc, argv));
    std::cout << solver.run() << '\n';
    return 0;
}
