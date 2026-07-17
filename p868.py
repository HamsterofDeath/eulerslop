#!/usr/bin/env python3
"""Project Euler 868: rank a word in bell-ringing permutation order."""


TARGET = "NOWPICKBELFRYMATHS"


def ringing_rank(permutation: list[int]) -> int:
    """Return the zero-based Steinhaus-Johnson-Trotter rank."""
    rank = 0
    positions = [0] * (len(permutation) + 1)
    remaining = list(permutation)

    # Removing the largest item gives the preceding-order permutation.
    # Its rank q selects a block of n permutations.  In even blocks the
    # largest item moves right-to-left; in odd blocks it moves left-to-right.
    for largest in range(len(permutation), 1, -1):
        position = remaining.index(largest)
        positions[largest] = position
        remaining.pop(position)

    for largest in range(2, len(permutation) + 1):
        offset = (
            largest - 1 - positions[largest]
            if rank % 2 == 0
            else positions[largest]
        )
        rank = rank * largest + offset
    return rank


def word_rank(word: str) -> int:
    alphabet = {
        letter: index
        for index, letter in enumerate(sorted(word), 1)
    }
    return ringing_rank([alphabet[letter] for letter in word])


def solve() -> int:
    assert word_rank("CBA") == 3
    assert word_rank("BELFRY") == 59
    return word_rank(TARGET)


if __name__ == "__main__":
    print(solve())
