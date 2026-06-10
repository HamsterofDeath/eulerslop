#!/usr/bin/env python3

def row_layouts(width):
    """All rows of 2s and 3s summing to width, as bitsets of internal crack positions."""
    results = []

    def rec(pos, mask):
        if pos == width:
            results.append(mask)
            return
        for brick in (2, 3):
            npos = pos + brick
            if npos < width:
                rec(npos, mask | (1 << npos))
            elif npos == width:
                results.append(mask)

    rec(0, 0)
    return results


def wall_count(width, height):
    rows = row_layouts(width)
    n = len(rows)
    compatible = [
        [j for j in range(n) if rows[i] & rows[j] == 0]
        for i in range(n)
    ]
    counts = [1] * n
    for _ in range(height - 1):
        counts = [sum(counts[j] for j in compatible[i]) for i in range(n)]
    return sum(counts)


def solve():
    assert wall_count(9, 3) == 8
    return wall_count(32, 10)


if __name__ == "__main__":
    print(solve())
