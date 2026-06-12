#!/usr/bin/env python3
from math import comb


def solve():
    # Linearity of expectation: for each colour, subtract the probability that
    # all 20 drawn balls came from the other 60 balls.
    expected = 7 * (1 - comb(60, 20) / comb(70, 20))
    return f"{expected:.9f}"


if __name__ == "__main__":
    print(solve())
