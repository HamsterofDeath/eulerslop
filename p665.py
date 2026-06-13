#!/usr/bin/env python3
"""Project Euler 665: Proportionate Nim."""


class OccupiedSet:
    """Dynamic set that can jump from an occupied integer to the next gap."""

    __slots__ = ("parent",)

    def __init__(self):
        self.parent = {}

    def find(self, x):
        parent = self.parent
        y = parent.get(x)
        if y is None:
            return x

        path = []
        while y is not None:
            path.append(x)
            x = y
            y = parent.get(x)

        for value in path:
            parent[value] = x
        return x

    def add(self, x):
        parent = self.parent
        if x not in parent:
            parent[x] = self.find(x + 1)


def losing_sum(limit):
    max_first = limit // 2

    used_coordinates = OccupiedSet()
    differences = OccupiedSet()
    twice_slope_keys = OccupiedSet()
    half_slope_keys = [OccupiedSet(), OccupiedSet()]

    # The terminal position (0, 0) attacks (a, 2a).
    used_coordinates.add(0)
    twice_slope_keys.add(0)
    half_slope_keys[0].add(0)

    # Cross-orientation attacks from (c, d) only become possible once a > d.
    cross_key_at_upper = [None] * (max_first + 1)
    next_cross = 1

    def activate_cross_attacks(a):
        nonlocal next_cross
        stop = min(a, max_first + 1)
        while next_cross < stop:
            key = cross_key_at_upper[next_cross]
            if key is not None:
                twice_slope_keys.add(key)
            next_cross += 1

    total = 0
    a = 1

    while True:
        next_a = used_coordinates.find(a)
        while next_a != a:
            a = next_a
            activate_cross_attacks(a)
            next_a = used_coordinates.find(a)

        if a > max_first:
            break
        activate_cross_attacks(a)

        b = a + 1
        while True:
            old_b = b

            next_b = used_coordinates.find(b)
            if next_b > b:
                b = next_b

            next_key = differences.find(b - a)
            if next_key > b - a:
                b = a + next_key

            next_key = twice_slope_keys.find(b - 2 * a)
            if next_key > b - 2 * a:
                b = max(b, 2 * a + next_key)

            key = 2 * b - a
            parity = key & 1
            half_key = (key - parity) // 2
            next_key = half_slope_keys[parity].find(half_key)
            if next_key > half_key:
                b = max(b, b + next_key - half_key)

            if b == old_b:
                break

        if a + b <= limit:
            total += a + b

        used_coordinates.add(a)
        used_coordinates.add(b)
        differences.add(b - a)
        twice_slope_keys.add(b - 2 * a)

        key = 2 * b - a
        parity = key & 1
        half_slope_keys[parity].add((key - parity) // 2)

        if b <= max_first:
            cross_key_at_upper[b] = a - 2 * b

    return total


def solve():
    return losing_sum(10_000_000)


if __name__ == "__main__":
    print(solve())
