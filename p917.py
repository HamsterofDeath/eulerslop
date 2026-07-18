"""Project Euler Problem 917: A Separable Matrix Path.

For a path through M[i,j] = a[i] + b[j], consider the two fixed chains of
down-transition weights da[i] = a[i+1]-a[i] and right-transition weights
db[j] = b[j+1]-b[j]. Swapping adjacent unlike transitions changes the path
cost by their weight difference. Thus minimizing the path is equivalent to
maximizing sum(position * transition_weight) while preserving each chain.

Pool-adjacent-violators reduces each chain to blocks of nondecreasing average
weight. Merging the two block streams by average is the optimal interleaving.
Each block stores enough information to recover its exact weighted-position
sum, and only a handful of blocks survive for the generated sequences.
"""


MODULUS = 998_388_889
SEED = 102_022_661
TARGET = 10**7

# A block is (sum of weights, number of weights, internal weighted-position
# sum), with internal positions numbered from one.
Block = tuple[int, int, int]


def append_pooled_block(stack: list[Block], weight: int) -> None:
    stack.append((weight, 1, weight))

    while len(stack) >= 2:
        sum_0, count_0, positions_0 = stack[-2]
        sum_1, count_1, positions_1 = stack[-1]
        if sum_0 * count_1 <= sum_1 * count_0:
            break

        stack.pop()
        stack[-1] = (
            sum_0 + sum_1,
            count_0 + count_1,
            positions_0 + count_0 * sum_1 + positions_1,
        )


def optimal_transition_value(
    down_blocks: list[Block],
    right_blocks: list[Block],
) -> int:
    """Return the maximum sum(position * transition weight)."""
    down_index = 0
    right_index = 0
    position_offset = 0
    result = 0

    while down_index < len(down_blocks) or right_index < len(right_blocks):
        if right_index == len(right_blocks) or (
            down_index < len(down_blocks)
            and down_blocks[down_index][0] * right_blocks[right_index][1]
            <= right_blocks[right_index][0] * down_blocks[down_index][1]
        ):
            weight_sum, count, internal_value = down_blocks[down_index]
            down_index += 1
        else:
            weight_sum, count, internal_value = right_blocks[right_index]
            right_index += 1

        result += internal_value + position_offset * weight_sum
        position_offset += count

    return result


def minimal_path_sum(size: int) -> int:
    first_a = SEED
    first_b = first_a * first_a % MODULUS
    if size == 1:
        return first_a + first_b

    down_blocks: list[Block] = []
    right_blocks: list[Block] = []
    a = first_a
    b = first_b

    for _ in range(1, size):
        next_a = b * b % MODULUS
        next_b = next_a * next_a % MODULUS
        append_pooled_block(down_blocks, next_a - a)
        append_pooled_block(right_blocks, next_b - b)
        a, b = next_a, next_b

    transition_value = optimal_transition_value(down_blocks, right_blocks)

    # Path cost plus its transition value is invariant under adjacent swaps.
    # Evaluating the invariant on the all-down-then-all-right path telescopes.
    return (2 * size - 1) * (a + b) - transition_value


def solve() -> int:
    assert minimal_path_sum(1) == 966_774_091
    assert minimal_path_sum(2) == 2_388_327_490
    assert minimal_path_sum(10) == 13_389_278_727
    return minimal_path_sum(TARGET)


if __name__ == "__main__":
    print(solve())
