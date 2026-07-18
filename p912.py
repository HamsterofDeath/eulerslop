"""Project Euler Problem 912: Binary Constraints.

Valid binary strings are ordered first by length and then lexicographically.
For each suffix block, keep the number of strings and the first two moments
of the local ranks of strings ending in 1.  Concatenating the 0- and 1-blocks
then only requires shifting the ranks in the second block.
"""

from functools import cache


MODULUS = 1_000_000_007
TARGET = 10**16


@cache
def block_statistics(remaining: int, trailing_ones: int) -> tuple[int, int, int, int]:
    """Return (size, selected count, rank sum, squared-rank sum)."""
    if remaining == 0:
        selected = int(trailing_ones > 0)
        return 1, selected, selected, selected

    zero_block = block_statistics(remaining - 1, 0)
    one_block = (
        block_statistics(remaining - 1, trailing_ones + 1)
        if trailing_ones < 2
        else (0, 0, 0, 0)
    )
    return concatenate(zero_block, one_block)


def concatenate(
    first: tuple[int, int, int, int],
    second: tuple[int, int, int, int],
) -> tuple[int, int, int, int]:
    """Concatenate two rank blocks, shifting the ranks of the second."""
    size_0, count_0, sum_0, square_sum_0 = first
    size_1, count_1, sum_1, square_sum_1 = second
    shift = size_0 % MODULUS

    return (
        size_0 + size_1,
        count_0 + count_1,
        (sum_0 + sum_1 + shift * (count_1 % MODULUS)) % MODULUS,
        (
            square_sum_0
            + square_sum_1
            + 2 * shift * sum_1
            + shift * shift * (count_1 % MODULUS)
        )
        % MODULUS,
    )


def prefix_statistics(
    remaining: int,
    trailing_ones: int,
    length: int,
) -> tuple[int, int, int, int]:
    """Return statistics for the first ``length`` strings in a suffix block."""
    if length == 0:
        return 0, 0, 0, 0

    whole_block = block_statistics(remaining, trailing_ones)
    if length == whole_block[0]:
        return whole_block

    zero_block = block_statistics(remaining - 1, 0)
    if length <= zero_block[0]:
        return prefix_statistics(remaining - 1, 0, length)

    one_prefix = prefix_statistics(
        remaining - 1,
        trailing_ones + 1,
        length - zero_block[0],
    )
    return concatenate(zero_block, one_prefix)


def odd_index_square_sum(limit: int) -> int:
    """Return F(limit) modulo MODULUS."""
    answer = 0
    global_offset = 0
    bit_length = 1
    remaining = limit

    while remaining:
        block = block_statistics(bit_length - 1, 1)
        take = min(remaining, block[0])
        prefix = (
            block
            if take == block[0]
            else prefix_statistics(bit_length - 1, 1, take)
        )
        _, count, rank_sum, square_sum = prefix
        offset = global_offset % MODULUS
        answer += square_sum + 2 * offset * rank_sum + offset * offset * count
        answer %= MODULUS

        global_offset += take
        remaining -= take
        bit_length += 1

    return answer


def solve() -> int:
    assert odd_index_square_sum(10) == 199
    return odd_index_square_sum(TARGET)


if __name__ == "__main__":
    print(solve())
