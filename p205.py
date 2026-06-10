#!/usr/bin/env python3
from collections import defaultdict


def dist(num_dice, sides):
    """Probability distribution of the sum of num_dice fair dice with given sides."""
    d = {0: 1.0}
    for _ in range(num_dice):
        nd = defaultdict(float)
        for total, p in d.items():
            for face in range(1, sides + 1):
                nd[total + face] += p / sides
        d = nd
    return d


def solve():
    peter = dist(9, 4)
    colin = dist(6, 6)
    p_win = sum(pp * pc
                for sp, pp in peter.items()
                for sc, pc in colin.items()
                if sp > sc)
    return f"{p_win:.7f}"


if __name__ == "__main__":
    print(solve())
