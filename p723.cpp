#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <string>
#include <unordered_map>
#include <vector>

struct Gaussian {
  long long x;
  long long y;
};

struct Key {
  long long x;
  long long y;

  bool operator==(const Key &other) const {
    return x == other.x && y == other.y;
  }
};

struct KeyHash {
  std::size_t operator()(const Key &key) const {
    std::uint64_t a = static_cast<std::uint64_t>(key.x);
    std::uint64_t b = static_cast<std::uint64_t>(key.y);
    a ^= a >> 33;
    a *= 0xff51afd7ed558ccdULL;
    a ^= a >> 33;
    b ^= b >> 33;
    b *= 0xc4ceb9fe1a85ec53ULL;
    b ^= b >> 33;
    return static_cast<std::size_t>(a ^ (b + 0x9e3779b97f4a7c15ULL + (a << 6) + (a >> 2)));
  }
};

static Gaussian multiply(Gaussian a, Gaussian b) {
  __int128 x = static_cast<__int128>(a.x) * b.x - static_cast<__int128>(a.y) * b.y;
  __int128 y = static_cast<__int128>(a.x) * b.y + static_cast<__int128>(a.y) * b.x;
  return {static_cast<long long>(x), static_cast<long long>(y)};
}

static Key canonical_line(long long x, long long y) {
  long long g = std::gcd(std::llabs(x), std::llabs(y));
  x /= g;
  y /= g;
  if (x < 0 || (x == 0 && y < 0)) {
    x = -x;
    y = -y;
  }
  return {x, y};
}

static Key perpendicular(Key key) {
  return canonical_line(-key.y, key.x);
}

static bool key_less(Key a, Key b) {
  if (a.x != b.x) return a.x < b.x;
  return a.y < b.y;
}

static std::string to_string128(__int128 value) {
  if (value == 0) return "0";
  bool negative = value < 0;
  if (negative) value = -value;
  std::string out;
  while (value > 0) {
    out.push_back(static_cast<char>('0' + value % 10));
    value /= 10;
  }
  if (negative) out.push_back('-');
  std::reverse(out.begin(), out.end());
  return out;
}

static Gaussian representation(long long p) {
  for (long long a = 1; a * a <= p; ++a) {
    long long b2 = p - a * a;
    long long b = 0;
    while (b * b < b2) ++b;
    if (b * b == b2) return {a, b};
  }
  std::abort();
}

class Counter {
 public:
  Counter() {
    for (std::size_t i = 0; i < primes_.size(); ++i) {
      Gaussian pi = representation(primes_[i]);
      Gaussian conjugate{pi.x, -pi.y};
      std::vector<Gaussian> pi_powers(max_exponents_[i] + 1, {1, 0});
      std::vector<Gaussian> conjugate_powers(max_exponents_[i] + 1, {1, 0});
      for (int e = 1; e <= max_exponents_[i]; ++e) {
        pi_powers[e] = multiply(pi_powers[e - 1], pi);
        conjugate_powers[e] = multiply(conjugate_powers[e - 1], conjugate);
      }
      for (int e = 0; e <= max_exponents_[i]; ++e) {
        factors_[i][e].reserve(e + 1);
        for (int alpha = 0; alpha <= e; ++alpha) {
          factors_[i][e].push_back(multiply(pi_powers[alpha], conjugate_powers[e - alpha]));
        }
      }
    }
  }

  __int128 solve() {
    return sum_with_limits(max_exponents_);
  }

  __int128 sum_with_limits(const std::array<int, 8> &limits) {
    std::array<int, 8> exponents{};
    return sum_divisors(0, 1, exponents, limits);
  }

  __int128 count_single(std::array<int, 8> exponents) const {
    long long d = 1;
    for (std::size_t i = 0; i < primes_.size(); ++i) {
      for (int k = 0; k < exponents[i]; ++k) d *= primes_[i];
    }
    return count_for_divisor(d, exponents);
  }

 private:
  static constexpr std::array<long long, 8> primes_{5, 13, 17, 29, 37, 41, 53, 61};
  static constexpr std::array<int, 8> max_exponents_{6, 3, 2, 1, 1, 1, 1, 1};
  std::array<std::array<std::vector<Gaussian>, 7>, 8> factors_{};

