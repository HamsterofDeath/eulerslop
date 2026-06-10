#!/usr/bin/env python3
"""Project Euler 208: Robot Walks.

The robot moves in 72-degree arcs, turning clockwise or anticlockwise each
step. Replace each arc by its chord: an anticlockwise arc from heading h is a
chord in direction 36 + 72*h degrees, a clockwise arc from heading h is a
chord in direction 36 + 72*(h-1) degrees. So every step contributes a unit
chord in one of exactly 5 directions (the 5th roots of unity rotated by 36
degrees). Since the only rational linear relation among 5th roots of unity is
1 + w + w^2 + w^3 + w^4 = 0, the path is closed iff all five chord-direction
counts are equal, i.e. each equals 70/5 = 14.

DP over (current heading, counts of chords taken in each direction class).
"""

from collections import defaultdict


def count_closed_paths(total_arcs):
    target = total_arcs // 5
    # state: (heading, (c0, c1, c2, c3, c4)) -> number of paths
    states = {(0, (0, 0, 0, 0, 0)): 1}
    for _ in range(total_arcs):
        new_states = defaultdict(int)
        for (h, counts), ways in states.items():
            # anticlockwise arc: chord class h, heading becomes h+1
            if counts[h] < target:
                c = list(counts)
                c[h] += 1
                new_states[((h + 1) % 5, tuple(c))] += ways
            # clockwise arc: chord class h-1, heading becomes h-1
            k = (h - 1) % 5
            if counts[k] < target:
                c = list(counts)
                c[k] += 1
                new_states[(k, tuple(c))] += ways
        states = new_states
    goal = (target,) * 5
    return sum(ways for (h, counts), ways in states.items() if counts == goal)


def solve():
    assert count_closed_paths(25) == 70932
    return count_closed_paths(70)


if __name__ == "__main__":
    print(solve())
