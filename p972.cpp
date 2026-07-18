#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <string>
#include <unordered_map>
#include <vector>

using i64 = std::int64_t;
using u64 = std::uint64_t;

constexpr int LIMIT = 12;

struct Rational {
  int numerator;
  int denominator;
};

struct Vector {
  i64 x;
  i64 y;
  i64 z;
};

struct Plane {
  i64 x;
  i64 y;
  i64 z;

  bool operator==(const Plane& other) const {
    return x == other.x && y == other.y && z == other.z;
  }
};

u64 mix(u64 value) {
  value ^= value >> 30;
  value *= 0xbf58476d1ce4e5b9ULL;
  value ^= value >> 27;
  value *= 0x94d049bb133111ebULL;
  return value ^ (value >> 31);
}

struct PlaneHash {
  std::size_t operator()(const Plane& plane) const {
    return mix(static_cast<u64>(plane.x))
        ^ mix(static_cast<u64>(plane.y) + 0x9e3779b97f4a7c15ULL)
        ^ mix(static_cast<u64>(plane.z) + 0x3c6ef372fe94f82aULL);
  }
};

std::vector<Rational> rationals(int limit) {
  std::vector<Rational> result;
  for (int denominator = 1;
       denominator <= limit;
       ++denominator) {
    for (int numerator = -denominator;
         numerator <= denominator;
         ++numerator) {
      if (std::gcd(std::abs(numerator), denominator) == 1) {
        result.push_back({numerator, denominator});
      }
    }
  }
  return result;
}

std::vector<Vector> lifted_points(int limit) {
  const std::vector<Rational> values = rationals(limit);
  std::vector<Vector> points;

  for (const Rational& x : values) {
    for (const Rational& y : values) {
      const i64 x_numerator = x.numerator;
      const i64 x_denominator = x.denominator;
      const i64 y_numerator = y.numerator;
      const i64 y_denominator = y.denominator;
      if (
          x_numerator * x_numerator
                  * y_denominator * y_denominator
              + y_numerator * y_numerator
                  * x_denominator * x_denominator
          >= x_denominator * x_denominator
                  * y_denominator * y_denominator
      ) {
        continue;
      }

      Vector point{
          x_numerator * x_denominator
              * y_denominator * y_denominator,
          y_numerator * y_denominator
              * x_denominator * x_denominator,
          x_denominator * x_denominator
                  * y_denominator * y_denominator
              + x_numerator * x_numerator
                  * y_denominator * y_denominator
              + y_numerator * y_numerator
                  * x_denominator * x_denominator,
      };
      const i64 divisor = std::gcd(
          std::gcd(std::abs(point.x), std::abs(point.y)),
          point.z
      );
      point.x /= divisor;
      point.y /= divisor;
      point.z /= divisor;
      points.push_back(point);
    }
  }
  return points;
}

Plane plane_through(const Vector& first, const Vector& second) {
  Plane plane{
      first.y * second.z - first.z * second.y,
      first.z * second.x - first.x * second.z,
      first.x * second.y - first.y * second.x,
  };
  const i64 divisor = std::gcd(
      std::gcd(std::abs(plane.x), std::abs(plane.y)),
      std::abs(plane.z)
  );
  assert(divisor != 0);
  plane.x /= divisor;
  plane.y /= divisor;
  plane.z /= divisor;

  if (
      plane.x < 0
      || (plane.x == 0 && plane.y < 0)
      || (plane.x == 0 && plane.y == 0 && plane.z < 0)
  ) {
    plane.x = -plane.x;
    plane.y = -plane.y;
    plane.z = -plane.z;
  }
  return plane;
}

u64 triple_count(int limit) {
  const std::vector<Vector> points = lifted_points(limit);
  std::unordered_map<Plane, int, PlaneHash> counts;
  counts.reserve(2 * points.size());

  u64 result = 0;
  for (std::size_t first = 0; first < points.size(); ++first) {
    counts.clear();
    for (std::size_t second = 0;
         second < points.size();
         ++second) {
      if (first != second) {
        ++counts[plane_through(points[first], points[second])];
      }
    }
    for (const auto& [plane, count] : counts) {
      static_cast<void>(plane);
      result += static_cast<u64>(count) * (count - 1);
    }
  }
  return result;
}

int main(int argc, char** argv) {
  assert(triple_count(2) == 24);
  assert(triple_count(3) == 1296);
  const int limit = argc > 1 ? std::stoi(argv[1]) : LIMIT;
  std::cout << triple_count(limit) << '\n';
}
