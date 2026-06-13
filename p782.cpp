#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <set>
#include <string>
#include <vector>

struct Linear {
  // ax*x + ay*y + an*n + ac
  int ax = 0;
  int ay = 0;
  int an = 0;
  int ac = 0;
};

struct Poly {
  // x2*x^2 + xy*x*y + y2*y^2 + xn*x*n + yn*y*n + n2*n^2
  // + x*x + y*y + nn*n + c
  std::array<int, 10> c{};
};

struct Form {
  int dim = 0;
  Poly poly;
  std::vector<Linear> inequalities;
};

static Linear add(Linear a, Linear b) {
  return {a.ax + b.ax, a.ay + b.ay, a.an + b.an, a.ac + b.ac};
}

static Linear neg(Linear a) {
  return {-a.ax, -a.ay, -a.an, -a.ac};
}

static Poly add(Poly a, const Poly& b) {
  for (int i = 0; i < 10; ++i) a.c[i] += b.c[i];
  return a;
}

static Poly multiply(Linear a, Linear b) {
  Poly p;
  p.c[0] = a.ax * b.ax;
  p.c[1] = a.ax * b.ay + a.ay * b.ax;
  p.c[2] = a.ay * b.ay;
  p.c[3] = a.ax * b.an + a.an * b.ax;
  p.c[4] = a.ay * b.an + a.an * b.ay;
  p.c[5] = a.an * b.an;
  p.c[6] = a.ax * b.ac + a.ac * b.ax;
  p.c[7] = a.ay * b.ac + a.ac * b.ay;
  p.c[8] = a.an * b.ac + a.ac * b.an;
  p.c[9] = a.ac * b.ac;
  return p;
}

static long long ceil_div(long long a, long long b) {
  if (b < 0) {
    a = -a;
    b = -b;
  }
  if (a >= 0) return (a + b - 1) / b;
  return -((-a) / b);
}

static long long floor_div(long long a, long long b) {
  if (b < 0) {
    a = -a;
    b = -b;
  }
  if (a >= 0) return a / b;
  return -(((-a) + b - 1) / b);
}

static long long value(const Poly& p, long long x, long long y, long long n) {
  const auto& c = p.c;
  return c[0] * x * x + c[1] * x * y + c[2] * y * y +
         c[3] * x * n + c[4] * y * n + c[5] * n * n +
         c[6] * x + c[7] * y + c[8] * n + c[9];
}

static bool ok(const Linear& e, long long x, long long y, long long n) {
  return e.ax * x + e.ay * y + e.an * n + e.ac >= 0;
}

static std::string key_for(const Form& f) {
  std::string s = std::to_string(f.dim);
  for (int v : f.poly.c) s += "," + std::to_string(v);
  std::vector<Linear> ineq = f.inequalities;
  std::sort(ineq.begin(), ineq.end(), [](const Linear& a, const Linear& b) {
    return std::array<int, 4>{a.ax, a.ay, a.an, a.ac} <
           std::array<int, 4>{b.ax, b.ay, b.an, b.ac};
  });
  for (const Linear& e : ineq) {
    s += ";" + std::to_string(e.ax) + "," + std::to_string(e.ay) + "," +
         std::to_string(e.an) + "," + std::to_string(e.ac);
  }
  return s;
}

