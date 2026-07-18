#include <cstdint>
#include <iostream>
#include <vector>

using i64 = std::int64_t;

constexpr int MODULUS = 1'234'567'891;

class PartitionTable {
 public:
  explicit PartitionTable(int limit)
      : limit_(limit),
        stride_(limit + 1),
        even_((limit + 1LL) * (limit + 1)),
        odd_((limit + 1LL) * (limit + 1)),
        partition_count_(limit + 1) {
    even_[index(0, 0)] = 1;
    partition_count_[0] = 1;
    build();
  }

  int count(int stones, int excess, int parity) const {
    if (stones == 0) {
      return excess == 0 && parity == 0 ? 1 : 0;
    }
    const int parts = stones - excess;
    if (parts < 1 || parts > stones) {
      return 0;
    }
    return parity == 0
        ? even_[index(stones, parts)]
        : odd_[index(stones, parts)];
  }

  const std::vector<int>& partition_counts() const {
    return partition_count_;
  }

 private:
  int limit_;
  int stride_;
  std::vector<int> even_;
  std::vector<int> odd_;
  std::vector<int> partition_count_;

  std::size_t index(int stones, int parts) const {
    return static_cast<std::size_t>(stones) * stride_
        + parts;
  }

  static int add_mod(int left, int right) {
    return static_cast<int>(
        (static_cast<i64>(left) + right) % MODULUS
    );
  }

  void build() {
    for (int stones = 1; stones <= limit_; ++stones) {
      i64 total = 0;
      for (int parts = 1; parts <= stones; ++parts) {
        const std::size_t current = index(stones, parts);
        const std::size_t with_one =
            index(stones - 1, parts - 1);

        // Removing one part of size 1 toggles odd-part parity.
        even_[current] = odd_[with_one];
        odd_[current] = even_[with_one];

        // If every part is at least 2, subtract 1 from all
        // parts. Odd-part parity then toggles iff parts is odd.
        if (stones >= 2 * parts) {
          const std::size_t shifted =
              index(stones - parts, parts);
          if (parts & 1) {
            even_[current] = add_mod(
                even_[current], odd_[shifted]
            );
            odd_[current] = add_mod(
                odd_[current], even_[shifted]
            );
          } else {
            even_[current] = add_mod(
                even_[current], even_[shifted]
            );
            odd_[current] = add_mod(
                odd_[current], odd_[shifted]
            );
          }
        }

        total += even_[current];
        total += odd_[current];
        total %= MODULUS;
      }
      partition_count_[stones] = static_cast<int>(total);
    }
  }
};

int always_a_wins_count(int limit) {
  const PartitionTable partitions(limit);
  const std::vector<int>& counts =
      partitions.partition_counts();

  std::vector<int> count_prefix(limit + 1);
  for (int stones = 0; stones <= limit; ++stones) {
    count_prefix[stones] = counts[stones];
    if (stones > 0) {
      count_prefix[stones] = static_cast<int>(
          (
              static_cast<i64>(count_prefix[stones])
              + count_prefix[stones - 1]
          ) % MODULUS
      );
    }
  }

  i64 all_settings = 0;
  for (int a_stones = 0; a_stones <= limit; ++a_stones) {
    all_settings +=
        static_cast<i64>(counts[a_stones])
        * count_prefix[limit - a_stones]
        % MODULUS;
    all_settings %= MODULUS;
  }

  i64 zero_excess = 0;
  i64 unit_excess_odd = 0;
  std::vector<int> prefix_even(limit + 1);
  std::vector<int> prefix_odd(limit + 1);

  for (int excess = 0; excess < limit; ++excess) {
    int running_even = 0;
    int running_odd = 0;
    for (int stones = 0; stones <= limit; ++stones) {
      running_even = static_cast<int>(
          (
              static_cast<i64>(running_even)
              + partitions.count(stones, excess, 0)
          ) % MODULUS
      );
      running_odd = static_cast<int>(
          (
              static_cast<i64>(running_odd)
              + partitions.count(stones, excess, 1)
          ) % MODULUS
      );
      prefix_even[stones] = running_even;
      prefix_odd[stones] = running_odd;
    }

    for (int a_stones = 0; a_stones <= limit; ++a_stones) {
      const int remaining = limit - a_stones;
      const int a_even = partitions.count(
          a_stones, excess, 0
      );
      const int a_odd = partitions.count(
          a_stones, excess, 1
      );
      const int all_b = static_cast<int>(
          (
              static_cast<i64>(prefix_even[remaining])
              + prefix_odd[remaining]
          ) % MODULUS
      );
      zero_excess +=
          (static_cast<i64>(a_even) + a_odd)
          * all_b % MODULUS;
      zero_excess %= MODULUS;

      if (excess + 1 < limit) {
        const int next_even = partitions.count(
            a_stones, excess + 1, 0
        );
        const int next_odd = partitions.count(
            a_stones, excess + 1, 1
        );
        unit_excess_odd +=
            (
                static_cast<i64>(next_even)
                    * prefix_odd[remaining]
                + static_cast<i64>(next_odd)
                    * prefix_even[remaining]
            ) % MODULUS;
        unit_excess_odd %= MODULUS;
      }
    }
  }

  const i64 inverse_two = (MODULUS + 1LL) / 2;
  i64 result =
      (all_settings - zero_excess + MODULUS)
      % MODULUS * inverse_two % MODULUS;
  result =
      (result - unit_excess_odd + MODULUS) % MODULUS;
  return static_cast<int>(result);
}

int main(int argc, char** argv) {
  const int limit =
      argc > 1 ? std::stoi(argv[1]) : 5000;

  if (always_a_wins_count(4) != 9) {
    std::cerr << "sample self-check failed\n";
    return 1;
  }
  std::cout << always_a_wins_count(limit) << '\n';
}
