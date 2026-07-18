#include <cstdint>
#include <iostream>
#include <vector>

using u64 = std::uint64_t;

constexpr int OUTPUT_MODULUS = 1'000'000'007;

int minimal_mersenne_root_mod(int exponent) {
  std::vector<unsigned char> quadratic_residue(exponent);
  const u64 half = (static_cast<u64>(exponent) - 1) / 2;
  for (u64 value = 1; value <= half; ++value) {
    quadratic_residue[value * value % exponent] = 1;
  }

  // The two square roots have complementary q-bit patterns.
  // The direct Gauss-sum branch has bits
  // {1} union {j+1 : j is a nonzero residue, j != -1}.
  int direct = 2;
  int complement = 1;
  int power_of_two = 4;
  for (int value = 1; value <= exponent - 2; ++value) {
    if (quadratic_residue[value]) {
      direct += power_of_two;
      if (direct >= OUTPUT_MODULUS) {
        direct -= OUTPUT_MODULUS;
      }
    } else {
      complement += power_of_two;
      if (complement >= OUTPUT_MODULUS) {
        complement -= OUTPUT_MODULUS;
      }
    }
    power_of_two = static_cast<int>(
        2LL * power_of_two % OUTPUT_MODULUS
    );
  }

  // For q=1 (mod 8), (-2/q)=1, so the direct branch
  // has its top bit set and the complement is minimal.
  // For q=5 (mod 8), the direct branch is minimal.
  return exponent % 8 == 1 ? complement : direct;
}

int main(int argc, char** argv) {
  const int exponent =
      argc > 1 ? std::stoi(argv[1]) : 74'207'281;

  if (
      minimal_mersenne_root_mod(5) != 6
      || minimal_mersenne_root_mod(17) != 47'569
  ) {
    std::cerr << "sample self-check failed\n";
    return 1;
  }
  std::cout << minimal_mersenne_root_mod(exponent) << '\n';
}
