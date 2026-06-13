#!/usr/bin/env python3
"""Project Euler 666: Polymorphic Bacteria."""


def action_rows(k, m):
    rows = []
    r = 306

    for i in range(k):
        row = []
        for _ in range(m):
            q = r % 5
            if q == 0:
                row.append((0, 0))
            elif q == 1:
                row.append((1, i))
            elif q == 2:
                row.append((2, (2 * i) % k))
            elif q == 3:
                row.append((3, (i * i + 1) % k))
            else:
                row.append((4, (i + 1) % k))
            r = (r * r) % 10_007
        rows.append(row)

    return rows


def extinction_probability(k, m, tolerance=1e-14):
    rows = action_rows(k, m)
    probability = [0.0] * k
    next_probability = [0.0] * k
    scale = 1.0 / m

    while True:
        max_delta = 0.0
        for i, row in enumerate(rows):
            current = probability[i]
            total = 0.0

            for kind, target in row:
                if kind == 0:
                    total += 1.0
                elif kind == 1:
                    total += current * current
                elif kind == 2:
                    total += probability[target]
                elif kind == 3:
                    child = probability[target]
                    total += child * child * child
                else:
                    total += current * probability[target]

            value = total * scale
            next_probability[i] = value
            delta = abs(value - current)
            if delta > max_delta:
                max_delta = delta

        probability, next_probability = next_probability, probability
        if max_delta < tolerance:
            return probability[0]


def solve():
    return f"{extinction_probability(500, 10):.8f}"


if __name__ == "__main__":
    print(solve())
