#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <optional>
#include <string>
#include <vector>

using i64 = std::int64_t;
using i128 = __int128;

constexpr i64 MODULUS = 1'000'000'007;
constexpr i64 PERTURBATION_DENOMINATOR = 1'000'003;
constexpr int DIMENSION = 5;
constexpr int FACET_COUNT = 15;
constexpr std::array<i64, DIMENSION> BASES{2, 3, 5, 7, 11};

using Vector = std::array<i64, DIMENSION>;
using Matrix = std::array<Vector, DIMENSION>;

i64 modulo(i64 value) {
  value %= MODULUS;
  return value < 0 ? value + MODULUS : value;
}

i64 modular_power(i64 base, i64 exponent) {
  exponent %= MODULUS - 1;
  if (exponent < 0) {
    exponent += MODULUS - 1;
  }
  i64 result = 1;
  while (exponent != 0) {
    if ((exponent & 1) != 0) {
      result = result * base % MODULUS;
    }
    base = base * base % MODULUS;
    exponent >>= 1;
  }
  return result;
}

i64 determinant(
    const std::vector<std::vector<i64>>& matrix
) {
  const int size = matrix.size();
  if (size == 0) {
    return 1;
  }
  i64 result = 0;
  for (int column = 0; column < size; ++column) {
    std::vector<std::vector<i64>> minor(
        size - 1, std::vector<i64>(size - 1)
    );
    for (int row = 1; row < size; ++row) {
      int target_column = 0;
      for (int source_column = 0;
           source_column < size;
           ++source_column) {
        if (source_column != column) {
          minor[row - 1][target_column++] =
              matrix[row][source_column];
        }
      }
    }
    result += (column % 2 == 0 ? 1 : -1)
        * matrix[0][column] * determinant(minor);
  }
  return result;
}

i64 matrix_determinant(const Matrix& matrix) {
  std::vector<std::vector<i64>> dynamic(
      DIMENSION, std::vector<i64>(DIMENSION)
  );
  for (int row = 0; row < DIMENSION; ++row) {
    for (int column = 0; column < DIMENSION; ++column) {
      dynamic[row][column] = matrix[row][column];
    }
  }
  return determinant(dynamic);
}

Matrix adjugate(const Matrix& matrix) {
  Matrix result{};
  for (int row = 0; row < DIMENSION; ++row) {
    for (int column = 0; column < DIMENSION; ++column) {
      std::vector<std::vector<i64>> minor(
          DIMENSION - 1,
          std::vector<i64>(DIMENSION - 1)
      );
      int target_row = 0;
      for (int source_row = 0;
           source_row < DIMENSION;
           ++source_row) {
        if (source_row == column) {
          continue;
        }
        int target_column = 0;
        for (int source_column = 0;
             source_column < DIMENSION;
             ++source_column) {
          if (source_column != row) {
            minor[target_row][target_column++] =
                matrix[source_row][source_column];
          }
        }
        ++target_row;
      }
      result[row][column] =
          ((row + column) % 2 == 0 ? 1 : -1)
          * determinant(minor);
    }
  }
  return result;
}

std::array<Vector, FACET_COUNT> facet_rows() {
  std::array<Vector, FACET_COUNT> rows{};
  for (int coordinate = 0;
       coordinate < DIMENSION;
       ++coordinate) {
    rows[coordinate][coordinate] = -1;
  }

  int facet = DIMENSION;
  for (int first = 0; first < DIMENSION; ++first) {
    for (int second = first + 1;
         second < DIMENSION;
         ++second) {
      rows[facet][first] = 1;
      rows[facet][second] = 1;
      ++facet;
    }
  }
  return rows;
}

struct ConeType {
  std::array<int, DIMENSION> facets;
  i64 active_determinant;
  Matrix active_adjugate;
  Matrix rays;
  i64 ray_determinant;
  Matrix ray_adjugate;
  i64 denominator_inverse;
};

