#!/usr/bin/env python3
"""Project Euler Problem 954: Heptaphobia.

For a number with residue r modulo 7, swapping positions i and j changes
the residue by

    (digit_j - digit_i) * (weight_i - weight_j).

Each swap therefore forbids one of only seven possible values of r.
Decimal place weights have period six modulo 7, and swaps between equal
weights change nothing.  The dynamic program groups positions by weight
and carries a seven-bit forbidden digit mask for every unprocessed group.
"""

from collections import defaultdict
from functools import lru_cache
from itertools import product


INVERSE_MODULO_SEVEN = (0, 1, 4, 5, 2, 3, 6)


def shifted_mask(mask: int, shift: int) -> int:
    result = 0
    for residue in range(7):
        if mask & (1 << residue):
            result |= 1 << ((residue + shift) % 7)
    return result


SHIFTED_MASKS = tuple(
    tuple(shifted_mask(mask, shift) for mask in range(128))
    for shift in range(7)
)


@lru_cache(maxsize=None)
def group_options(
    position_count: int,
    allowed_digits: tuple[int, ...],
) -> tuple[tuple[int, int, int], ...]:
    """Return (residue mask, digit sum, multiplicity) summaries."""
    summaries: dict[tuple[int, int], int] = defaultdict(int)
    for digits in product(allowed_digits, repeat=position_count):
        mask = 0
        digit_sum = 0
        for digit in digits:
            residue = digit % 7
            mask |= 1 << residue
            digit_sum += residue
        summaries[(mask, digit_sum % 7)] += 1

    return tuple(
        (mask, digit_sum, multiplicity)
        for (mask, digit_sum), multiplicity in summaries.items()
    )


def count_with_residue(
    length: int,
    target_residue: int,
    leading_digit: int,
) -> int:
    weights = [
        pow(10, length - 1 - index, 7)
        for index in range(length)
    ]
    leading_weight = weights[0]

    position_counts = [0] * 7
    for weight in weights[1:]:
        position_counts[weight] += 1

    groups = []
    for weight in range(1, 7):
        if position_counts[weight] == 0:
            continue

        allowed = tuple(
            digit
            for digit in range(10)
            if (
                weight == leading_weight
                or digit == 0
                or (
                    target_residue
                    + (digit - leading_digit)
                    * (leading_weight - weight)
                )
                % 7
                != 0
            )
        )
        options = group_options(position_counts[weight], allowed)
        groups.append((weight, options))

    # Small option sets impose the strongest constraints first.
    groups.sort(key=lambda group: len(group[1]))

    # State: (packed forbidden masks, current residue) -> count.
    states = {(0, leading_digit * leading_weight % 7): 1}

    for group_index, (weight, options) in enumerate(groups):
        next_states: dict[tuple[int, int], int] = defaultdict(int)
        offset = 7 * (weight - 1)
        forbidden_bits = 127 << offset
        future_weights = [
            future_weight
            for future_weight, _ in groups[group_index + 1 :]
        ]

        for (packed, residue), count in states.items():
            forbidden = (packed >> offset) & 127
            cleared = packed & ~forbidden_bits

            for mask, digit_sum, multiplicity in options:
                if mask & forbidden:
                    continue

                updated = cleared
                for future_weight in future_weights:
                    difference = (future_weight - weight) % 7
                    shift = (
                        target_residue
                        * INVERSE_MODULO_SEVEN[difference]
                        % 7
                    )
                    updated |= (
                        SHIFTED_MASKS[shift][mask]
                        << (7 * (future_weight - 1))
                    )

                key = (
                    updated,
                    (residue + weight * digit_sum) % 7,
                )
                next_states[key] += count * multiplicity

        states = next_states

    return sum(
        count
        for (_, residue), count in states.items()
        if residue == target_residue
    )


def count_length(length: int) -> int:
    return sum(
        count_with_residue(length, residue, leading_digit)
        for residue in range(1, 7)
        for leading_digit in range(1, 10)
    )


def count_heptaphobic(maximum_digits: int) -> int:
    return sum(
        count_length(length)
        for length in range(1, maximum_digits + 1)
    )


def solve() -> int:
    assert count_heptaphobic(2) == 74
    assert count_heptaphobic(4) == 3737
    return count_heptaphobic(13)


if __name__ == "__main__":
    print(solve())
