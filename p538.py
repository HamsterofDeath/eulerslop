#!/usr/bin/env python3
from collections import defaultdict


LIMIT = 3_000_000


POW3 = [1]
for _ in range(40):
    POW3.append(POW3[-1] * 3)


def u(n):
    return (1 << ((3 * n).bit_count())) + POW3[(2 * n).bit_count()] + (
        n + 1
    ).bit_count()


def area_key(sides):
    perimeter = sum(sides)
    if 2 * max(sides) >= perimeter:
        return None

    quadruple_area_squared = 1
    for side in sides:
        quadruple_area_squared *= perimeter - 2 * side
    return quadruple_area_squared, perimeter


def best_perimeter(counts):
    values = sorted((value for value, count in counts.items() if count), reverse=True)
    best_area = -1
    best = 0

    for index, largest in enumerate(values):
        sides = [largest]

        copies = min(counts[largest] - 1, 3)
        while copies and len(sides) < 4:
            sides.append(largest)
            copies -= 1

        next_index = index + 1
        while len(sides) < 4 and next_index < len(values):
            value = values[next_index]
            copies = min(counts[value], 4)
            while copies and len(sides) < 4:
                sides.append(value)
                copies -= 1
            next_index += 1

        if len(sides) < 4:
            continue

        key = area_key(sides)
        if key is not None and (key[0] > best_area or (key[0] == best_area and key[1] > best)):
            best_area, best = key

    return best


def solve(limit=LIMIT):
    counts = defaultdict(int)
    total = 0
    current = 0
    last_change = 4

    for n in range(1, limit + 1):
        value = u(n)
        before = min(counts[value], 4)
        counts[value] += 1
        after = min(counts[value], 4)

        if n >= 4 and after != before:
            total += current * (n - last_change)
            current = best_perimeter(counts)
            last_change = n

    if last_change <= limit:
        total += current * (limit + 1 - last_change)
    return total


def _check_samples():
    counts = defaultdict(int)
    subtotal = 0
    samples = {}
    for n in range(1, 151):
        counts[u(n)] += 1
        if n >= 4:
            value = best_perimeter(counts)
            subtotal += value
            if n in (5, 10, 150):
                samples[n] = value

    assert samples[5] == 59
    assert samples[10] == 118
    assert samples[150] == 3223
    assert subtotal == 234761


if __name__ == "__main__":
    _check_samples()
    print(solve())
