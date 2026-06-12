#!/usr/bin/env python3
import numpy as np

def solve():
    # Represent each square by its base corner A and base vector h (|h| = s),
    # the square lying to the left of A -> A+h; r = rot90(h).  Its corners are
    # A, A+h, A+h+r, A+r.  The 3-4-5 right triangle sits on the far side
    # A+r .. A+h+r (hypotenuse, smaller leg on the right), so its apex is at
    #   P = A + (16/25) h + (1 + 12/25) r
    # (the altitude foot splits the hypotenuse 16/25 : 9/25, altitude 12/25).
    # The two child squares are built on the legs:
    #   left : base A+r -> P, vector (16 h + 12 r)/25, side (4/5) s
    #   right: base P -> A+h+r, vector (9 h - 12 r)/25, side (3/5) s
    # Every point of the subtree rooted at a square of side s lies within
    # distance K*s of A: the square itself is within sqrt(2)*s and the child
    # anchors within 1.612*s, so K = max(sqrt2, 1 + 0.8K, 1.612 + 0.6K) gives
    # K = 5.  Hence a whole branch can be pruned once 5*s cannot push any of
    # the four current axis-aligned bounds further than eps.
    eps = 1e-13
    minx, maxx, miny, maxy = 0.0, 1.0, 0.0, 1.0
    ax = np.array([0.0]); ay = np.array([0.0])      # base corner A
    hx = np.array([1.0]); hy = np.array([0.0])      # base vector h
    s = np.array([1.0])                             # side length

    while ax.size:
        rx, ry = -hy, hx
        # track the corners B, C, D and the apex P (A was tracked as a parent
        # corner; the root square is covered by the initial 0..1 bounds)
        px = np.concatenate((ax + hx, ax + hx + rx, ax + rx,
                             ax + 0.64 * hx + 1.48 * rx))
        py = np.concatenate((ay + hy, ay + hy + ry, ay + ry,
                             ay + 0.64 * hy + 1.48 * ry))
        minx = min(minx, px.min()); maxx = max(maxx, px.max())
        miny = min(miny, py.min()); maxy = max(maxy, py.max())

        # children of every active square
        cax = np.concatenate((ax + rx, ax + 0.64 * hx + 1.48 * rx))
        cay = np.concatenate((ay + ry, ay + 0.64 * hy + 1.48 * ry))
        chx = np.concatenate((0.64 * hx + 0.48 * rx, 0.36 * hx - 0.48 * rx))
        chy = np.concatenate((0.64 * hy + 0.48 * ry, 0.36 * hy - 0.48 * ry))
        cs = np.concatenate((0.8 * s, 0.6 * s))

        reach = 5.0 * cs  # whole subtree stays within this radius of A
        keep = ((cax + reach > maxx + eps) | (cax - reach < minx - eps) |
                (cay + reach > maxy + eps) | (cay - reach < miny - eps))
        ax, ay, hx, hy, s = cax[keep], cay[keep], chx[keep], chy[keep], cs[keep]

    return "%.10f" % ((maxx - minx) * (maxy - miny))

if __name__ == "__main__":
    print(solve())
