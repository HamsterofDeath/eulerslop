#include <cmath>
#include <cstdint>
#include <iostream>
#include <map>

using u64 = std::uint64_t;
using u128 = unsigned __int128;

constexpr u64 TARGET_N = 10'000'000'000'000'000ULL;
constexpr u64 OUTPUT_MODULUS = 1'000'000'000;

u64 integer_square_root(u128 value) {
  u64 root = static_cast<u64>(std::sqrt(static_cast<long double>(value)));
  while (static_cast<u128>(root + 1) * (root + 1) <= value) {
    ++root;
  }
  while (static_cast<u128>(root) * root > value) {
    --root;
  }
  return root;
}

u64 death_premium(u64 deaths, u64 blood_denominator) {
  const u128 quotient =
      static_cast<u128>(deaths) * deaths / blood_denominator;
  return integer_square_root(quotient) + 1;
}

u64 ceil_multiple_sqrt(u64 multiplier, u64 value) {
  if (multiplier == 0) {
    return 0;
  }
  const u128 square =
      static_cast<u128>(multiplier) * multiplier * value;
  const u64 floor = integer_square_root(square);
  return static_cast<u128>(floor) * floor == square
      ? floor : floor + 1;
}

class PirateProcess {
 public:
  PirateProcess(u64 coins, u64 blood_denominator)
      : coins_(coins), blood_denominator_(blood_denominator) {
    allocation_[coins] = 1;
  }

  u64 sum_through(u64 limit, u64 modulus) {
    u64 population = 1;
    u64 senior_coins = coins_;
    u64 answer = coins_ % modulus;

    while (population < limit) {
      const u64 deaths = next_accepted_distance(population);
      if (population + deaths > limit) {
        const u64 count = limit - population;
        add_failed_range(
            answer, count, senior_coins, modulus
        );
        break;
      }

      if (deaths > 1) {
        add_failed_range(
            answer, deaths - 1, senior_coins, modulus
        );
      }
      senior_coins = accept(population, deaths);
      population += deaths;
      answer += senior_coins % modulus;
      answer %= modulus;
    }
    return answer;
  }

 private:
  u64 coins_;
  u64 blood_denominator_;
  std::map<u64, u64> allocation_;

  static u64 required_survivor_votes(
      u64 population, u64 deaths
  ) {
    if (deaths >= population) {
      return 0;
    }
    return (population - deaths + 1) / 2;
  }

  u128 cheapest_sum(u64 wanted) const {
    u128 sum = 0;
    for (const auto& [coins, count] : allocation_) {
      const u64 take = std::min(wanted, count);
      sum += static_cast<u128>(take) * coins;
      wanted -= take;
      if (wanted == 0) {
        break;
      }
    }
    return sum;
  }

  bool feasible(u64 population, u64 deaths) const {
    const u64 votes =
        required_survivor_votes(population, deaths);
    const u64 premium =
        death_premium(deaths, blood_denominator_);
    const u128 cost =
        cheapest_sum(votes)
        + static_cast<u128>(votes) * premium;
    return cost <= coins_;
  }

  u64 next_accepted_distance(u64 population) const {
    if (feasible(population, 1)) {
      return 1;
    }

    const u64 first_interval_end = std::min(
        population,
        ceil_multiple_sqrt(1, blood_denominator_) - 1
    );
    if (feasible(population, first_interval_end)) {
      u64 low = 2;
      u64 high = first_interval_end;
      while (low < high) {
        const u64 middle = (low + high) / 2;
        if (feasible(population, middle)) {
          high = middle;
        } else {
          low = middle + 1;
        }
      }
      return low;
    }

    // In a fixed-premium interval the cost decreases with deaths.
    // Once the one-premium interval fails, interval-end feasibility
    // stays false through the concave rising branch and then becomes
    // true permanently on the descending branch.
    u64 low_level = 2;
    u64 high_level =
        death_premium(population, blood_denominator_) + 1;
    while (low_level < high_level) {
      const u64 middle = (low_level + high_level) / 2;
      const u64 interval_end = std::min(
          population,
          ceil_multiple_sqrt(middle, blood_denominator_) - 1
      );
      if (feasible(population, interval_end)) {
        high_level = middle;
      } else {
        low_level = middle + 1;
      }
    }

    const u64 level = low_level;
    u64 low = ceil_multiple_sqrt(
        level - 1, blood_denominator_
    );
    u64 high = std::min(
        population,
        ceil_multiple_sqrt(level, blood_denominator_) - 1
    );
    while (low < high) {
      const u64 middle = (low + high) / 2;
      if (feasible(population, middle)) {
        high = middle;
      } else {
        low = middle + 1;
      }
    }
    return low;
  }

  u64 accept(u64 population, u64 deaths) {
    const u64 votes =
        required_survivor_votes(population, deaths);
    const u64 premium =
        death_premium(deaths, blood_denominator_);
    u64 remaining = votes;
    u128 bribe_cost = 0;
    std::map<u64, u64> next;

    for (const auto& [coins, count] : allocation_) {
      const u64 take = std::min(remaining, count);
      if (take != 0) {
        next[coins + premium] += take;
        bribe_cost +=
            static_cast<u128>(take) * (coins + premium);
        remaining -= take;
      }
      if (remaining == 0) {
        break;
      }
    }

    const u64 proposer_coins =
        coins_ - static_cast<u64>(bribe_cost);
    ++next[proposer_coins];
    const u64 next_population = population + deaths;
    u64 represented = 0;
    for (const auto& [coins, count] : next) {
      represented += count;
    }
    if (represented < next_population) {
      next[0] += next_population - represented;
    }
    allocation_ = std::move(next);
    return proposer_coins;
  }

  static void add_failed_range(
      u64& answer, u64 count, u64 senior_coins,
      u64 modulus
  ) {
    const u128 contribution =
        static_cast<u128>(count) * senior_coins
        + static_cast<u128>(count) * (count + 1) / 2;
    answer = static_cast<u64>(
        (answer + contribution % modulus) % modulus
    );
  }
};

u64 T(
    u64 limit, u64 coins, u64 blood_denominator,
    u64 modulus
) {
  return PirateProcess(coins, blood_denominator)
      .sum_through(limit, modulus);
}

int main() {
  constexpr u64 SAMPLE_MODULUS =
      1'000'000'000'000'000'003ULL;
  const u64 sample_one = T(30, 3, 3, SAMPLE_MODULUS);
  const u64 sample_two = T(50, 3, 31, SAMPLE_MODULUS);
  const u64 sample_three =
      T(1'000, 101, 101, SAMPLE_MODULUS);
  if (
      sample_one != 190 || sample_two != 385
      || sample_three != 142'427
  ) {
    std::cerr
        << "samples: " << sample_one << ", "
        << sample_two << ", " << sample_three << '\n';
    std::cerr << "sample self-check failed\n";
    return 1;
  }

  u64 answer = 0;
  u64 power_of_ten = 1;
  for (int exponent = 1; exponent <= 6; ++exponent) {
    power_of_ten *= 10;
    const u64 coins = power_of_ten + 1;
    answer += T(TARGET_N, coins, coins, OUTPUT_MODULUS);
    answer %= OUTPUT_MODULUS;
  }
  std::cout << answer << '\n';
}
