#include <algorithm>
#include <array>
#include <cassert>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>

constexpr int PERIMETER_LIMIT = 200;
constexpr long double PI =
    3.141592653589793238462643383279502884L;

struct Point {
  long double x;
  long double y;

  Point operator+(const Point& other) const {
    return {x + other.x, y + other.y};
  }
  Point operator-(const Point& other) const {
    return {x - other.x, y - other.y};
  }
  Point operator*(long double scale) const {
    return {x * scale, y * scale};
  }
};

long double dot(const Point& first, const Point& second) {
  return first.x * second.x + first.y * second.y;
}

long double cross(const Point& first, const Point& second) {
  return first.x * second.y - first.y * second.x;
}

long double norm(const Point& point) {
  return std::sqrt(dot(point, point));
}

using Triangle = std::array<Point, 3>;

long double segment_contribution(Point first, Point second) {
  const Point direction = second - first;
  const long double quadratic_a = dot(direction, direction);
  const long double quadratic_b = 2 * dot(first, direction);
  const long double quadratic_c = dot(first, first) - 1;

  std::vector<long double> parameters{0, 1};
  const long double discriminant =
      quadratic_b * quadratic_b
      - 4 * quadratic_a * quadratic_c;
  if (discriminant > 0) {
    const long double root = std::sqrt(discriminant);
    for (const long double parameter : {
             (-quadratic_b - root) / (2 * quadratic_a),
             (-quadratic_b + root) / (2 * quadratic_a),
         }) {
      if (parameter > 0 && parameter < 1) {
        parameters.push_back(parameter);
      }
    }
  }
  std::sort(parameters.begin(), parameters.end());

  long double area = 0;
  for (std::size_t index = 1;
       index < parameters.size();
       ++index) {
    const Point start =
        first + direction * parameters[index - 1];
    const Point finish =
        first + direction * parameters[index];
    const Point midpoint = (start + finish) * 0.5L;
    if (dot(midpoint, midpoint) <= 1) {
      area += cross(start, finish) / 2;
    } else {
      area += std::atan2(
          cross(start, finish),
          dot(start, finish)
      ) / 2;
    }
  }
  return area;
}

long double intersection_area(
    const Triangle& triangle,
    const Point& centre
) {
  long double area = 0;
  for (int index = 0; index < 3; ++index) {
    area += segment_contribution(
        triangle[index] - centre,
        triangle[(index + 1) % 3] - centre
    );
  }
  return area;
}

Point area_gradient(
    const Triangle& triangle,
    const Point& centre
) {
  std::vector<long double> events{0, 2 * PI};

  for (int index = 0; index < 3; ++index) {
    const Point start = triangle[index];
    const Point edge = triangle[(index + 1) % 3] - start;
    const long double length = norm(edge);
    const Point inward_normal = {-edge.y / length, edge.x / length};
    const long double distance =
        dot(inward_normal, centre - start);
    if (std::abs(distance) < 1) {
      const long double normal_angle =
          std::atan2(inward_normal.y, inward_normal.x);
      const long double offset = std::acos(-distance);
      for (long double angle : {
               normal_angle - offset,
               normal_angle + offset,
           }) {
        angle = std::fmod(angle, 2 * PI);
        if (angle < 0) {
          angle += 2 * PI;
        }
        events.push_back(angle);
      }
    }
  }
  std::sort(events.begin(), events.end());

  Point gradient{0, 0};
  for (std::size_t index = 1; index < events.size(); ++index) {
    const long double begin = events[index - 1];
    const long double end = events[index];
    const long double middle = (begin + end) / 2;
    const Point boundary = centre + Point{
        std::cos(middle), std::sin(middle)
    };

    bool inside = true;
    for (int edge_index = 0; edge_index < 3; ++edge_index) {
      const Point edge =
          triangle[(edge_index + 1) % 3]
          - triangle[edge_index];
      if (cross(
              edge,
              boundary - triangle[edge_index]
          ) < -1e-18L) {
        inside = false;
        break;
      }
    }
    if (inside) {
      gradient.x += std::sin(end) - std::sin(begin);
      gradient.y += -std::cos(end) + std::cos(begin);
    }
  }
  return gradient;
}

long double maximum_step_inside(
    const Triangle& triangle,
    const Point& centre,
    const Point& direction
) {
  long double maximum = 1e100L;
  for (int index = 0; index < 3; ++index) {
    const Point start = triangle[index];
    const Point edge = triangle[(index + 1) % 3] - start;
    const long double current = cross(edge, centre - start);
    const long double change = cross(edge, direction);
    if (change < 0) {
      maximum = std::min(maximum, current / -change);
    }
  }
  return maximum;
}

