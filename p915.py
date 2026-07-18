"""Project Euler Problem 915: Nested Recursive Sequence.

The recurrence restarts modulo each sequence value, which gives the strong
divisibility property

    gcd(s(a), s(b)) = s(gcd(a, b)).

Consequently every summand is s(s(gcd(a, b))).  These nested values are
eventually periodic modulo 123456789, and a prefix sum of that period lets us
group all d for which floor(N/d) is equal.  The number of ordered coprime pairs
up to q is 2*sum(phi(k), k <= q)-1.
"""

from array import array
from functools import cache


MODULUS = 123_456_789
TARGET = 10**8
TOTIENT_SIEVE_LIMIT = 10**6


def sequence_cycle(modulus: int) -> tuple[list[int], int, int]:
    """Return values before repetition, cycle start index, and cycle length."""
    values = []
    first_index: dict[int, int] = {}
    value = 1
    index = 1

    while value not in first_index:
        first_index[value] = index
        values.append(value)
        value = (pow(value - 1, 3, modulus) + 2) % modulus
        index += 1

    cycle_start = first_index[value]
    return values, cycle_start, index - cycle_start


def periodic_value(cycle_data: tuple[list[int], int, int], index: int) -> int:
    values, cycle_start, period = cycle_data
    if index <= len(values):
        return values[index - 1]
    reduced_index = cycle_start + (index - cycle_start) % period
    return values[reduced_index - 1]


OUTER_CYCLE = sequence_cycle(MODULUS)
INDEX_CYCLE = sequence_cycle(OUTER_CYCLE[2])

assert OUTER_CYCLE[1:] == (54, 33_705)
assert INDEX_CYCLE[1:] == (3, 420)


def nested_sequence_value(index: int) -> int:
    """Return s(s(index)) modulo MODULUS."""
    if index <= 4:
        exact_value = 1
        for _ in range(1, index):
            exact_value = (exact_value - 1) ** 3 + 2
        outer_index = exact_value
    else:
        # s(index) is already beyond the outer preperiod. Its residue modulo
        # the outer period determines the required point in that cycle.
        index_residue = periodic_value(INDEX_CYCLE, index)
        outer_index = OUTER_CYCLE[1] + (
            index_residue - OUTER_CYCLE[1]
        ) % OUTER_CYCLE[2]
    return periodic_value(OUTER_CYCLE, outer_index)


NESTED_PREFIX_LENGTH = 4
NESTED_PERIOD = 420
NESTED_PREFIX = [
    nested_sequence_value(index) for index in range(1, NESTED_PREFIX_LENGTH + 1)
]
NESTED_CYCLE = [
    nested_sequence_value(index)
    for index in range(
        NESTED_PREFIX_LENGTH + 1,
        NESTED_PREFIX_LENGTH + NESTED_PERIOD + 1,
    )
]

NESTED_CYCLE_PREFIX = [0]
for value in NESTED_CYCLE:
    NESTED_CYCLE_PREFIX.append((NESTED_CYCLE_PREFIX[-1] + value) % MODULUS)


def nested_prefix_sum(limit: int) -> int:
    """Return sum(s(s(d)), d <= limit) modulo MODULUS."""
    if limit <= 0:
        return 0
    if limit <= NESTED_PREFIX_LENGTH:
        return sum(NESTED_PREFIX[:limit]) % MODULUS

    complete_periods, remainder = divmod(
        limit - NESTED_PREFIX_LENGTH,
        NESTED_PERIOD,
    )
    return (
        sum(NESTED_PREFIX)
        + complete_periods * NESTED_CYCLE_PREFIX[-1]
        + NESTED_CYCLE_PREFIX[remainder]
    ) % MODULUS


def totient_prefix_table(limit: int) -> array:
    totients = array("I", range(limit + 1))
    for prime in range(2, limit + 1):
        if totients[prime] == prime:
            for multiple in range(prime, limit + 1, prime):
                totients[multiple] -= totients[multiple] // prime

    prefix = array("Q", [0]) * (limit + 1)
    running_sum = 0
    for number in range(1, limit + 1):
        running_sum += totients[number]
        prefix[number] = running_sum
    return prefix


def make_summatory_totient(prefix: array):
    """Build a cached summatory-totient function using quotient grouping."""

    @cache
    def summatory_totient(limit: int) -> int:
        if limit < len(prefix):
            return prefix[limit]

        result = limit * (limit + 1) // 2
        left = 2
        while left <= limit:
            quotient = limit // left
            right = limit // quotient
            result -= (right - left + 1) * summatory_totient(quotient)
            left = right + 1
        return result

    return summatory_totient


def gcd_sum(limit: int, summatory_totient) -> int:
    result = 0
    left = 1

    while left <= limit:
        quotient = limit // left
        right = limit // quotient
        nested_sum = nested_prefix_sum(right) - nested_prefix_sum(left - 1)
        coprime_pairs = 2 * summatory_totient(quotient) - 1
        result = (result + nested_sum * coprime_pairs) % MODULUS
        left = right + 1

    return result


def solve() -> int:
    totient_prefix = totient_prefix_table(TOTIENT_SIEVE_LIMIT)
    summatory_totient = make_summatory_totient(totient_prefix)

    assert gcd_sum(3, summatory_totient) == 12
    assert gcd_sum(4, summatory_totient) == 24_881_925
    assert gcd_sum(100, summatory_totient) == 14_416_749
    return gcd_sum(TARGET, summatory_totient)


if __name__ == "__main__":
    print(solve())
