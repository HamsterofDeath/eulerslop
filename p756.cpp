#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

static constexpr int TARGET_N = 12'345'678;
static constexpr int TARGET_M = 12'345;

static std::vector<int> totients(int n) {
  std::vector<int> phi(n + 1);
  for (int i = 0; i <= n; ++i) phi[i] = i;
  for (int p = 2; p <= n; ++p) {
    if (phi[p] != p) continue;
    for (int multiple = p; multiple <= n; multiple += p) {
      phi[multiple] -= phi[multiple] / p;
    }
  }
  return phi;
}

static long double expected_error(int n, int m) {
  std::vector<int> phi = totients(n);

  long double error = 0;
  long double compensation = 0;
  long double missed_weight = static_cast<long double>(n - m) / n;

  for (int k = 1; k <= n - m; ++k) {
    long double addend = static_cast<long double>(phi[k]) * missed_weight - compensation;
    long double next = error + addend;
    compensation = (next - error) - addend;
    error = next;
    missed_weight *= static_cast<long double>(n - k - m) / (n - k);
  }

  return error;
}

int main(int argc, char **argv) {
  int n = TARGET_N;
  int m = TARGET_M;
  if (argc > 2) {
    n = std::stoi(argv[1]);
    m = std::stoi(argv[2]);
  }
  std::cout << std::fixed << std::setprecision(6) << static_cast<double>(expected_error(n, m)) << '\n';
  return 0;
}
