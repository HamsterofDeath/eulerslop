#!/usr/bin/env python3
"""Project Euler Problem 960: Stone Game Solitaire.

A successful sequence has n-1 turns.  In any connected component with
v piles and e turns, conservation of stones gives

    n*e = v*(n-1).

Thus the turn graph must be one connected tree.  Cutting an edge into
components of sizes s and n-s shows that its endpoint removals are
n-s and s, respectively, so its score is min(s,n-s).

For each cut size, choose the vertices on both sides, choose a Cayley
tree on each side, and choose the endpoints of the joining edge.  Every
tree's distinct edges may then be played in any of (n-1)! orders.
"""

from math import comb, factorial


MODULUS = 1_000_000_007


def stone_game_total(pile_count: int) -> int:
    tree_score_sum = 0

    for smaller_side in range(1, pile_count // 2 + 1):
        larger_side = pile_count - smaller_side
        tree_edge_pairs = (
            comb(pile_count, smaller_side)
            * smaller_side ** (smaller_side - 1)
            * larger_side ** (larger_side - 1)
        )

        # Equal-sized sides describe the same unoriented cut twice.
        if smaller_side == larger_side:
            tree_edge_pairs //= 2

        tree_score_sum += smaller_side * tree_edge_pairs

    return factorial(pile_count - 1) * tree_score_sum


def solve() -> int:
    assert stone_game_total(3) == 12
    assert stone_game_total(4) == 360
    assert stone_game_total(8) == 16_785_941_760
    return stone_game_total(100) % MODULUS


if __name__ == "__main__":
    print(solve())
