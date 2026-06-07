#!/usr/bin/env python3
from itertools import combinations

def solve():
    squares = [(0, 1), (0, 4), (0, 9), (1, 6), (2, 5), (3, 6), (4, 9), (6, 4), (8, 1)]
    digits = list(range(10))

    count = 0
    for c1 in combinations(digits, 6):
        set1 = set(c1)
        if 6 in set1 or 9 in set1:
            set1 = set1 | {6, 9}
        for c2 in combinations(digits, 6):
            set2 = set(c2)
            if 6 in set2 or 9 in set2:
                set2 = set2 | {6, 9}
            if all((a in set1 and b in set2) or (b in set1 and a in set2) for a, b in squares):
                count += 1
    return count // 2  # each pair counted twice (order)

if __name__ == "__main__":
    print(solve())
