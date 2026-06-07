#!/usr/bin/env python3

def solve():
    # Group cube numbers by sorted digits
    groups = {}
    n = 1
    while True:
        c = n ** 3
        key = "".join(sorted(str(c)))
        groups.setdefault(key, []).append(c)
        if len(groups[key]) == 5:
            return groups[key][0]
        n += 1

if __name__ == "__main__":
    print(solve())
