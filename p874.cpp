#include <algorithm>
#include <cassert>
#include <cmath>
#include <cstdint>
#include <functional>
#include <iostream>
#include <limits>
#include <queue>
#include <tuple>
#include <vector>

using i64 = std::int64_t;

namespace {

std::vector<int> first_primes(int count) {
    int limit;
    if (count < 6) {
        limit = 20;
    } else {
        const double value = count;
        limit = static_cast<int>(
            value * (std::log(value) + std::log(std::log(value)))
        ) + 20;
    }

    while (true) {
        std::vector<bool> is_prime(limit + 1, true);
        is_prime[0] = false;
        is_prime[1] = false;
        for (int prime = 2; 1LL * prime * prime <= limit; ++prime) {
            if (!is_prime[prime]) {
                continue;
            }
            for (int multiple = prime * prime;
                 multiple <= limit;
                 multiple += prime) {
                is_prime[multiple] = false;
            }
        }

        std::vector<int> primes;
        primes.reserve(count);
        for (int value = 2;
             value <= limit && static_cast<int>(primes.size()) < count;
             ++value) {
            if (is_prime[value]) {
                primes.push_back(value);
            }
        }
        if (static_cast<int>(primes.size()) == count) {
            return primes;
        }
        limit *= 2;
    }
}

i64 maximal_prime_score(int index_limit, int list_length) {
    const auto primes = first_primes(index_limit + 1);
    if (list_length == 0) {
        list_length = primes[index_limit];
    }

    const int largest_prime = primes[index_limit - 1];
    const int target_residue = (
        index_limit - list_length % index_limit
    ) % index_limit;
    const i64 unconstrained = 1LL * list_length * largest_prime;
    if (target_residue == 0) {
        return unconstrained;
    }

    std::vector<int> cost(index_limit);
    for (int decrease = 1; decrease < index_limit; ++decrease) {
        cost[decrease] = (
            largest_prime - primes[index_limit - 1 - decrease]
        );
    }

    constexpr i64 INF = std::numeric_limits<i64>::max() / 4;
    std::vector<i64> distance(index_limit, INF);
    std::vector<int> changes(index_limit, std::numeric_limits<int>::max());
    using State = std::tuple<i64, int, int>;
    std::priority_queue<State, std::vector<State>, std::greater<State>> queue;
    distance[0] = 0;
    changes[0] = 0;
    queue.push({0, 0, 0});

    while (!queue.empty()) {
        const auto [current_cost, current_changes, residue] = queue.top();
        queue.pop();
        if (
            current_cost != distance[residue]
            || current_changes != changes[residue]
        ) {
            continue;
        }
        if (residue == target_residue) {
            assert(current_changes <= list_length);
            return unconstrained - current_cost;
        }

        for (int decrease = 1; decrease < index_limit; ++decrease) {
            int next_residue = residue + decrease;
            if (next_residue >= index_limit) {
                next_residue -= index_limit;
            }
            const i64 next_cost = current_cost + cost[decrease];
            const int next_changes = current_changes + 1;
            if (
                next_cost < distance[next_residue]
                || (
                    next_cost == distance[next_residue]
                    && next_changes < changes[next_residue]
                )
            ) {
                distance[next_residue] = next_cost;
                changes[next_residue] = next_changes;
                queue.push({next_cost, next_changes, next_residue});
            }
        }
    }
    assert(false);
    return -1;
}

}  // namespace

int main(int argc, char** argv) {
    const int index_limit = argc > 1 ? std::stoi(argv[1]) : 7'000;
    const int list_length = argc > 2 ? std::stoi(argv[2]) : 0;
    assert(index_limit >= 2 && list_length >= 0);
    std::cout << maximal_prime_score(index_limit, list_length) << '\n';
}
