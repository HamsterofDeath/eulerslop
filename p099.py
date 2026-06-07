#!/usr/bin/env python3
import urllib.request
from math import log

def solve():
    url = "https://projecteuler.net/project/resources/p099_base_exp.txt"
    with urllib.request.urlopen(url) as f:
        data = f.read().decode("utf-8").strip().split("\n")
    
    best_val = 0
    best_line = 0
    for i, line in enumerate(data, 1):
        base, exp = map(int, line.split(","))
        val = exp * log(base)
        if val > best_val:
            best_val = val
            best_line = i
    return best_line

if __name__ == "__main__":
    print(solve())
