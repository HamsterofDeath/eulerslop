#!/usr/bin/env python3
"""Project Euler 287: Quadtree encoding of a disk image.

D_N is a 2^N x 2^N image, pixel (x,y) black iff
(x - 2^(N-1))^2 + (y - 2^(N-1))^2 <= 2^(2N-2): a disk of radius r = 2^(N-1)
centred on the lattice point (r, r).

Minimal encoding: a uniform region costs 2 bits, otherwise 1 bit + cost of
the four quadrants (splitting a uniform region can never be cheaper, since
1 + 4*2 > 2).  So the minimal length is determined solely by which aligned
squares are non-uniform.  If M_k = number of non-uniform aligned squares of
size 2^(N-k) (these are exactly the internal/split nodes of the tree), then
  splits = sum M_k,   leaves = sum (4*M_k - M_{k+1}) = 3*sum M_k + M_0,
  total bits = splits + 2*leaves = 7 * sum_{k=0}^{N-1} M_k + 2.

Counting M_k without touching pixels: shift to u = x - r, v = y - r.  A
square never straddles the axes, so within a quadrant the pixel of a square
closest to the centre is one corner and the farthest the opposite corner.
The square is non-uniform iff the closest pixel is inside the disk and the
farthest is outside (disk convexity).  The pixel-coordinate magnitudes in a
square of size s start at i*s on the positive side and at i*s + 1 on the
negative side, so the four quadrants are handled by offsets (dx,dy) in
{0,1}^2.  For each column A we count the valid B range with integer sqrt;
everything is vectorised with numpy (one array per level/offset).
"""

import numpy as np


def isqrt_arr(v):
    """Elementwise floor(sqrt(v)) for an int64 array, exact for v < 2^52."""
    x = np.sqrt(v.astype(np.float64)).astype(np.int64)
    x = np.where(x * x > v, x - 1, x)
    x = np.where((x + 1) * (x + 1) <= v, x + 1, x)
    return x


def solve():
    N = 24
    r = 1 << (N - 1)
    r2 = r * r

    total_M = 1  # M_0 = 1: the whole image is non-uniform
    for k in range(1, N):
        s = 1 << (N - k)          # square size at this level
        n = r // s                # squares per axis in one quadrant
        i = np.arange(n, dtype=np.int64)
        for dx in (0, 1):
            A = i * s + dx                    # closest |u| in the square
            F = A + s - 1                     # farthest |u|
            Bhi = isqrt_arr(r2 - A * A)       # max |v| with (A,|v|) inside
            F2 = r2 - F * F
            G = isqrt_arr(np.maximum(F2, 0))
            for dy in (0, 1):
                # need closest corner inside: B <= Bhi, B = j*s + dy
                jmax = np.minimum((Bhi - dy) // s, n - 1)
                # need farthest corner outside: B + s - 1 > G  (when F2 >= 0)
                lo = G + 2 - s - dy
                jmin = np.where(F2 < 0, 0, np.maximum(0, -((-lo) // s)))
                total_M += int(np.maximum(0, jmax - jmin + 1).sum())

    return 7 * total_M + 2


if __name__ == "__main__":
    print(solve())
