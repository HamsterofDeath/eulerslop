#!/usr/bin/env python3
"""Project Euler 212: Combined Volume of Cuboids.

Generate 50000 cuboids from the lagged Fibonacci generator, hash them into
a grid of 400-unit cells (max cuboid extent is 399, so intersecting cuboids
have corner cells differing by at most 1 per axis), then compute the union
volume as sum over cuboids i of vol(C_i) minus the union of intersections
of C_i with all later cuboids (recursive inclusion-exclusion on the small
intersection-box lists).
"""

CELL = 400


def make_cuboids(count):
    total_s = 6 * count
    s = [0] * (total_s + 1)
    for k in range(1, 56):
        s[k] = (100003 - 200003 * k + 300007 * k ** 3) % 1000000
    for k in range(56, total_s + 1):
        s[k] = (s[k - 24] + s[k - 55]) % 1000000
    cuboids = []
    for n in range(1, count + 1):
        i = 6 * n
        x0 = s[i - 5] % 10000
        y0 = s[i - 4] % 10000
        z0 = s[i - 3] % 10000
        dx = 1 + (s[i - 2] % 399)
        dy = 1 + (s[i - 1] % 399)
        dz = 1 + (s[i] % 399)
        cuboids.append((x0, x0 + dx, y0, y0 + dy, z0, z0 + dz))
    return cuboids


def union_volume(boxes):
    """Union volume of a (small) list of boxes via inclusion-exclusion:
    U(B_1..B_n) = sum_i [vol(B_i) - U({B_i & B_j : j > i, nonempty})]."""
    total = 0
    n = len(boxes)
    for i in range(n):
        ax0, ax1, ay0, ay1, az0, az1 = boxes[i]
        sub = []
        for j in range(i + 1, n):
            bx0, bx1, by0, by1, bz0, bz1 = boxes[j]
            ix0 = ax0 if ax0 > bx0 else bx0
            ix1 = ax1 if ax1 < bx1 else bx1
            if ix1 <= ix0:
                continue
            iy0 = ay0 if ay0 > by0 else by0
            iy1 = ay1 if ay1 < by1 else by1
            if iy1 <= iy0:
                continue
            iz0 = az0 if az0 > bz0 else bz0
            iz1 = az1 if az1 < bz1 else bz1
            if iz1 <= iz0:
                continue
            sub.append((ix0, ix1, iy0, iy1, iz0, iz1))
        total += (ax1 - ax0) * (ay1 - ay0) * (az1 - az0)
        if sub:
            total -= union_volume(sub)
    return total


def combined_volume(cuboids):
    # Spatial hash: bucket each cuboid by the cell of its low corner.
    cells = {}
    for idx, (x0, _x1, y0, _y1, z0, _z1) in enumerate(cuboids):
        key = (x0 // CELL, y0 // CELL, z0 // CELL)
        if key in cells:
            cells[key].append(idx)
        else:
            cells[key] = [idx]

    total = 0
    cells_get = cells.get
    for i, box in enumerate(cuboids):
        ax0, ax1, ay0, ay1, az0, az1 = box
        cx, cy, cz = ax0 // CELL, ay0 // CELL, az0 // CELL
        sub = []
        for gx in (cx - 1, cx, cx + 1):
            for gy in (cy - 1, cy, cy + 1):
                for gz in (cz - 1, cz, cz + 1):
                    bucket = cells_get((gx, gy, gz))
                    if not bucket:
                        continue
                    for j in bucket:
                        if j <= i:
                            continue
                        bx0, bx1, by0, by1, bz0, bz1 = cuboids[j]
                        ix0 = ax0 if ax0 > bx0 else bx0
                        ix1 = ax1 if ax1 < bx1 else bx1
                        if ix1 <= ix0:
                            continue
                        iy0 = ay0 if ay0 > by0 else by0
                        iy1 = ay1 if ay1 < by1 else by1
                        if iy1 <= iy0:
                            continue
                        iz0 = az0 if az0 > bz0 else bz0
                        iz1 = az1 if az1 < bz1 else bz1
                        if iz1 <= iz0:
                            continue
                        sub.append((ix0, ix1, iy0, iy1, iz0, iz1))
        total += (ax1 - ax0) * (ay1 - ay0) * (az1 - az0)
        if sub:
            total -= union_volume(sub)
    return total


def solve():
    cuboids = make_cuboids(50000)
    assert cuboids[0] == (7, 7 + 94, 53, 53 + 369, 183, 183 + 56)
    assert cuboids[1] == (2383, 2383 + 42, 3563, 3563 + 212, 5079, 5079 + 344)
    assert combined_volume(cuboids[:100]) == 723581599
    return combined_volume(cuboids)


if __name__ == "__main__":
    print(solve())
