#!/usr/bin/env python3
import urllib.request

def is_special(s):
    s = sorted(s)
    n = len(s)
    # Rule 2
    for k in range(1, n):
        if sum(s[:k+1]) <= sum(s[-(k):]):
            return False
    # Rule 1: all subset sums distinct
    sums = set()
    for mask in range(1, 1 << n):
        total = 0
        for i in range(n):
            if mask & (1 << i):
                total += s[i]
        if total in sums:
            return False
        sums.add(total)
    return True

def solve():
    url = "https://projecteuler.net/project/resources/p105_sets.txt"
    with urllib.request.urlopen(url) as f:
        data = f.read().decode("utf-8").strip().split("\n")
    total = 0
    for line in data:
        vals = list(map(int, line.split(",")))
        if is_special(vals):
            total += sum(vals)
    return total

if __name__ == "__main__":
    print(solve())
