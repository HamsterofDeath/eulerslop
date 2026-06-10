#!/usr/bin/env python3
import urllib.request

def solve():
    url = "https://projecteuler.net/project/resources/p079_keylog.txt"
    with urllib.request.urlopen(url) as f:
        attempts = [line.strip() for line in f.read().decode("utf-8").strip().split("\n")]

    # Topological sort on digits that actually appear in the keylog
    # For each attempt "abc", we know a comes before b comes before c
    digits = set("".join(attempts))
    before = {d: set() for d in digits}
    after = {d: set() for d in digits}

    for a in attempts:
        for i in range(len(a)):
            for j in range(i + 1, len(a)):
                before[a[j]].add(a[i])
                after[a[i]].add(a[j])

    # Find the order
    result = []
    remaining = set(before.keys())
    while remaining:
        # Find digit with no prerequisites
        for d in sorted(remaining):
            if not before[d] & remaining:
                result.append(d)
                remaining.remove(d)
                break

    return "".join(result)

if __name__ == "__main__":
    print(solve())