  __int128 sum_divisors(int index, long long d, std::array<int, 8> &exponents,
                        const std::array<int, 8> &limits) {
    if (index == static_cast<int>(primes_.size())) {
      return count_for_divisor(d, exponents);
    }

    __int128 total = 0;
    long long next_d = d;
    for (int e = 0; e <= limits[index]; ++e) {
      exponents[index] = e;
      total += sum_divisors(index + 1, next_d, exponents, limits);
      next_d *= primes_[index];
    }
    return total;
  }

  std::vector<Gaussian> base_points(const std::array<int, 8> &exponents) const {
    std::vector<Gaussian> base{{1, 0}};
    for (std::size_t i = 0; i < primes_.size(); ++i) {
      std::vector<Gaussian> next;
      next.reserve(base.size() * factors_[i][exponents[i]].size());
      for (Gaussian z : base) {
        for (Gaussian factor : factors_[i][exponents[i]]) {
          next.push_back(multiply(z, factor));
        }
      }
      base.swap(next);
    }
    return base;
  }

  static std::vector<Gaussian> with_units(const std::vector<Gaussian> &base) {
    std::vector<Gaussian> points;
    points.reserve(base.size() * 4);
    for (Gaussian z : base) {
      points.push_back(z);
      points.push_back({-z.y, z.x});
      points.push_back({-z.x, -z.y});
      points.push_back({z.y, -z.x});
    }
    return points;
  }

  __int128 count_for_divisor(long long d, const std::array<int, 8> &exponents) const {
    std::vector<Gaussian> points = with_units(base_points(exponents));
    const long long m = static_cast<long long>(points.size());
    const long long tau = m / 4;

    std::unordered_map<Key, std::vector<unsigned long long>, KeyHash> groups;
    groups.max_load_factor(0.7f);
    groups.reserve(static_cast<std::size_t>(std::max<long long>(16, m * m / 8)));

    for (long long i = 0; i < m; ++i) {
      for (long long j = i + 1; j < m; ++j) {
        long long sx = points[i].x + points[j].x;
        long long sy = points[i].y + points[j].y;
        if (sx == 0 && sy == 0) continue;

        Key key = canonical_line(sx, sy);
        unsigned long long norm = static_cast<unsigned long long>(
            static_cast<__int128>(sx) * sx + static_cast<__int128>(sy) * sy);
        groups[key].push_back(norm);
      }
    }

    for (auto &entry : groups) {
      std::sort(entry.second.begin(), entry.second.end());
    }

    const unsigned long long limit = static_cast<unsigned long long>(4) * d;
    __int128 non_diameter_metric = 0;
    for (const auto &entry : groups) {
      Key key = entry.first;
      Key partner_key = perpendicular(key);
      if (!key_less(key, partner_key)) continue;
      auto partner = groups.find(partner_key);
      if (partner == groups.end()) continue;

      const auto &a = entry.second;
      const auto &b = partner->second;
      long long j = static_cast<long long>(b.size()) - 1;
      for (unsigned long long norm_a : a) {
        while (j >= 0 && static_cast<__int128>(norm_a) + b[static_cast<std::size_t>(j)] > limit) {
          --j;
        }
        non_diameter_metric += j + 1;
      }
    }

    __int128 diameter_quads = static_cast<__int128>(tau) * (2 * tau - 1) * (4 * tau - 3);
    __int128 shared_endpoint_overcount = static_cast<__int128>(m) * (m - 2) / 2;
    return diameter_quads + non_diameter_metric - shared_endpoint_overcount;
  }
};

int main(int argc, char **argv) {
  Counter counter;
  if (argc > 1 && std::string(argv[1]) == "--samples") {
    std::array<int, 8> exponents{};
    std::cout << "f(1)=" << to_string128(counter.count_single(exponents)) << '\n';
    exponents[0] = 1;
    std::cout << "f(sqrt(5))=" << to_string128(counter.count_single(exponents)) << '\n';
    exponents[0] = 2;
    std::cout << "f(5)=" << to_string128(counter.count_single(exponents)) << '\n';

    std::array<int, 8> limits{};
    limits[0] = 2;
    limits[1] = 1;
    std::cout << "S(325)=" << to_string128(counter.sum_with_limits(limits)) << '\n';
    limits = {};
    limits[0] = 1;
    limits[1] = 1;
    limits[2] = 1;
    std::cout << "S(1105)=" << to_string128(counter.sum_with_limits(limits)) << '\n';
    return 0;
  }
  std::cout << to_string128(counter.solve()) << '\n';
  return 0;
}
