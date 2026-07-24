#!/usr/bin/env python3
"""Project Euler Problem 983: Consonant Circle Crossing.

Choose d non-opposite lattice vectors v_i of squared length m.  Embed a
d-dimensional hypercube by mapping each subset A to sum(v_i for i in A).
Use the even subsets as circle centres and the odd subsets as harmony
points.  Toggling one vector moves between a centre and a point by
exactly the radius, so the construction has 2**(d-1) of each.

The embedding must be injective within each bipartition and must not
create harmony points outside the odd subset sums.  We test those
conditions exactly.  A four-vector difference test cheaply prunes a
partial choice as soon as two non-neighbouring centres would harmonise.
"""

from itertools import combinations, product
from math import isqrt


TARGET = 500

Point = tuple[int, int]


def add(first: Point, second: Point) -> Point:
    return first[0] + second[0], first[1] + second[1]


def lattice_vectors(squared_radius: int) -> list[Point]:
    vectors: set[Point] = set()
    for x_coordinate in range(
        -isqrt(squared_radius), isqrt(squared_radius) + 1
    ):
        y_squared = squared_radius - x_coordinate * x_coordinate
        y_coordinate = isqrt(y_squared)
        if y_coordinate * y_coordinate == y_squared:
            vectors.add((x_coordinate, y_coordinate))
            vectors.add((x_coordinate, -y_coordinate))
    return sorted(vectors)


def opposite_pair_representatives(vectors: list[Point]) -> list[Point]:
    return [
        vector
        for vector in vectors
        if vector > (-vector[0], -vector[1])
    ]


def has_four_vector_conflict(
    selected: list[Point], circle_differences: set[Point]
) -> bool:
    if len(selected) < 4:
        return False

    newest = selected[-1]
    for triple in combinations(selected[:-1], 3):
        for signs in product((-1, 1), repeat=3):
            difference = newest
            for sign, vector in zip(signs, triple):
                difference = (
                    difference[0] + sign * vector[0],
                    difference[1] + sign * vector[1],
                )
            if difference != (0, 0) and difference in circle_differences:
                return True
    return False


def valid_hypercube(
    generators: list[Point], circle_vectors: list[Point]
) -> bool:
    even_sums = {(0, 0)}
    odd_sums: set[Point] = set()

    for generator in generators:
        next_even = even_sums | {
            add(point, generator) for point in odd_sums
        }
        next_odd = odd_sums | {
            add(point, generator) for point in even_sums
        }
        even_sums, odd_sums = next_even, next_odd

    expected_size = 1 << (len(generators) - 1)
    if len(even_sums) != expected_size or len(odd_sums) != expected_size:
        return False

    non_harmony_points: set[Point] = set()
    for center in even_sums:
        for radius_vector in circle_vectors:
            point = add(center, radius_vector)
            if point in odd_sums:
                continue
            if point in non_harmony_points:
                return False
            non_harmony_points.add(point)
    return True


def supports_hypercube(squared_radius: int, dimension: int) -> bool:
    vectors = lattice_vectors(squared_radius)
    representatives = opposite_pair_representatives(vectors)
    if len(representatives) < dimension:
        return False

    differences = {
        (first[0] - second[0], first[1] - second[1])
        for first in vectors
        for second in vectors
        if first != second
    }

    def search(start: int, selected: list[Point]) -> bool:
        if len(selected) == dimension:
            return valid_hypercube(selected, vectors)

        remaining = dimension - len(selected)
        final_start = len(representatives) - remaining
        for index in range(start, final_start + 1):
            selected.append(representatives[index])
            if (
                not has_four_vector_conflict(selected, differences)
                and search(index + 1, selected)
            ):
                return True
            selected.pop()
        return False

    return search(0, [])


def minimum_squared_radius(target: int) -> int:
    dimension = (target - 1).bit_length() + 1
    squared_radius = 1
    while not supports_hypercube(squared_radius, dimension):
        squared_radius += 1
    return squared_radius


def solve() -> int:
    assert minimum_squared_radius(2) == 1
    assert minimum_squared_radius(4) == 5
    return minimum_squared_radius(TARGET)


if __name__ == "__main__":
    print(solve())
