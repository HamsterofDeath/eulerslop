#!/usr/bin/env python3
import urllib.request

def solve():
    url = "https://projecteuler.net/project/resources/p022_names.txt"
    with urllib.request.urlopen(url) as f:
        data = f.read().decode("utf-8")
    names = sorted(name.strip('"') for name in data.split(","))
    return sum((i + 1) * sum(ord(c) - 64 for c in name) for i, name in enumerate(names))

if __name__ == "__main__":
    print(solve())
