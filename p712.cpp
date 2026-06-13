#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

using i64 = long long;
using u64 = unsigned long long;

constexpr i64 MOD = 1'000'000'007LL;
constexpr u64 DEFAULT_N = 1'000'000'000'000ULL;

u64 isqrt_u64(u64 n) {
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

std::vector<int> primes_up_to(int limit, std::vector<int>& prime_pi) {
    std::vector<bool> composite(limit + 1);
    std::vector<int> primes;
    prime_pi.assign(limit + 1, 0);

    for (int i = 2; i <= limit; ++i) {
        if (!composite[i]) {
            primes.push_back(i);
            if (static_cast<i64>(i) * i <= limit) {
                for (i64 j = static_cast<i64>(i) * i; j <= limit; j += i) {
                    composite[static_cast<std::size_t>(j)] = true;
                }
            }
        }
        prime_pi[i] = static_cast<int>(primes.size());
    }
    return primes;
}

class PrimeCounter {
public:
    explicit PrimeCounter(u64 n) : n_(n), root_(isqrt_u64(n)) {
        if (root_ > static_cast<u64>(std::numeric_limits<int>::max())) {
            throw std::runtime_error("sieve root is too large");
        }
        primes_ = primes_up_to(static_cast<int>(root_), small_pi_);
        build_floor_values();
        run_lucy_sieve();
    }

    u64 pi(u64 x) const {
        if (x <= root_) {
            return static_cast<u64>(small_pi_[static_cast<std::size_t>(x)]);
        }
        return prime_pi_values_[large_id_[static_cast<std::size_t>(n_ / x)]];
    }

    const std::vector<int>& small_primes() const {
        return primes_;
    }

private:
    void build_floor_values() {
        for (u64 l = 1, r; l <= n_; l = r + 1) {
            const u64 v = n_ / l;
            r = n_ / v;

            const int id = static_cast<int>(values_.size());
            values_.push_back(v);
            prime_pi_values_.push_back(v - 1);

            if (v <= root_) {
                small_id_.resize(std::max<std::size_t>(small_id_.size(), v + 1), -1);
                small_id_[static_cast<std::size_t>(v)] = id;
            } else {
                const u64 key = n_ / v;
                large_id_.resize(std::max<std::size_t>(large_id_.size(), key + 1), -1);
                large_id_[static_cast<std::size_t>(key)] = id;
            }
        }
    }

    u64 current_pi(u64 x) const {
        if (x <= root_) {
            return prime_pi_values_[small_id_[static_cast<std::size_t>(x)]];
        }
        return prime_pi_values_[large_id_[static_cast<std::size_t>(n_ / x)]];
    }

    void run_lucy_sieve() {
        for (const int p_int : primes_) {
            const u64 p = static_cast<u64>(p_int);
            const u64 p2 = p * p;
            const u64 before_p = static_cast<u64>(small_pi_[static_cast<std::size_t>(p - 1)]);

            for (std::size_t i = 0; i < values_.size() && values_[i] >= p2; ++i) {
                prime_pi_values_[i] -= current_pi(values_[i] / p) - before_p;
            }
        }
    }

    u64 n_;
    u64 root_;
    std::vector<int> primes_;
    std::vector<int> small_pi_;
    std::vector<int> small_id_;
    std::vector<int> large_id_;
    std::vector<u64> values_;
    std::vector<u64> prime_pi_values_;
};

i64 contribution(u64 n, u64 quotient) {
    const i64 q = static_cast<i64>(quotient % MOD);
    const i64 rest = static_cast<i64>((n - quotient) % MOD);
    return (2LL * q % MOD) * rest % MOD;
}

u64 parse_n(int argc, char** argv) {
    if (argc == 1) {
        return DEFAULT_N;
    }
    if (argc == 3 && std::string(argv[1]) == "--n") {
        return std::stoull(argv[2]);
    }
    throw std::runtime_error("usage: p712 [--n N]");
}

}  // namespace

int main(int argc, char** argv) {
    const u64 n = parse_n(argc, argv);
    const u64 root = isqrt_u64(n);

    PrimeCounter counter(n);
    i64 answer = 0;

    for (u64 l = 2, r; l <= n; l = r + 1) {
        const u64 q = n / l;
        r = n / q;
        const u64 count = counter.pi(r) - counter.pi(l - 1);
        answer = (answer + static_cast<i64>(count % MOD) * contribution(n, q)) % MOD;
    }

    for (const int p_int : counter.small_primes()) {
        const u64 p = static_cast<u64>(p_int);
        if (p > root) {
            break;
        }
        u64 power = p * p;
        while (power <= n) {
            answer += contribution(n, n / power);
            answer %= MOD;
            if (power > n / p) {
                break;
            }
            power *= p;
        }
    }

    std::cout << answer % MOD << '\n';
    return 0;
}
