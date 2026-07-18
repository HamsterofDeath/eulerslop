#include <cstdint>
#include <iostream>
#include <vector>

using u64 = std::uint64_t;
using u128 = __uint128_t;

std::vector<u64> peerless_tree_counts(int limit) {
  // planted[d][n]: planted trees on n vertices whose root has
  // final degree d (the plant supplies its parent edge).
  std::vector<std::vector<u64>> planted(
      limit + 1,
      std::vector<u64>(limit + 1)
  );
  std::vector<std::vector<u64>> allowed_children(
      limit + 1,
      std::vector<u64>(limit + 1)
  );
  std::vector<u64> all_planted(limit + 1);

  // multisets[d][k][n] is MSET_k(A-A_d) at degree n.
  std::vector<std::vector<std::vector<u64>>> multisets(
      limit + 1
  );
  for (int degree = 1; degree <= limit; ++degree) {
    multisets[degree].assign(
        degree + 1,
        std::vector<u64>(limit + 1)
    );
    multisets[degree][0][0] = 1;
  }

  // Coefficients at size n depend only on smaller sizes, so all
  // mutually recursive degree classes can be advanced together.
  for (int size = 1; size <= limit; ++size) {
    for (int degree = 1; degree <= limit; ++degree) {
      planted[degree][size] =
          multisets[degree][degree - 1][size - 1];
      all_planted[size] += planted[degree][size];
    }
    for (int degree = 1; degree <= limit; ++degree) {
      allowed_children[degree][size] =
          all_planted[size] - planted[degree][size];
    }

    // If M_k(u) marks multisets of exactly k objects, then
    //   k M_k = sum_{j=1}^k B(x^j) M_{k-j}.
    for (int degree = 1; degree <= limit; ++degree) {
      for (
          int cardinality = 1;
          cardinality <= degree;
          ++cardinality
      ) {
        u128 coefficient = 0;
        for (
            int cycle_length = 1;
            cycle_length <= cardinality;
            ++cycle_length
        ) {
          for (
              int child_size = 1;
              cycle_length * child_size <= size;
              ++child_size
          ) {
            coefficient +=
                static_cast<u128>(
                    allowed_children[degree][child_size]
                )
                * multisets[degree][
                    cardinality - cycle_length
                  ][
                    size - cycle_length * child_size
                  ];
          }
        }
        multisets[degree][cardinality][size] =
            static_cast<u64>(
                coefficient / cardinality
            );
      }
    }
  }

  // Vertex-rooted peerless trees.
  std::vector<u64> rooted(limit + 1);
  rooted[1] = 1;
  for (int size = 2; size <= limit; ++size) {
    for (int degree = 1; degree <= limit; ++degree) {
      rooted[size] +=
          multisets[degree][degree][size - 1];
    }
  }

  // Dissymmetry: T = vertex-rooted + edge-rooted
  // - directed-edge-rooted. An admissible edge has distinct
  // endpoint degree classes, so directed edge-rootings are twice
  // the unordered cross-class edge-rootings. Hence T = R-E.
  std::vector<u64> unrooted(limit + 1);
  for (int size = 1; size <= limit; ++size) {
    u128 ordered_cross_class_pairs = 0;
    for (int left_size = 1; left_size < size; ++left_size) {
      u128 same_degree_pairs = 0;
      for (int degree = 1; degree <= limit; ++degree) {
        same_degree_pairs +=
            static_cast<u128>(
                planted[degree][left_size]
            )
            * planted[degree][size - left_size];
      }
      ordered_cross_class_pairs +=
          static_cast<u128>(all_planted[left_size])
              * all_planted[size - left_size]
          - same_degree_pairs;
    }
    const u64 edge_rooted = static_cast<u64>(
        ordered_cross_class_pairs / 2
    );
    unrooted[size] = rooted[size] - edge_rooted;
  }
  return unrooted;
}

int main(int argc, char** argv) {
  const int limit =
      argc > 1 ? std::stoi(argv[1]) : 50;
  const std::vector<u64> counts =
      peerless_tree_counts(limit);

  if (limit >= 10) {
    u64 sample_sum = 0;
    for (int size = 3; size <= 10; ++size) {
      sample_sum += counts[size];
    }
    if (counts[7] != 6 || sample_sum != 74) {
      std::cerr << "sample self-check failed\n";
      return 1;
    }
  }

  u64 result = 0;
  for (int size = 3; size <= limit; ++size) {
    result += counts[size];
  }
  std::cout << result << '\n';
}
