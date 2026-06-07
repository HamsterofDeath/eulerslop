#!/usr/bin/env python3

def solve():
    coins = [1, 2, 5, 10, 20, 50, 100, 200]
    ways = [0] * 201
    ways[0] = 1
    for coin in coins:
        for amount in range(coin, 201):
            ways[amount] += ways[amount - coin]
    return ways[200]

if __name__ == "__main__":
    print(solve())