std::vector<ConeType> make_cone_types(
    const std::array<Vector, FACET_COUNT>& rows
) {
  std::vector<ConeType> cones;

  for (int a = 0; a < FACET_COUNT; ++a) {
    for (int b = a + 1; b < FACET_COUNT; ++b) {
      for (int c = b + 1; c < FACET_COUNT; ++c) {
        for (int d = c + 1; d < FACET_COUNT; ++d) {
          for (int e = d + 1; e < FACET_COUNT; ++e) {
            ConeType cone;
            cone.facets = {a, b, c, d, e};
            Matrix active{};
            for (int row = 0; row < DIMENSION; ++row) {
              active[row] = rows[cone.facets[row]];
            }

            i64 active_determinant =
                matrix_determinant(active);
            if (active_determinant == 0) {
              continue;
            }
            Matrix active_adjugate = adjugate(active);
            if (active_determinant < 0) {
              active_determinant = -active_determinant;
              for (Vector& row : active_adjugate) {
                for (i64& value : row) {
                  value = -value;
                }
              }
            }
            cone.active_determinant = active_determinant;
            cone.active_adjugate = active_adjugate;

            for (int ray = 0; ray < DIMENSION; ++ray) {
              i64 divisor = 0;
              for (int coordinate = 0;
                   coordinate < DIMENSION;
                   ++coordinate) {
                cone.rays[coordinate][ray] =
                    -active_adjugate[coordinate][ray];
                divisor = std::gcd(
                    divisor,
                    std::abs(cone.rays[coordinate][ray])
                );
              }
              for (int coordinate = 0;
                   coordinate < DIMENSION;
                   ++coordinate) {
                cone.rays[coordinate][ray] /= divisor;
              }
            }

            i64 ray_determinant =
                matrix_determinant(cone.rays);
            Matrix ray_adjugate = adjugate(cone.rays);
            if (ray_determinant < 0) {
              ray_determinant = -ray_determinant;
              for (Vector& row : ray_adjugate) {
                for (i64& value : row) {
                  value = -value;
                }
              }
            }
            cone.ray_determinant = ray_determinant;
            cone.ray_adjugate = ray_adjugate;
            assert(
                ray_determinant == 1
                || ray_determinant == 4
                || ray_determinant == 16
            );

            i64 denominator = 1;
            for (int ray = 0; ray < DIMENSION; ++ray) {
              i64 monomial = 1;
              for (int coordinate = 0;
                   coordinate < DIMENSION;
                   ++coordinate) {
                monomial = monomial * modular_power(
                    BASES[coordinate],
                    cone.rays[coordinate][ray]
                ) % MODULUS;
              }
              denominator = denominator
                  * modulo(1 - monomial) % MODULUS;
            }
            assert(denominator != 0);
            cone.denominator_inverse =
                modular_power(denominator, MODULUS - 2);
            cones.push_back(cone);
          }
        }
      }
    }
  }
  assert(cones.size() == 1548);
  return cones;
}

i128 ceil_div(i128 numerator, i128 denominator) {
  if (numerator >= 0) {
    return (numerator + denominator - 1) / denominator;
  }
  return -((-numerator) / denominator);
}

i64 monomial(const std::array<i64, DIMENSION>& point) {
  i64 result = 1;
  for (int coordinate = 0;
       coordinate < DIMENSION;
       ++coordinate) {
    result = result * modular_power(
        BASES[coordinate], point[coordinate]
    ) % MODULUS;
  }
  return result;
}

i64 cone_numerator(
    const ConeType& cone,
    const std::array<i128, DIMENSION>& vertex_numerators,
    i128 vertex_denominator
) {
  std::array<i64, DIMENSION> lower{};
  std::array<i64, DIMENSION> upper{};
  for (int coordinate = 0;
       coordinate < DIMENSION;
       ++coordinate) {
    i64 minimum_shift = 0;
    i64 maximum_shift = 0;
    for (int ray = 0; ray < DIMENSION; ++ray) {
      minimum_shift +=
          std::min<i64>(0, cone.rays[coordinate][ray]);
      maximum_shift +=
          std::max<i64>(0, cone.rays[coordinate][ray]);
    }
    lower[coordinate] = static_cast<i64>(
        ceil_div(
            vertex_numerators[coordinate],
            vertex_denominator
        )
    ) + minimum_shift;
    upper[coordinate] = static_cast<i64>(
        ceil_div(
            vertex_numerators[coordinate],
            vertex_denominator
        )
    ) + maximum_shift;
  }

  i64 result = 0;
  int point_count = 0;
  std::array<i64, DIMENSION> point{};
  for (point[0] = lower[0]; point[0] < upper[0]; ++point[0]) {
    for (point[1] = lower[1]; point[1] < upper[1]; ++point[1]) {
      for (point[2] = lower[2]; point[2] < upper[2]; ++point[2]) {
        for (point[3] = lower[3]; point[3] < upper[3]; ++point[3]) {
          for (point[4] = lower[4];
               point[4] < upper[4];
               ++point[4]) {
            std::array<i128, DIMENSION> difference{};
            for (int coordinate = 0;
                 coordinate < DIMENSION;
                 ++coordinate) {
              difference[coordinate] =
                  static_cast<i128>(point[coordinate])
                      * vertex_denominator
                  - vertex_numerators[coordinate];
            }

            const i128 parameter_denominator =
                static_cast<i128>(cone.ray_determinant)
                * vertex_denominator;
            bool in_parallelepiped = true;
            for (int parameter = 0;
                 parameter < DIMENSION;
                 ++parameter) {
              i128 numerator = 0;
              for (int coordinate = 0;
                   coordinate < DIMENSION;
                   ++coordinate) {
                numerator +=
                    static_cast<i128>(
                        cone.ray_adjugate[parameter][coordinate]
                    ) * difference[coordinate];
              }
              if (
                  numerator < 0
                  || numerator >= parameter_denominator
              ) {
                in_parallelepiped = false;
                break;
              }
            }
            if (in_parallelepiped) {
              result = modulo(result + monomial(point));
              ++point_count;
            }
          }
        }
      }
    }
  }
  assert(point_count == cone.ray_determinant);
  return result;
}