long double maximize_normalized_overlap(
    const Triangle& triangle,
    Point centre
) {
  long double inverse_hessian[2][2] = {{1, 0}, {0, 1}};
  long double area = intersection_area(triangle, centre);
  Point gradient = area_gradient(triangle, centre);

  for (int iteration = 0; iteration < 100; ++iteration) {
    if (norm(gradient) < 1e-13L) {
      break;
    }

    Point direction{
        inverse_hessian[0][0] * gradient.x
            + inverse_hessian[0][1] * gradient.y,
        inverse_hessian[1][0] * gradient.x
            + inverse_hessian[1][1] * gradient.y,
    };
    if (dot(direction, gradient) <= 0) {
      direction = gradient;
      inverse_hessian[0][0] = inverse_hessian[1][1] = 1;
      inverse_hessian[0][1] = inverse_hessian[1][0] = 0;
    }

    const long double directional_derivative =
        dot(gradient, direction);
    long double step = std::min(
        1.0L,
        0.99L * maximum_step_inside(
            triangle, centre, direction
        )
    );
    Point next_centre;
    long double next_area;
    bool accepted = false;
    for (int search = 0; search < 60; ++search) {
      next_centre = centre + direction * step;
      next_area = intersection_area(triangle, next_centre);
      if (
          next_area
          >= area + 1e-4L * step * directional_derivative
      ) {
        accepted = true;
        break;
      }
      step /= 2;
    }
    if (!accepted) {
      break;
    }

    const Point next_gradient =
        area_gradient(triangle, next_centre);
    const Point displacement = next_centre - centre;
    const Point gradient_change = gradient - next_gradient;
    const long double curvature =
        dot(displacement, gradient_change);

    if (curvature > 1e-18L) {
      const long double rho = 1 / curvature;
      const long double v[2] = {
          gradient_change.x, gradient_change.y
      };
      const long double s[2] = {
          displacement.x, displacement.y
      };
      long double left[2][2];
      long double right[2][2];
      for (int row = 0; row < 2; ++row) {
        for (int column = 0; column < 2; ++column) {
          const long double identity = row == column ? 1 : 0;
          left[row][column] =
              identity - rho * s[row] * v[column];
          right[row][column] =
              identity - rho * v[row] * s[column];
        }
      }
      long double temporary[2][2] = {};
      long double updated[2][2] = {};
      for (int row = 0; row < 2; ++row) {
        for (int column = 0; column < 2; ++column) {
          for (int inner = 0; inner < 2; ++inner) {
            temporary[row][column] +=
                left[row][inner]
                * inverse_hessian[inner][column];
          }
        }
      }
      for (int row = 0; row < 2; ++row) {
        for (int column = 0; column < 2; ++column) {
          for (int inner = 0; inner < 2; ++inner) {
            updated[row][column] +=
                temporary[row][inner] * right[inner][column];
          }
          updated[row][column] += rho * s[row] * s[column];
          inverse_hessian[row][column] = updated[row][column];
        }
      }
    } else {
      inverse_hessian[0][0] = inverse_hessian[1][1] = 1;
      inverse_hessian[0][1] = inverse_hessian[1][0] = 0;
    }

    centre = next_centre;
    area = next_area;
    gradient = next_gradient;
  }
  return area;
}

long double maximum_intersection(int a, int b, int c) {
  const long double x = (
      static_cast<long double>(b) * b
      + static_cast<long double>(c) * c
      - static_cast<long double>(a) * a
  ) / (2 * c);
  const long double y = std::sqrt(
      static_cast<long double>(b) * b - x * x
  );
  const long double triangle_area = c * y / 2;
  const long double radius =
      std::sqrt(triangle_area / PI);

  Triangle triangle{{
      {0, 0},
      {c / radius, 0},
      {x / radius, y / radius},
  }};
  Point incenter = (
      triangle[0] * a
      + triangle[1] * b
      + triangle[2] * c
  ) * (1.0L / (a + b + c));

  return maximize_normalized_overlap(triangle, incenter)
      * radius * radius;
}

long double solve() {
  long double result = 0;
  for (int a = 1; a <= PERIMETER_LIMIT / 3; ++a) {
    for (int b = a; a + 2 * b <= PERIMETER_LIMIT; ++b) {
      const int maximum_c =
          std::min(a + b - 1, PERIMETER_LIMIT - a - b);
      for (int c = b; c <= maximum_c; ++c) {
        if (std::gcd(std::gcd(a, b), c) != 1) {
          continue;
        }
        const int copies =
            PERIMETER_LIMIT / (a + b + c);
        const long long square_sum =
            static_cast<long long>(copies)
            * (copies + 1) * (2 * copies + 1) / 6;
        result += maximum_intersection(a, b, c) * square_sum;
      }
    }
  }
  return result;
}

int main(int argc, char** argv) {
  const long double first = maximum_intersection(3, 4, 5);
  const long double second = maximum_intersection(3, 4, 6);
  assert(std::abs(first - 4.593049L) < 1e-6L);
  assert(std::abs(second - 3.552564L) < 1e-6L);

  if (argc == 4) {
    std::cout << std::fixed << std::setprecision(9)
              << maximum_intersection(
                     std::stoi(argv[1]),
                     std::stoi(argv[2]),
                     std::stoi(argv[3])
                 )
              << '\n';
  } else {
    std::cout << std::fixed << std::setprecision(2)
              << solve() << '\n';
  }
}
