#!/usr/bin/env python3
from math import isqrt


def probability(size):
    square_labels = {i * i for i in range(1, isqrt(size * size) + 1)}
    dyn_num = dyn_den = 0
    fixed_num = fixed_den = 0

    for r in range(size):
        for c in range(size):
            label = r * size + c + 1
            degree = (r > 0) + (r + 1 < size) + (c > 0) + (c + 1 < size)

            # Rule (i) has transition probabilities 1/(degree+1), including
            # staying put, so the reversible stationary weight is degree+1.
            dyn_weight = degree + 1
            # Rule (ii) has a fixed self-loop and uniform moves, giving the
            # usual random-walk stationary weight degree.
            fixed_weight = degree

            dyn_den += dyn_weight
            fixed_den += fixed_weight
            if label in square_labels:
                dyn_num += dyn_weight
                fixed_num += fixed_weight

    return 0.5 * (dyn_num / dyn_den + fixed_num / fixed_den)


def solve():
    assert f"{probability(5):.12f}" == "0.177976190476"
    return f"{probability(1000):.12f}"


if __name__ == "__main__":
    print(solve())
