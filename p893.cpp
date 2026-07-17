#include <algorithm>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>

using i64 = std::int64_t;

namespace {

constexpr int DIGIT_COST[10] = {6, 2, 5, 5, 4, 5, 6, 3, 7, 6};
constexpr int OPERATOR_COST = 2;

int literal_cost(int number) {
    int result = 0;
    do {
        result += DIGIT_COST[number % 10];
        number /= 10;
    } while (number != 0);
    return result;
}

i64 summatory_minimum_cost(int limit) {
    // product_cost[n] is the cheapest product of decimal literals.
    std::vector<int> product_cost(limit + 1);
    for (int number = 1; number <= limit; ++number) {
        product_cost[number] = literal_cost(number);
    }
    for (int factor = 2; factor * factor <= limit; ++factor) {
        for (int product = factor * factor;
             product <= limit;
             product += factor) {
            product_cost[product] = std::min(
                product_cost[product],
                product_cost[factor]
                    + OPERATOR_COST
                    + product_cost[product / factor]
            );
        }
    }

    // Addition partitions an expression into product-only terms.
    // In every unordered split, at least one side has no greater cost
    // than the other.  Iterating only those low-cost classes is exact
    // and prunes almost all numerical candidates.
    std::vector<int> minimum_cost(limit + 1);
    std::vector<std::vector<int>> numbers_by_cost(64);
    i64 result = 0;
    for (int number = 1; number <= limit; ++number) {
        int best = product_cost[number];
        for (int first_cost = 2;
             2 * first_cost + OPERATOR_COST <= best;
             ++first_cost) {
            for (int first : numbers_by_cost[first_cost]) {
                if (first >= number) {
                    break;
                }
                const int second_cost = minimum_cost[number - first];
                if (first_cost <= second_cost) {
                    best = std::min(
                        best,
                        first_cost + OPERATOR_COST + second_cost
                    );
                }
            }
        }
        minimum_cost[number] = best;
        numbers_by_cost[best].push_back(number);
        result += best;
    }
    return result;
}

}  // namespace

int main(int argc, char** argv) {
    const int limit = argc > 1 ? std::stoi(argv[1]) : 1'000'000;
    std::cout << summatory_minimum_cost(limit) << '\n';
}
