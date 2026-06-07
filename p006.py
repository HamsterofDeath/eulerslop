#!/usr/bin/env python3

def solve():
    n = 100
    sum_squares = n * (n + 1) * (2 * n + 1) // 6
    square_sum = (n * (n + 1) // 2) ** 2
    return square_sum - sum_squares

if __name__ == "__main__":
    print(solve())
