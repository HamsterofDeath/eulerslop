#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <unordered_map>
#include <utility>
#include <vector>

using Piles = std::vector<std::vector<int>>;
using ThresholdState = std::vector<std::pair<int, int>>;

constexpr long long MOD = 1'234'567'891LL;
constexpr int TARGET_N = 10'000;
constexpr long long TARGET_ROUNDS = 10'000'000'000'000'000LL;

std::vector<int> smallest_prime_factors(int limit) {
    std::vector<int> spf(limit + 1);
    std::iota(spf.begin(), spf.end(), 0);
    for (int i = 2; i * i <= limit; ++i) {
        if (spf[i] == i) {
            for (long long j = 1LL * i * i; j <= limit; j += i) {
                if (spf[j] == j) spf[j] = i;
            }
        }
    }
    return spf;
}

std::vector<int> primes_up_to(int limit) {
    std::vector<int> spf = smallest_prime_factors(limit);
    std::vector<int> primes;
    for (int i = 2; i <= limit; ++i) {
        if (spf[i] == i) primes.push_back(i);
    }
    return primes;
}

Piles initial_state(int n) {
    std::vector<int> spf = smallest_prime_factors(n);
    Piles piles;
    for (int k = 2; k <= n; ++k) {
        int x = k;
        std::vector<int> factors;
        while (x > 1) {
            int p = spf[x];
            factors.push_back(p);
            x /= p;
        }
        piles.push_back(std::move(factors));
    }
    return piles;
}

void step_values(Piles& piles) {
    std::vector<int> heads;
    heads.reserve(piles.size());
    Piles next;
    next.reserve(piles.size() + 1);
    for (auto& pile : piles) {
        heads.push_back(pile.front());
        if (pile.size() > 1) next.emplace_back(pile.begin() + 1, pile.end());
    }
    std::sort(heads.begin(), heads.end());
    next.push_back(std::move(heads));
    piles.swap(next);
}

long long sum_state(const Piles& piles) {
    long long total = 0;
    for (const auto& pile : piles) {
        long long product = 1;
        for (int p : pile) product = product * p % MOD;
        total = (total + product) % MOD;
    }
    return total;
}

long long direct_sum(int n, int rounds) {
    Piles piles = initial_state(n);
    for (int i = 0; i < rounds; ++i) step_values(piles);
    return sum_state(piles);
}

std::pair<int, int> length_cycle(int n) {
    std::vector<int> spf = smallest_prime_factors(n);
    std::vector<int> lengths;
    for (int k = 2; k <= n; ++k) {
        int x = k;
        int count = 0;
        while (x > 1) {
            x /= spf[x];
            ++count;
        }
        lengths.push_back(count);
    }

    std::unordered_map<std::string, int> seen;
    auto key_of = [](const std::vector<int>& values) {
        std::string key;
        key.reserve(values.size() * 2);
        for (int value : values) {
            key.append(reinterpret_cast<const char*>(&value), sizeof(value));
        }
        return key;
    };

    seen[key_of(lengths)] = 0;
    for (int t = 1;; ++t) {
        int pile_count = static_cast<int>(lengths.size());
        std::vector<int> next;
        next.reserve(lengths.size() + 1);
        for (int length : lengths) {
            if (length > 1) next.push_back(length - 1);
        }
        next.push_back(pile_count);
        lengths.swap(next);

        std::string key = key_of(lengths);
        auto it = seen.find(key);
        if (it != seen.end()) return {it->second, t - it->second};
        seen.emplace(std::move(key), t);
    }
}

void step_threshold(ThresholdState& state) {
    ThresholdState next;
    next.reserve(state.size() + 1);
    int head_ones = 0;
    int pile_count = static_cast<int>(state.size());
    for (auto [length, ones] : state) {
        if (ones > 0) ++head_ones;
        if (length > 1) next.push_back({length - 1, ones > 0 ? ones - 1 : 0});
    }
    next.push_back({pile_count, head_ones});
    state.swap(next);
}

uint64_t threshold_hash(const ThresholdState& state) {
    uint64_t hash = 1469598103934665603ULL;
    for (auto [length, ones] : state) {
        uint64_t packed = (static_cast<uint64_t>(length) << 32) ^ static_cast<uint32_t>(ones);
        hash ^= packed;
        hash *= 1099511628211ULL;
    }
    return hash;
}

ThresholdState advance_periods(ThresholdState state, long long cycles, int period_rounds) {
    if (cycles == 0) return state;

    std::unordered_map<uint64_t, std::vector<int>> seen;
    std::vector<ThresholdState> history;
    for (long long cycle = 0;; ++cycle) {
        if (cycle == cycles) return state;

        uint64_t hash = threshold_hash(state);
        auto it = seen.find(hash);
        if (it != seen.end()) {
            for (int index : it->second) {
                if (history[index] == state) {
                    long long preperiod = index;
                    long long cycle_length = cycle - index;
                    long long wanted = preperiod + (cycles - preperiod) % cycle_length;
                    return history[static_cast<int>(wanted)];
                }
            }
        }
        seen[hash].push_back(static_cast<int>(history.size()));
        history.push_back(state);

        for (int i = 0; i < period_rounds; ++i) step_threshold(state);
    }
}

long long reconstruct_from_thresholds(
    const Piles& base,
    const std::vector<int>& primes,
    long long cycles,
    int period_rounds
) {
    int pile_count = static_cast<int>(base.size());
    std::vector<long long> products(pile_count, 1);
    std::vector<int> previous_leq(pile_count, 0);

    for (int prime : primes) {
        ThresholdState state;
        state.reserve(pile_count);
        for (const auto& pile : base) {
            int ones = static_cast<int>(std::upper_bound(pile.begin(), pile.end(), prime) - pile.begin());
            state.push_back({static_cast<int>(pile.size()), ones});
        }

        ThresholdState final_state = advance_periods(std::move(state), cycles, period_rounds);
        for (int i = 0; i < pile_count; ++i) {
            int exact_count = final_state[i].second - previous_leq[i];
            for (int j = 0; j < exact_count; ++j) products[i] = products[i] * prime % MOD;
            previous_leq[i] = final_state[i].second;
        }
    }

    long long total = 0;
    for (long long product : products) total = (total + product) % MOD;
    return total;
}

long long solve_target() {
    auto [preperiod, period] = length_cycle(TARGET_N);
    assert(preperiod == 24414);
    assert(period == 253);

    int phase = static_cast<int>((TARGET_ROUNDS - preperiod) % period);
    if (phase < 0) phase += period;

    Piles base = initial_state(TARGET_N);
    for (int i = 0; i < preperiod + phase; ++i) step_values(base);

    std::vector<int> primes = primes_up_to(TARGET_N);
    assert(reconstruct_from_thresholds(base, primes, 0, period) == sum_state(base));

    long long cycles = (TARGET_ROUNDS - (preperiod + phase)) / period;
    return reconstruct_from_thresholds(base, primes, cycles, period);
}

int main() {
    assert(direct_sum(5, 3) == 21);
    assert(direct_sum(10, 100) == 257);
    std::cout << solve_target() << '\n';
}
