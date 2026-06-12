#!/usr/bin/env python3
# Project Euler 327 - Rooms of Doom
#
# Travelling through R rooms means passing R+1 doors. With capacity C:
# if R+1 <= C we just carry R+1 cards: M(C,R) = R+1.
# Otherwise, treat room 1 as the new start: we must deliver X = M(C,R-1)
# cards into room 1's box. A round trip (start -> room1 -> start) costs 2
# cards (enter + exit) and can deposit at most C-2 cards; the final entry
# costs 1 card and brings in at most C-1 usable cards. With k round trips:
#   k*(C-2) + (C-1) >= X,  k = max(0, ceil((X-(C-1))/(C-2)))
# and the total dispensed is M(C,R) = X + 2k + 1 (delivered cards plus
# the 2k+1 overhead cards burned on doors).

def M(C, R):
    if R + 1 <= C:
        return R + 1
    X = M(C, R - 1)
    k = max(0, -(-(X - (C - 1)) // (C - 2)))
    return X + 2 * k + 1

def solve():
    # sanity checks from the statement
    assert M(3, 6) == 123 and M(4, 6) == 23
    assert sum(M(c, 10) for c in range(3, 11)) == 10382
    return sum(M(c, 30) for c in range(3, 41))

if __name__ == "__main__":
    print(solve())
