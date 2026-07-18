"""Project Euler Problem 924: Next Digit Permutations.

B(x)-x depends only on the shortest decimal suffix containing an ascent.
For a_n modulo 10^11, the recurrence enters a cycle of length 15,625,000;
every residue in that cycle has an ascent within its last eleven digits.

A table handles suffixes with an ascent in their final six digits. Only 3,125
cycle entries require the eleven-digit fallback. Separately, a_n modulo
1e9+7 has preperiod 39,911 and period 21,353, so its contribution can be
summed directly. The first five (short) terms are evaluated exactly.
"""

from array import array


MODULUS = 1_000_000_007
TARGET = 10**16
DECIMAL_DIGITS = 11
DECIMAL_MODULUS = 10**DECIMAL_DIGITS
DECIMAL_PERIOD = 15_625_000
LOOKUP_DIGITS = 6
LOOKUP_MODULUS = 10**LOOKUP_DIGITS
NO_ASCENT = 2_147_483_647


def next_permutation_adjustment(value: int, width: int) -> int | None:
    """Return next_permutation(value)-value within a zero-padded width."""
    digits = [0] * width
    remaining = value
    for index in range(width - 1, -1, -1):
        digits[index] = remaining % 10
        remaining //= 10

    pivot = width - 2
    while pivot >= 0 and digits[pivot] >= digits[pivot + 1]:
        pivot -= 1
    if pivot < 0:
        return None

    successor = width - 1
    while digits[successor] <= digits[pivot]:
        successor -= 1
    digits[pivot], digits[successor] = digits[successor], digits[pivot]
    digits[pivot + 1 :] = reversed(digits[pivot + 1 :])

    permutation = 0
    for digit in digits:
        permutation = 10 * permutation + digit
    return permutation - value


def exact_next_permutation(value: int) -> int:
    digits = list(str(value))
    pivot = len(digits) - 2
    while pivot >= 0 and digits[pivot] >= digits[pivot + 1]:
        pivot -= 1
    if pivot < 0:
        return 0

    successor = len(digits) - 1
    while digits[successor] <= digits[pivot]:
        successor -= 1
    digits[pivot], digits[successor] = digits[successor], digits[pivot]
    digits[pivot + 1 :] = reversed(digits[pivot + 1 :])
    return int("".join(digits))


def adjustment_lookup() -> array:
    lookup = array("i", [NO_ASCENT]) * LOOKUP_MODULUS
    for suffix in range(LOOKUP_MODULUS):
        adjustment = next_permutation_adjustment(suffix, LOOKUP_DIGITS)
        if adjustment is not None:
            lookup[suffix] = adjustment
    return lookup


def decimal_adjustment_sum(first_index: int, last_index: int) -> int:
    """Sum B(a_n)-a_n over a cyclic range beginning at first_index."""
    assert first_index == 6
    count = last_index - first_index + 1
    complete_cycles, remainder = divmod(count, DECIMAL_PERIOD)
    lookup = adjustment_lookup()

    value = 0
    for _ in range(first_index):
        value = (value * value + 2) % DECIMAL_MODULUS
    cycle_start = value

    cycle_sum = 0
    remainder_sum = 0
    for offset in range(DECIMAL_PERIOD):
        adjustment = lookup[value % LOOKUP_MODULUS]
        if adjustment == NO_ASCENT:
            adjustment = next_permutation_adjustment(
                value,
                DECIMAL_DIGITS,
            )
            # This assertion exhaustively establishes that eleven digits are
            # sufficient throughout the complete decimal cycle.
            assert adjustment is not None

        cycle_sum = (cycle_sum + adjustment) % MODULUS
        if offset < remainder:
            remainder_sum = (remainder_sum + adjustment) % MODULUS
        value = (value * value + 2) % DECIMAL_MODULUS

    assert value == cycle_start
    return (complete_cycles * cycle_sum + remainder_sum) % MODULUS


def recurrence_prefix_sum(limit: int) -> int:
    """Return sum(a_n, 0 <= n <= limit) modulo MODULUS."""
    values = []
    first_index: dict[int, int] = {}
    value = 0

    while value not in first_index:
        first_index[value] = len(values)
        values.append(value)
        value = (value * value + 2) % MODULUS

    cycle_start = first_index[value]
    period = len(values) - cycle_start
    prefix = [0]
    for entry in values:
        prefix.append((prefix[-1] + entry) % MODULUS)

    count = limit + 1
    if count <= len(values):
        return prefix[count]

    complete_cycles, remainder = divmod(count - cycle_start, period)
    cycle_sum = prefix[-1] - prefix[cycle_start]
    return (
        prefix[cycle_start]
        + complete_cycles * cycle_sum
        + prefix[cycle_start + remainder]
        - prefix[cycle_start]
    ) % MODULUS


def early_permutation_sum(last_index: int) -> int:
    value = 0
    result = 0
    for _ in range(1, last_index + 1):
        value = value * value + 2
        result = (result + exact_next_permutation(value)) % MODULUS
    return result


def permutation_sum(limit: int) -> int:
    if limit <= 10:
        return early_permutation_sum(limit)

    early_end = min(limit, 5)
    result = early_permutation_sum(early_end)
    if limit <= early_end:
        return result

    recurrence_sum = (
        recurrence_prefix_sum(limit) - recurrence_prefix_sum(early_end)
    )
    adjustment_sum = decimal_adjustment_sum(early_end + 1, limit)
    return (result + recurrence_sum + adjustment_sum) % MODULUS


def solve() -> int:
    assert permutation_sum(10) == 543_870_437
    return permutation_sum(TARGET)


if __name__ == "__main__":
    print(solve())
