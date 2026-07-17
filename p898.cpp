#include <algorithm>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <utility>
#include <vector>

namespace {

struct PairDistribution {
    long double weight;
    long double negative_probability;
    long double zero_probability;
    long double positive_probability;
};

void generate_half(
    const std::vector<PairDistribution>& pairs,
    int index,
    int end,
    long double sum,
    long double probability,
    std::vector<std::pair<long double, long double>>& output
) {
    if (index == end) {
        output.push_back({sum, probability});
        return;
    }
    const auto& item = pairs[index];
    generate_half(
        pairs, index + 1, end,
        sum - item.weight,
        probability * item.negative_probability,
        output
    );
    generate_half(
        pairs, index + 1, end,
        sum,
        probability * item.zero_probability,
        output
    );
    generate_half(
        pairs, index + 1, end,
        sum + item.weight,
        probability * item.positive_probability,
        output
    );
}

long double optimal_probability(
    const std::vector<long double>& lying_probabilities
) {
    std::vector<PairDistribution> pairs;
    for (long double probability : lying_probabilities) {
        if (probability >= 0.5L) {
            continue;
        }
        const long double complement = 1 - probability;
        pairs.push_back({
            2 * std::log(complement / probability),
            probability * probability,
            2 * probability * complement,
            complement * complement,
        });
    }

    const int middle = static_cast<int>(pairs.size()) / 2;
    std::vector<std::pair<long double, long double>> left;
    std::vector<std::pair<long double, long double>> right;
    generate_half(pairs, 0, middle, 0, 1, left);
    generate_half(
        pairs,
        middle,
        static_cast<int>(pairs.size()),
        0,
        1,
        right
    );
    std::sort(right.begin(), right.end());

    std::vector<long double> prefix(right.size() + 1);
    for (std::size_t index = 0; index < right.size(); ++index) {
        prefix[index + 1] = prefix[index] + right[index].second;
    }

    constexpr long double EPSILON = 1e-15L;
    long double result = 0;
    for (const auto& [left_sum, left_probability] : left) {
        const long double boundary = -left_sum;
        const auto first_tie = std::lower_bound(
            right.begin(),
            right.end(),
            std::pair<long double, long double>{
                boundary - EPSILON, -1
            }
        );
        const auto after_tie = std::upper_bound(
            right.begin(),
            right.end(),
            std::pair<long double, long double>{
                boundary + EPSILON, 2
            }
        );
        const std::size_t first_index = first_tie - right.begin();
        const std::size_t after_index = after_tie - right.begin();
        const long double tie_probability = (
            prefix[after_index] - prefix[first_index]
        );
        const long double greater_probability = (
            prefix.back() - prefix[after_index]
        );
        result += left_probability * (
            greater_probability + tie_probability / 2
        );
    }
    return result;
}

}  // namespace

int main(int argc, char** argv) {
    std::vector<long double> probabilities;
    if (argc > 1 && std::string(argv[1]) == "example") {
        probabilities = {0.2L, 0.4L, 0.6L, 0.8L};
    } else {
        for (int percent = 25; percent <= 75; ++percent) {
            probabilities.push_back(percent / 100.0L);
        }
    }
    std::cout << std::fixed << std::setprecision(10)
              << optimal_probability(probabilities) << '\n';
}