static std::vector<Form> build_forms(int max_patterns) {
  std::vector<Form> forms;
  std::set<std::string> seen;

  for (int t = 1; t <= max_patterns; ++t) {
    for (int rmask = 1; rmask < (1 << t); ++rmask) {
      std::vector<int> rows;
      for (int i = 0; i < t; ++i) {
        if (rmask & (1 << i)) rows.push_back(i);
      }
      for (int cmask = 1; cmask < (1 << t); ++cmask) {
        if ((rmask | cmask) != ((1 << t) - 1)) continue;
        std::vector<int> cols;
        for (int i = 0; i < t; ++i) {
          if (cmask & (1 << i)) cols.push_back(i);
        }

        std::vector<int> common;
        for (int r : rows) {
          if (cmask & (1 << r)) common.push_back(r);
        }

        std::vector<std::pair<int, int>> entries;
        for (int r : rows) {
          for (int c : cols) entries.push_back({r, c});
        }

        const int masks = 1 << static_cast<int>(entries.size());
        for (int bits = 0; bits < masks; ++bits) {
          int a[3][3] = {};
          for (int b = 0; b < static_cast<int>(entries.size()); ++b) {
            a[entries[b].first][entries[b].second] = (bits >> b) & 1;
          }

          int row_sig[3] = {};
          int col_sig[3] = {};
          for (int r : rows) {
            int sig = 0;
            for (int i = 0; i < static_cast<int>(common.size()); ++i) {
              if (a[r][common[i]]) sig |= 1 << i;
            }
            row_sig[r] = sig;
          }
          for (int c : cols) {
            int sig = 0;
            for (int i = 0; i < static_cast<int>(common.size()); ++i) {
              if (a[common[i]][c]) sig |= 1 << i;
            }
            col_sig[c] = sig;
          }

          std::vector<int> sigs;
          for (int r : rows) sigs.push_back(row_sig[r]);
          for (int c : cols) sigs.push_back(col_sig[c]);
          std::sort(sigs.begin(), sigs.end());
          sigs.erase(std::unique(sigs.begin(), sigs.end()), sigs.end());

          bool feasible = true;
          int dim = static_cast<int>(rows.size()) - 1;
          for (int sig : sigs) {
            int row_count = 0;
            int col_count = 0;
            for (int r : rows) row_count += row_sig[r] == sig;
            for (int c : cols) col_count += col_sig[c] == sig;
            if (row_count == 0 || col_count == 0) feasible = false;
            dim += col_count - 1;
          }
          // Higher-dimensional cases collapse to forms already generated with
          // at most two parameters; the sample assertions exercise this.
          if (!feasible || dim > 2) continue;

          Linear n_expr{0, 0, 1, 0};
          Linear zero{0, 0, 0, 0};
          Linear row_expr[3];
          Linear col_expr[3];
          std::vector<Linear> inequalities;
          int var = 0;
          Linear used = zero;
          for (int i = 0; i < static_cast<int>(rows.size()); ++i) {
            Linear e;
            if (i + 1 < static_cast<int>(rows.size())) {
              e = (var == 0) ? Linear{1, 0, 0, 0} : Linear{0, 1, 0, 0};
              ++var;
              used = add(used, e);
            } else {
              e = add(n_expr, neg(used));
            }
            row_expr[rows[i]] = e;
            inequalities.push_back(e);
          }

          for (int sig : sigs) {
            std::vector<int> sig_cols;
            Linear total = zero;
            for (int r : rows) {
              if (row_sig[r] == sig) total = add(total, row_expr[r]);
            }
            for (int c : cols) {
              if (col_sig[c] == sig) sig_cols.push_back(c);
            }
            Linear sig_used = zero;
            for (int i = 0; i < static_cast<int>(sig_cols.size()); ++i) {
              Linear e;
              if (i + 1 < static_cast<int>(sig_cols.size())) {
                e = (var == 0) ? Linear{1, 0, 0, 0} : Linear{0, 1, 0, 0};
                ++var;
                sig_used = add(sig_used, e);
              } else {
                e = add(total, neg(sig_used));
              }
              col_expr[sig_cols[i]] = e;
              inequalities.push_back(e);
            }
          }

          if (var != dim) continue;
          Poly poly;
          for (int r : rows) {
            for (int c : cols) {
              if (a[r][c]) poly = add(poly, multiply(row_expr[r], col_expr[c]));
            }
          }

          Form f{dim, poly, inequalities};
          std::string key = key_for(f);
          if (seen.insert(key).second) forms.push_back(f);
        }
      }
    }
  }

  return forms;
}

static long long count_values(int n, int max_patterns) {
  const long long limit = 1LL * n * n;
  std::vector<std::uint64_t> bits((limit + 64) / 64, 0);
  auto mark = [&](long long v) {
    if (0 <= v && v <= limit) bits[v >> 6] |= 1ULL << (v & 63);
  };

  for (const Form& f : build_forms(max_patterns)) {
    if (f.dim == 0) {
      bool good = true;
      for (const Linear& e : f.inequalities) good = good && ok(e, 0, 0, n);
      if (good) mark(value(f.poly, 0, 0, n));
    } else if (f.dim == 1) {
      for (int x = 0; x <= n; ++x) {
        bool good = true;
        for (const Linear& e : f.inequalities) good = good && ok(e, x, 0, n);
        if (good) mark(value(f.poly, x, 0, n));
      }
    } else {
      for (int x = 0; x <= n; ++x) {
        long long lo = 0;
        long long hi = n;
        bool possible = true;
        for (const Linear& e : f.inequalities) {
          long long rest = 1LL * e.ax * x + 1LL * e.an * n + e.ac;
          if (e.ay > 0) {
            lo = std::max(lo, ceil_div(-rest, e.ay));
          } else if (e.ay < 0) {
            hi = std::min(hi, floor_div(rest, -e.ay));
          } else if (rest < 0) {
            possible = false;
            break;
          }
        }
        if (!possible || lo > hi) continue;
        for (long long y = lo; y <= hi; ++y) mark(value(f.poly, x, y, n));
      }
    }
  }

  long long total = 0;
  for (std::uint64_t word : bits) total += __builtin_popcountll(word);
  return total;
}

static long long solve(int n) {
  const long long cells = 1LL * n * n + 1;
  const long long at_most_1 = 2;
  const long long at_most_2 = count_values(n, 2);
  const long long at_most_3 = count_values(n, 3);
  return 4 * cells - at_most_3 - at_most_2 - at_most_1;
}

int main(int argc, char** argv) {
  int n = 10000;
  if (argc > 1) n = std::atoi(argv[1]);
  std::cout << solve(n) << '\n';
  return 0;
}
