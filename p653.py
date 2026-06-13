#!/usr/bin/env python3

MODULUS = 32_745_673
FIRST_RANDOM = 6_563_116
MARBLE_DIAMETER = 20
WEST_CENTER = 10
EAST_THRESHOLD = 10_000_000


def d(length, count, label):
    """Distance traveled by the original `label`th marble."""
    r = FIRST_RANDOM
    compressed_position = WEST_CENTER
    offsets = []

    for _ in range(count):
        compressed_position += r % 1000 + 1
        if r <= EAST_THRESHOLD:
            offsets.append(-compressed_position)
        else:
            offsets.append(compressed_position - MARBLE_DIAMETER)
        r = (r * r) % MODULUS

    # Removing the rod diameters turns collisions into point particles passing
    # through each other.  The east boundary advances one diameter after every
    # exit, while each particle's contribution to its exit time is fixed.
    exit_rank = count - label + 1
    east_boundary = length - MARBLE_DIAMETER * (label - 1)
    offsets.sort()
    return east_boundary + offsets[exit_rank - 1]


def solve():
    return d(1_000_000_000, 1_000_001, 500_001)


if __name__ == "__main__":
    print(solve())
