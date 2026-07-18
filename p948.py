#!/usr/bin/env python3
"""Project Euler Problem 948: Left and Right.

For a word w, let A(w) say Left wins with Left to move and B(w) say
Left wins with Right to move.  Optimal play gives

    A(w) = OR  B(s) over proper nonempty suffixes s,
    B(w) = AND A(p) over proper nonempty prefixes p.

Induction with the usual lattice-path/ballot encoding shows that the
(0,0) and (1,1) classes both contain
C(n-1, floor((n-1)/2)) words.  The (0,1) class is empty for odd n and
has Catalan number C_{n/2-1} words for even n.  The requested (1,0)
class is everything left over.
"""

from math import comb


def count_first_player_wins(n: int) -> int:
    equal_class = comb(n - 1, (n - 1) // 2)
    exceptional = 0
    if n % 2 == 0:
        index = n // 2 - 1
        exceptional = comb(2 * index, index) // (index + 1)
    return 2**n - 2 * equal_class - exceptional


def solve() -> int:
    assert count_first_player_wins(3) == 4
    assert count_first_player_wins(8) == 181
    return count_first_player_wins(60)


if __name__ == "__main__":
    print(solve())
