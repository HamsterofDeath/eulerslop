#include <algorithm>
#include <atomic>
#include <cstdint>
#include <iostream>
#include <thread>
#include <vector>

using i64 = std::int64_t;

struct PairSequence {
  int multiplicity;
  int stable_start;
  int stable_value;
  std::vector<int> values;
};

i64 paper_cut_sum(int maximum_width, int maximum_height) {
  std::vector<std::vector<int>> grundy_rows(
      maximum_width + 1
  );
  std::vector<int> stable_value(maximum_width + 1);
  std::vector<int> stable_start(maximum_width + 1);

  // A strip of width 1 can never be cut both ways.
  grundy_rows[1] = {0, 0};
  stable_value[1] = 0;
  stable_start[1] = 1;

  const auto grundy_at = [&](int width, int height) {
    return height
                < static_cast<int>(grundy_rows[width].size())
        ? grundy_rows[width][height]
        : stable_value[width];
  };

  i64 result = 0;
  for (int width = 2; width <= maximum_width; ++width) {
    int largest_pair_start = 1;
    for (int left = 1; left <= width / 2; ++left) {
      largest_pair_start = std::max(
          largest_pair_start,
          std::max(
              stable_start[left],
              stable_start[width - left]
          )
      );
    }
    const int guaranteed_stable_height =
        2 * largest_pair_start;

    std::vector<PairSequence> pairs;
    pairs.reserve(width / 2);
    for (int left = 1; left <= width / 2; ++left) {
      const int right = width - left;
      PairSequence pair;
      pair.multiplicity = left == right ? 1 : 2;
      pair.stable_start = std::max(
          stable_start[left], stable_start[right]
      );
      pair.stable_value =
          stable_value[left] ^ stable_value[right];
      pair.values.resize(guaranteed_stable_height + 1);
      for (
          int height = 1;
          height <= guaranteed_stable_height;
          ++height
      ) {
        pair.values[height] =
            grundy_at(left, height)
            ^ grundy_at(right, height);
      }
      pairs.push_back(std::move(pair));
    }

    // For a very tall rectangle, a central horizontal cut
    // contributes value L xor L = 0. Boundary cuts contribute
    // A(y) xor L, so the eventual mex is known before computing
    // any values in the current row.
    std::vector<unsigned char> eventual_options(1, 1);
    for (const PairSequence& pair : pairs) {
      for (
          int height = 1;
          height < pair.stable_start;
          ++height
      ) {
        const int option =
            pair.values[height] ^ pair.stable_value;
        if (
            option
            >= static_cast<int>(eventual_options.size())
        ) {
          eventual_options.resize(option + 1);
        }
        eventual_options[option] = 1;
      }
    }
    int eventual_grundy = 0;
    while (
        eventual_grundy
            < static_cast<int>(eventual_options.size())
        && eventual_options[eventual_grundy]
    ) {
      ++eventual_grundy;
    }
    stable_value[width] = eventual_grundy;

    grundy_rows[width].resize(
        guaranteed_stable_height + 1
    );
    std::vector<i64> winning_moves(
        guaranteed_stable_height + 1
    );

    // All heights in this row depend only on smaller widths, so
    // they can be evaluated independently.
    std::atomic<int> next_height{1};
    const unsigned int thread_count = std::max(
        1U,
        std::min(
            {
                32U,
                std::thread::hardware_concurrency(),
                static_cast<unsigned int>(
                    guaranteed_stable_height
                ),
            }
        )
    );
    std::vector<std::thread> workers;
    workers.reserve(thread_count);
    for (unsigned int worker = 0; worker < thread_count; ++worker) {
      workers.emplace_back([&] {
        std::vector<int> seen(256);
        int stamp = 0;
        while (true) {
          const int height = next_height.fetch_add(1);
          if (height > guaranteed_stable_height) {
            break;
          }
          ++stamp;
          i64 winning = 0;

          for (const PairSequence& pair : pairs) {
            for (int cut = 1; cut <= height / 2; ++cut) {
              const int other = height - cut;
              if (other == 0) {
                continue;
              }
              const int option =
                  pair.values[cut]
                  ^ pair.values[other];
              if (option >= static_cast<int>(seen.size())) {
                seen.resize(option + 1);
              }
              seen[option] = stamp;
              if (option == 0) {
                winning += pair.multiplicity
                    * (cut == other ? 1 : 2);
              }
            }
          }

          int grundy = 0;
          while (
              grundy < static_cast<int>(seen.size())
              && seen[grundy] == stamp
          ) {
            ++grundy;
          }
          grundy_rows[width][height] = grundy;
          winning_moves[height] = winning;
        }
      });
    }
    for (std::thread& worker : workers) {
      worker.join();
    }

    if (
        grundy_rows[width][guaranteed_stable_height]
        != eventual_grundy
    ) {
      std::cerr << "stability bound failed\n";
      return -1;
    }

    int last_exception = 0;
    for (
        int height = 1;
        height <= guaranteed_stable_height;
        ++height
    ) {
      if (
          grundy_rows[width][height]
          != eventual_grundy
      ) {
        last_exception = height;
      }
    }
    stable_start[width] = last_exception + 1;

    // For h >= 2T, each pair sequence contributes a central
    // block of h-2T+1 zero-xors, plus two fixed boundaries.
    i64 affine_intercept = 0;
    for (const PairSequence& pair : pairs) {
      int matching_boundary_values = 0;
      for (
          int height = 1;
          height < pair.stable_start;
          ++height
      ) {
        if (pair.values[height] == pair.stable_value) {
          ++matching_boundary_values;
        }
      }
      affine_intercept += pair.multiplicity
          * (
              -2LL * pair.stable_start
              + 1
              + 2LL * matching_boundary_values
          );
    }
    const i64 affine_slope = width - 1;
    if (
        winning_moves[guaranteed_stable_height]
        != affine_slope * guaranteed_stable_height
            + affine_intercept
    ) {
      std::cerr << "winning-move tail check failed\n";
      return -1;
    }

    for (
        int height = 2;
        height < guaranteed_stable_height
            && height <= maximum_height;
        ++height
    ) {
      result += winning_moves[height];
    }
    if (maximum_height >= guaranteed_stable_height) {
      const i64 count =
          maximum_height - guaranteed_stable_height + 1LL;
      const i64 height_sum =
          (
              guaranteed_stable_height
              + static_cast<i64>(maximum_height)
          ) * count / 2;
      result += affine_slope * height_sum
          + affine_intercept * count;
    }

    // Only exceptional entries need to remain in memory.
    grundy_rows[width].resize(stable_start[width]);
  }
  return result;
}

int main(int argc, char** argv) {
  const int maximum_width =
      argc > 1 ? std::stoi(argv[1]) : 123;
  const int maximum_height =
      argc > 2 ? std::stoi(argv[2]) : 1'234'567;

  if (paper_cut_sum(12, 123) != 327'398) {
    std::cerr << "sample self-check failed\n";
    return 1;
  }
  std::cout
      << paper_cut_sum(maximum_width, maximum_height)
      << '\n';
}
