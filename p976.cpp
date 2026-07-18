#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>

using i64 = std::int64_t;

constexpr int LIMIT = 10'000'000;
constexpr i64 MODULUS = 1'234'567'891;
constexpr i64 INVERSE_TWO = (MODULUS + 1) / 2;

i64 modulo(i64 value) {
  value %= MODULUS;
  return value < 0 ? value + MODULUS : value;
}

struct Series {
  i64 difference;
  i64 sum;
  i64 previous_previous = 1;
  i64 previous;
  i64 even_total = 1;
  i64 odd_total;

  Series(i64 u, i64 v)
      : difference(modulo(u - v)),
        sum(modulo(u + v)),
        previous(difference),
        odd_total(difference) {}

  void append(int index, i64 inverse) {
    const i64 coefficient = (
        difference * previous
        + modulo(sum + index - 2) * previous_previous
    ) % MODULUS * inverse % MODULUS;
    previous_previous = previous;
    previous = coefficient;
    if ((index & 1) == 0) {
      even_total = modulo(even_total + coefficient);
    } else {
      odd_total = modulo(odd_total + coefficient);
    }
  }
};

i64 winning_tuples(int maximum_strips, int maximum_length) {
  const i64 even_classes = maximum_length / 2;
  const i64 one_mod_four_classes = (maximum_length + 3) / 4;
  const i64 three_mod_four_classes = (maximum_length + 1) / 4;

  // Total multisets, the all-even class multiplicities, and the
  // corresponding term where the two odd-length classes are separated.
  std::array<Series, 3> series{
      Series(maximum_length, 0),
      Series(maximum_length, even_classes),
      Series(
          even_classes + one_mod_four_classes,
          even_classes + three_mod_four_classes
      ),
  };

  std::vector<i64> inverses(maximum_strips + 1);
  if (maximum_strips >= 1) {
    inverses[1] = 1;
  }
  for (int index = 2; index <= maximum_strips; ++index) {
    inverses[index] = MODULUS - (
        (MODULUS / index) * inverses[MODULUS % index]
        % MODULUS
    );
    for (Series& current : series) {
      current.append(index, inverses[index]);
    }
  }

  const i64 pairable_even = (
      series[1].even_total + series[2].even_total
  ) % MODULUS * INVERSE_TWO % MODULUS;
  const i64 favorable_odd = (
      series[1].odd_total + series[2].odd_total
  ) % MODULUS * INVERSE_TWO % MODULUS;

  return modulo(
      series[0].even_total - pairable_even + favorable_odd
  );
}

int main(int argc, char** argv) {
  assert(winning_tuples(2, 4) == 7);
  assert(winning_tuples(5, 10) == 901);
  if (argc == 3) {
    std::cout << winning_tuples(
        std::stoi(argv[1]), std::stoi(argv[2])
    ) << '\n';
  } else {
    std::cout << winning_tuples(LIMIT, LIMIT) << '\n';
  }
}
