#!/usr/bin/env python3

def solve():
    target = 100
    ways = [0] * (target + 1)
    ways[0] = 1
    for n in range(1, target):
        for amount in range(n, target + 1):
            ways[amount] += ways[amount - n]
    return ways[target]

if __name__ == "__main__":
    print(solve())
