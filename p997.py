#!/usr/bin/env python3
"""Project Euler Problem 997: Dice Box.

Represent an oriented die by a signed permutation of its three pairs of
opposite faces.  Removing the forced sign alternation along each axis
leaves variables

    X[j,k], Y[i,k], Z[i,j] in {+/-1, +/-2, +/-3}.

Their absolute values must be all different at every cell.  Viewing the
three labels as F_3, a layer has

    Z[i,j] = -X[j,k]-Y[i,k].

A nonconstant layer has a unique valid factorization, while a constant
layer has two.  Classifying the disjoint color sets used by X and Y
therefore gives 3*(2^x+2^y+2^z-4) unsigned configurations.

The signs satisfy one binary equation per cell.  Its homogeneous kernel
has dimension x+y+z-1, and every color configuration gives a consistent
right-hand side.  Thus each has 2^(x+y+z-1) sign assignments.
"""


def dice_boxes(x: int, y: int, z: int) -> int:
    unsigned = 3 * (2**x + 2**y + 2**z - 4)
    signs = 2 ** (x + y + z - 1)
    return unsigned * signs


def solve() -> int:
    return dice_boxes(9, 10, 11)


if __name__ == "__main__":
    assert dice_boxes(1, 1, 1) == 24
    assert dice_boxes(2, 3, 4) == 18_432
    print(solve())
