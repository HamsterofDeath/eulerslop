#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>

class Fenwick {
 public:
  explicit Fenwick(std::uint32_t n) : tree_(n + 1, 0) {}

  void add(std::uint32_t index) {
    for (++index; index < tree_.size(); index += index & -index) {
      ++tree_[index];
    }
  }

  std::uint64_t sum_less(std::uint32_t index) const {
    std::uint64_t total = 0;
    for (; index > 0; index -= index & -index) {
      total += tree_[index];
    }
    return total;
  }

  std::uint64_t sum_leq(std::uint32_t index) const {
    if (index + 1 >= tree_.size()) return sum_less(tree_.size() - 1);
    return sum_less(index + 1);
  }

 private:
  std::vector<std::uint32_t> tree_;
};

static std::uint64_t total_triangles(std::uint64_t n) {
  return n * (3 * n + 1) / 2;
}

// Count upper-pointing upper-half triangles hit by the dyadic lattice when
// D = 2^k < N.  In this range every reachable lattice point lies in a distinct
// unit triangle, so the problem is a non-carry count modulo D.
static std::uint64_t count_when_grid_is_coarse(std::uint64_t n, std::uint32_t d) {
  const std::uint32_t multiplier = static_cast<std::uint32_t>(n & (d - 1));
  const std::uint64_t base = static_cast<std::uint64_t>(d - 1) * (d - 2) / 2;
  Fenwick seen(d);
  std::uint64_t extra = 0;

  for (std::uint32_t b = d - 1; b >= 1; --b) {
    const std::uint32_t t = d - b - 1;
    if (t >= 1) {
      seen.add(static_cast<std::uint32_t>(
          (static_cast<std::uint64_t>(multiplier) * t) & (d - 1)));
    }
    const std::uint32_t rb = static_cast<std::uint32_t>(
        (static_cast<std::uint64_t>(multiplier) * b) & (d - 1));
    extra += seen.sum_less(d - rb);
    if (b == 1) break;
  }

  return base + extra;
}

// Count the single possible intermediate power with N < D < 2N.  Each
// coordinate interval then contains at most two integer grid lines.  Reducing
// the hit condition gives rem_i + rem_j > N - M, where M = D - N.
static std::uint64_t count_when_grid_is_fine(std::uint64_t n, std::uint64_t d) {
  const std::uint64_t m = d - n;
  Fenwick seen(static_cast<std::uint32_t>(n));
  std::uint64_t total = 0;

  for (std::uint64_t j = n; j-- > 0;) {
    const std::uint64_t prefix_index = n - j - 1;
    const std::uint32_t ri = static_cast<std::uint32_t>((m * prefix_index) % n);
    seen.add(ri);

    const std::uint64_t rj = (m * j) % n;
    const std::int64_t threshold =
        static_cast<std::int64_t>(n - m) - static_cast<std::int64_t>(rj);

    std::uint64_t full_cycle;
    if (threshold < 0) {
      full_cycle = n;
    } else {
      full_cycle = n - 1 - static_cast<std::uint64_t>(threshold);
    }

    const std::uint64_t prefix_size = prefix_index + 1;
    std::uint64_t prefix_count;
    if (threshold < 0) {
      prefix_count = prefix_size;
    } else {
      prefix_count =
          prefix_size - seen.sum_leq(static_cast<std::uint32_t>(threshold));
    }
    total += full_cycle + prefix_count;
  }

  return total;
}

static std::uint64_t hit_count(std::uint64_t n, std::uint64_t d) {
  if (d <= 2) return 0;
  if (d < n) {
    return count_when_grid_is_coarse(n, static_cast<std::uint32_t>(d));
  }
  if (d > 2 * n) return total_triangles(n);
  if (d == n) return 0;  // Not used for the odd inputs here.
  return count_when_grid_is_fine(n, d);
}

static std::uint64_t solve(std::uint64_t n) {
  const std::uint64_t total = total_triangles(n);
  std::uint64_t d = 1;
  std::uint64_t jumps = 0;
  std::uint64_t seen_sum = 0;

  while (d <= 2 * n) {
    d <<= 1;
    ++jumps;
    if (d <= 2 * n) {
      seen_sum += hit_count(n, d);
    }
  }

  return jumps * total - seen_sum;
}

int main(int argc, char** argv) {
  std::uint64_t n = 123456789ULL;
  if (argc > 1) n = std::strtoull(argv[1], nullptr, 10);
  std::cout << solve(n) << '\n';
  return 0;
}
