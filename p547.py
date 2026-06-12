#!/usr/bin/env python3

import math

import numpy as np


def unit_square_distances(max_delta, order=30):
    nodes, weights = np.polynomial.legendre.leggauss(order)
    pieces = []
    piece_weights = []
    for left, right in [(-1.0, 0.0), (0.0, 1.0)]:
        midpoint = (left + right) / 2
        half_width = (right - left) / 2
        shifted = midpoint + half_width * nodes
        pieces.append(shifted)
        piece_weights.append(half_width * weights * (1 - np.abs(shifted)))

    offsets = np.concatenate(pieces)
    offset_weights = np.concatenate(piece_weights)
    distances = {}
    weight_grid = offset_weights[:, None] * offset_weights[None, :]

    for dx in range(-max_delta, max_delta + 1):
        x_values = dx + offsets[:, None]
        for dy in range(-max_delta, max_delta + 1):
            y_values = dy + offsets[None, :]
            distances[(dx, dy)] = float(np.sum(weight_grid * np.hypot(x_values, y_values)))
    return distances


def hollow_lamina_sum(size):
    distances = unit_square_distances(size - 1)

    full_full = 0.0
    for dx in range(-(size - 1), size):
        for dy in range(-(size - 1), size):
            full_full += (
                (size - abs(dx))
                * (size - abs(dy))
                * distances[(dx, dy)]
            )

    full_to_cell = [[0.0] * size for _ in range(size)]
    for bx in range(size):
        for by in range(size):
            total = 0.0
            for ax in range(size):
                for ay in range(size):
                    total += distances[(bx - ax, by - ay)]
            full_to_cell[bx][by] = total

    prefix = [[0.0] * (size + 1) for _ in range(size + 1)]
    for x in range(size):
        for y in range(size):
            prefix[x + 1][y + 1] = (
                prefix[x][y + 1]
                + prefix[x + 1][y]
                - prefix[x][y]
                + full_to_cell[x][y]
            )

    hole_hole = {}
    for width in range(1, size - 1):
        for height in range(1, size - 1):
            total = 0.0
            for dx in range(-(width - 1), width):
                x_count = width - abs(dx)
                for dy in range(-(height - 1), height):
                    total += x_count * (height - abs(dy)) * distances[(dx, dy)]
            hole_hole[(width, height)] = total

    result = 0.0
    for width in range(1, size - 1):
        for height in range(1, size - 1):
            area = size * size - width * height
            hole_pair_sum = hole_hole[(width, height)]
            for x in range(1, size - width):
                for y in range(1, size - height):
                    full_hole = (
                        prefix[x + width][y + height]
                        - prefix[x][y + height]
                        - prefix[x + width][y]
                        + prefix[x][y]
                    )
                    result += (full_full - 2 * full_hole + hole_pair_sum) / (area * area)
    return result


def solve():
    assert round(hollow_lamina_sum(3), 4) == 1.6514
    assert round(hollow_lamina_sum(4), 4) == 19.6564
    return f"{hollow_lamina_sum(40):.4f}"


if __name__ == "__main__":
    print(solve())
