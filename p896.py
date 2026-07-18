#!/usr/bin/env python3
"""Project Euler Problem 896: Divisible Ranges.

For a range [a, a+L-1], assigning offset j to position i requires

    a + j == 0 (mod i).

Thus a valid permutation is a choice of distinct offsets whose
congruences for a are mutually consistent.  Divisibility depends only
on a modulo lcm(1,...,L), so a memoized backtracking search enumerates
all valid residues in one period.  At each state, the position with the
fewest currently compatible offsets is assigned first, and generalized
CRT merges its congruence into the state.
"""

from math import gcd


TARGET_LENGTH = 36
TARGET_INDEX = 36


def merge_congruences(
    first_residue: int,
    first_modulus: int,
    second_residue: int,
    second_modulus: int,
) -> tuple[int, int] | None:
    """Merge two congruences, allowing non-coprime moduli."""
    common = gcd(first_modulus, second_modulus)
    difference = second_residue - first_residue
    if difference % common:
        return None

    reduced_second = second_modulus // common
    if reduced_second == 1:
        multiplier = 0
    else:
        inverse = pow(
            first_modulus // common, -1, reduced_second
        )
        multiplier = (
            difference // common * inverse
        ) % reduced_second

    modulus = first_modulus * reduced_second
    residue = (
        first_residue + first_modulus * multiplier
    ) % modulus
    return residue, modulus


def lcm_through(limit: int) -> int:
    result = 1
    for value in range(2, limit + 1):
        result = result // gcd(result, value) * value
    return result


def compatible_offsets(
    length: int,
    unused_offsets: int,
    target: int,
    step: int,
) -> list[int]:
    result = []
    for offset in range(target, length, step):
        if unused_offsets & (1 << offset):
            result.append(offset)
    return result


def most_constrained_position(
    length: int,
    residue: int,
    modulus: int,
    unused_offsets: int,
    remaining_positions: int,
) -> tuple[int, list[int]] | None:
    """Choose a position by minimum remaining values."""
    best_position = 0
    best_offsets: list[int] | None = None

    # Descending order breaks equal-size ties toward larger moduli.
    for position in range(length, 0, -1):
        if not remaining_positions & (1 << (position - 1)):
            continue
        common = gcd(modulus, position)
        offsets = compatible_offsets(
            length,
            unused_offsets,
            (-residue) % common,
            common,
        )
        if not offsets:
            return None
        if best_offsets is None or len(offsets) < len(best_offsets):
            best_position = position
            best_offsets = offsets

    if best_offsets is None:
        return None
    return best_position, best_offsets


def valid_residues(length: int) -> tuple[set[int], int]:
    """Enumerate valid positive-start residues over one full period."""
    period = lcm_through(length)
    all_bits = (1 << length) - 1
    residues: set[int] = set()
    visited: set[tuple[int, int, int, int]] = set()

    def search(
        residue: int,
        modulus: int,
        unused_offsets: int,
        remaining_positions: int,
    ) -> None:
        residue %= modulus
        state = (
            residue,
            modulus,
            unused_offsets,
            remaining_positions,
        )
        if state in visited:
            return
        visited.add(state)

        if remaining_positions == 0:
            residues.add(residue)
            return

        choice = most_constrained_position(
            length,
            residue,
            modulus,
            unused_offsets,
            remaining_positions,
        )
        if choice is None:
            return
        position, offsets = choice
        next_positions = remaining_positions & ~(
            1 << (position - 1)
        )

        for offset in offsets:
            merged = merge_congruences(
                residue,
                modulus,
                (-offset) % position,
                position,
            )
            if merged is None:
                continue
            next_residue, next_modulus = merged
            search(
                next_residue,
                next_modulus,
                unused_offsets & ~(1 << offset),
                next_positions,
            )

    search(0, 1, all_bits, all_bits)
    return residues, period


def ordered_starts(length: int) -> list[int]:
    residues, period = valid_residues(length)
    return sorted(
        residue if residue else period
        for residue in residues
    )


def nth_divisible_range(length: int, index: int) -> int:
    starts = ordered_starts(length)
    if not 1 <= index <= len(starts):
        raise ValueError("requested range lies outside one period")
    return starts[index - 1]


def has_divisible_permutation(start: int, length: int) -> bool:
    """Independently verify one range by bipartite matching."""
    edges = [
        [],
        *[
            [
                offset
                for offset in range(length)
                if (start + offset) % position == 0
            ]
            for position in range(1, length + 1)
        ],
    ]
    matched_position = [-1] * length

    def augment(position: int, seen_offsets: list[bool]) -> bool:
        for offset in edges[position]:
            if seen_offsets[offset]:
                continue
            seen_offsets[offset] = True
            previous = matched_position[offset]
            if previous == -1 or augment(previous, seen_offsets):
                matched_position[offset] = position
                return True
        return False

    for position in range(length, 0, -1):
        if not augment(position, [False] * length):
            return False
    return True


def solve() -> int:
    assert ordered_starts(4)[:4] == [1, 2, 3, 6]
    assert has_divisible_permutation(6, 4)
    answer = nth_divisible_range(TARGET_LENGTH, TARGET_INDEX)
    assert has_divisible_permutation(answer, TARGET_LENGTH)
    return answer


if __name__ == "__main__":
    print(solve())