struct PolytopeEvaluator {
  std::array<Vector, FACET_COUNT> rows = facet_rows();
  std::vector<ConeType> cones = make_cone_types(rows);

  std::optional<i64> evaluate_with_perturbation(
      const std::array<i64, 10>& bounds,
      int attempt
  ) const {
    std::array<i64, FACET_COUNT> right_sides{};
    i64 state = 104729 + 7919 * attempt;
    for (int facet = DIMENSION;
         facet < FACET_COUNT;
         ++facet) {
      state = (
          static_cast<i128>(state) * 48271 + 1
      ) % (PERTURBATION_DENOMINATOR - 1);
      const i64 offset = state + 1;
      right_sides[facet] =
          bounds[facet - DIMENSION]
              * PERTURBATION_DENOMINATOR
          + offset;
    }

    i64 result = 0;
    int vertex_count = 0;
    for (const ConeType& cone : cones) {
      std::array<i128, DIMENSION> vertex_numerators{};
      for (int coordinate = 0;
           coordinate < DIMENSION;
           ++coordinate) {
        for (int row = 0; row < DIMENSION; ++row) {
          vertex_numerators[coordinate] +=
              static_cast<i128>(
                  cone.active_adjugate[coordinate][row]
              ) * right_sides[cone.facets[row]];
        }
      }

      bool feasible = true;
      int active_count = 0;
      for (int facet = 0; facet < FACET_COUNT; ++facet) {
        i128 left_side = 0;
        for (int coordinate = 0;
             coordinate < DIMENSION;
             ++coordinate) {
          left_side +=
              static_cast<i128>(rows[facet][coordinate])
              * vertex_numerators[coordinate];
        }
        const i128 right_side =
            static_cast<i128>(right_sides[facet])
            * cone.active_determinant;
        if (left_side > right_side) {
          feasible = false;
          break;
        }
        if (left_side == right_side) {
          ++active_count;
        }
      }
      if (!feasible) {
        continue;
      }
      if (active_count != DIMENSION) {
        return std::nullopt;
      }

      const i128 vertex_denominator =
          static_cast<i128>(cone.active_determinant)
          * PERTURBATION_DENOMINATOR;
      const i64 numerator = cone_numerator(
          cone, vertex_numerators, vertex_denominator
      );
      result = modulo(
          result + numerator * cone.denominator_inverse
      );
      ++vertex_count;
    }
    assert(vertex_count != 0);
    return result;
  }

  i64 evaluate(const std::array<i64, 10>& bounds) const {
    for (int attempt = 0; attempt < 20; ++attempt) {
      const std::optional<i64> result =
          evaluate_with_perturbation(bounds, attempt);
      if (result.has_value()) {
        return *result;
      }
    }
    assert(false && "failed to find a generic perturbation");
    return 0;
  }
};

i64 solve(const PolytopeEvaluator& evaluator) {
  std::array<i64, 1000> sequence{};
  sequence[0] = 1;
  sequence[1] = 7;
  for (int index = 2; index < static_cast<int>(sequence.size());
       ++index) {
    sequence[index] = (
        7 * sequence[index - 1]
        + sequence[index - 2] * sequence[index - 2]
    ) % MODULUS;
  }

  i64 result = 0;
  for (int block = 0; block < 100; ++block) {
    std::array<i64, 10> bounds{};
    std::copy_n(
        sequence.begin() + 10 * block,
        10,
        bounds.begin()
    );
    result = modulo(result + evaluator.evaluate(bounds));
  }
  return result;
}

int main(int argc, char** argv) {
  const PolytopeEvaluator evaluator;
  assert(evaluator.evaluate({2, 2, 2, 2, 2, 2, 2, 2, 2, 2})
      == 7120);
  assert(evaluator.evaluate({1, 2, 3, 4, 5, 6, 7, 8, 9, 10})
      == 799809376);
  if (argc == 11) {
    std::array<i64, 10> bounds{};
    for (int index = 0; index < 10; ++index) {
      bounds[index] = std::stoll(argv[index + 1]);
    }
    std::cout << evaluator.evaluate(bounds) << '\n';
    return 0;
  }
  std::cout << solve(evaluator) << '\n';
}
