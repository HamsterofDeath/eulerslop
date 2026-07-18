#include <array>
#include <cstdint>
#include <iostream>
#include <unordered_map>
#include <unordered_set>
#include <vector>

using u64 = std::uint64_t;
using i64 = std::int64_t;

constexpr std::array<int, 5> SUIT_CHOICES{1, 4, 6, 4, 1};

struct GroupKey {
  int five_count;
  int suffix_length;
  int suffix_product;

  bool operator==(const GroupKey& other) const {
    return five_count == other.five_count
        && suffix_length == other.suffix_length
        && suffix_product == other.suffix_product;
  }
};

struct LowKey {
  GroupKey group;
  i64 balance;

  bool operator==(const LowKey& other) const {
    return group == other.group && balance == other.balance;
  }
};

std::size_t mix_hash(std::size_t seed, std::size_t value) {
  seed ^= value + 0x9e3779b97f4a7c15ULL
      + (seed << 6) + (seed >> 2);
  return seed;
}

struct GroupHash {
  std::size_t operator()(const GroupKey& key) const {
    std::size_t result = key.five_count;
    result = mix_hash(result, key.suffix_length);
    return mix_hash(result, key.suffix_product);
  }
};

struct LowHash {
  std::size_t operator()(const LowKey& key) const {
    std::size_t result = GroupHash{}(key.group);
    return mix_hash(
        result,
        std::hash<i64>{}(key.balance)
    );
  }
};

using LowCounts =
    std::unordered_map<LowKey, u64, LowHash>;

void enumerate_low_ranks(
    int rank,
    i64 hand_score,
    i64 pair_score,
    i64 closed_run_score,
    int suffix_length,
    int suffix_product,
    u64 suit_weight,
    const std::array<u64, 16>& subset_counts,
    LowCounts& counts
) {
  if (rank == 10) {
    const i64 balance =
        hand_score
        - pair_score
        - 2 * static_cast<i64>(subset_counts[15])
        - closed_run_score;
    const LowKey key{
        {
            static_cast<int>(subset_counts[5]),
            suffix_length,
            suffix_product,
        },
        balance,
    };
    counts[key] += suit_weight;
    return;
  }

  for (int multiplicity = 0; multiplicity <= 4; ++multiplicity) {
    std::array<u64, 16> next_subsets{};
    for (int sum = 0; sum <= 15; ++sum) {
      if (subset_counts[sum] == 0) {
        continue;
      }
      int binomial = 1;
      for (
          int chosen = 0;
          chosen <= multiplicity
              && sum + chosen * rank <= 15;
          ++chosen
      ) {
        if (chosen > 0) {
          binomial =
              binomial * (multiplicity - chosen + 1)
              / chosen;
        }
        next_subsets[sum + chosen * rank] +=
            subset_counts[sum] * binomial;
      }
    }

    i64 next_closed_run_score = closed_run_score;
    int next_suffix_length;
    int next_suffix_product;
    if (multiplicity == 0) {
      if (suffix_length >= 3) {
        next_closed_run_score +=
            static_cast<i64>(suffix_length)
            * suffix_product;
      }
      next_suffix_length = 0;
      next_suffix_product = 1;
    } else {
      next_suffix_length = suffix_length + 1;
      next_suffix_product =
          suffix_product * multiplicity;
    }

    enumerate_low_ranks(
        rank + 1,
        hand_score + rank * multiplicity,
        pair_score + multiplicity * (multiplicity - 1),
        next_closed_run_score,
        next_suffix_length,
        next_suffix_product,
        suit_weight * SUIT_CHOICES[multiplicity],
        next_subsets,
        counts
    );
  }
}

struct HighHand {
  std::array<int, 4> multiplicities;
  int card_count;
  int pair_score;
  int suit_weight;
};

std::vector<HighHand> enumerate_high_ranks() {
  std::vector<HighHand> hands;
  hands.reserve(625);
  for (int encoded = 0; encoded < 625; ++encoded) {
    int remaining = encoded;
    HighHand hand{{}, 0, 0, 1};
    for (int rank = 0; rank < 4; ++rank) {
      const int multiplicity = remaining % 5;
      remaining /= 5;
      hand.multiplicities[rank] = multiplicity;
      hand.card_count += multiplicity;
      hand.pair_score +=
          multiplicity * (multiplicity - 1);
      hand.suit_weight *= SUIT_CHOICES[multiplicity];
    }
    hands.push_back(hand);
  }
  return hands;
}

i64 boundary_run_score(
    const GroupKey& low,
    const std::array<int, 4>& high
) {
  if (high[0] == 0) {
    i64 result =
        low.suffix_length >= 3
            ? static_cast<i64>(low.suffix_length)
                * low.suffix_product
            : 0;
    if (high[1] != 0 && high[2] != 0 && high[3] != 0) {
      result += 3LL * high[1] * high[2] * high[3];
    }
    return result;
  }

  int prefix_length = 0;
  int prefix_product = 1;
  while (
      prefix_length < 4
      && high[prefix_length] != 0
  ) {
    prefix_product *= high[prefix_length];
    ++prefix_length;
  }

  const int combined_length =
      low.suffix_length + prefix_length;
  if (combined_length < 3) {
    return 0;
  }
  return static_cast<i64>(combined_length)
      * low.suffix_product
      * prefix_product;
}

u64 matching_hand_count() {
  LowCounts low_counts;
  low_counts.reserve(2'000'000);
  std::array<u64, 16> initial_subsets{};
  initial_subsets[0] = 1;
  enumerate_low_ranks(
      1, 0, 0, 0, 0, 1, 1,
      initial_subsets, low_counts
  );

  std::unordered_set<GroupKey, GroupHash> group_set;
  group_set.reserve(low_counts.size());
  for (const auto& [key, count] : low_counts) {
    group_set.insert(key.group);
  }
  const std::vector<GroupKey> groups(
      group_set.begin(),
      group_set.end()
  );

  u64 result = 0;
  for (const HighHand& high : enumerate_high_ranks()) {
    for (const GroupKey& group : groups) {
      const i64 run_score =
          boundary_run_score(
              group,
              high.multiplicities
          );
      const i64 required_low_balance =
          high.pair_score
          + 2LL * high.card_count * group.five_count
          + run_score
          - 10LL * high.card_count;
      const auto found = low_counts.find(
          LowKey{group, required_low_balance}
      );
      if (found != low_counts.end()) {
        result += found->second * high.suit_weight;
      }
    }
  }

  // The empty selection satisfies score equality but is not a Hand.
  return result - 1;
}

int main() {
  std::cout << matching_hand_count() << '\n';
}
