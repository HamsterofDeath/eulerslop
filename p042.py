#!/usr/bin/env python3
import urllib.request

def solve():
    url = "https://projecteuler.net/project/resources/p042_words.txt"
    with urllib.request.urlopen(url) as f:
        data = f.read().decode("utf-8")
    words = [w.strip('"') for w in data.split(",")]
    tris = {n * (n + 1) // 2 for n in range(1, 100)}
    return sum(1 for w in words if sum(ord(c) - 64 for c in w) in tris)

if __name__ == "__main__":
    print(solve())
