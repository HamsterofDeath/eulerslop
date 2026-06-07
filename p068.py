#!/usr/bin/env python3
from itertools import permutations

def solve():
    best = "0"
    # 10 must be on an outer node for 16 digits
    for perm in permutations(range(1, 11)):
        outer = [perm[i] for i in range(5)]
        inner = [perm[i] for i in range(5, 10)]
        # Total of each line
        s = outer[0] + inner[0] + inner[1]
        valid = True
        groups = []
        for i in range(5):
            a = outer[i]
            b = inner[i]
            c = inner[(i + 1) % 5]
            if a + b + c != s:
                valid = False
                break
            groups.append((a, b, c))
        if not valid:
            continue
        # 10 must be on outer
        if 10 not in outer:
            continue
        # Find smallest outer to start
        min_idx = min(range(5), key=lambda i: outer[i])
        # Rotate groups to start at min_idx
        rotated = groups[min_idx:] + groups[:min_idx]
        s = "".join(str(x) for g in rotated for x in g)
        if len(s) == 16 and s > best:
            best = s
    return int(best)

if __name__ == "__main__":
    print(solve())
