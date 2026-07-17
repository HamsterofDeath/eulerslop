#!/usr/bin/env python3
"""Project Euler 872: path sums in the recursively rebuilt tree."""


TREE_SIZE = 10**17
TARGET_NODE = 9**17


def path_sum(tree_size: int, node: int) -> int:
    """Return the sum from node to the root in T_tree_size."""
    result = 0
    while True:
        result += node
        difference = tree_size - node
        if difference == 0:
            return result

        # In T_n the parent of k is k plus the highest power of two not
        # exceeding n-k.  Moving to the parent therefore clears the highest
        # set bit of the remaining difference.
        node += 1 << (difference.bit_length() - 1)


def solve() -> int:
    assert path_sum(6, 1) == 12
    assert path_sum(10, 3) == 29
    return path_sum(TREE_SIZE, TARGET_NODE)


if __name__ == "__main__":
    print(solve())
