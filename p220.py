#!/usr/bin/env python3
"""Project Euler 220: Heighway Dragon.

D_0 = "Fa", with rewriting rules a -> "aRbFR", b -> "LFaLb".
F = forward one unit, L/R = turn 90 degrees, start at (0,0) facing up.
Find the cursor position after 10**12 steps (F's) in D_50.

For each symbol ('a' or 'b') at each expansion depth we precompute its
total effect as a transform (step count, displacement in the local frame,
net rotation).  Walking the curve, whole subtrees whose step count fits in
the remaining budget are applied in O(1); only the single branch containing
the final step is descended.
"""

DEPTH = 50
TARGET = 10 ** 12


def rotate(x, y, k):
    """Rotate vector (x, y) by k quarter-turns counterclockwise."""
    k %= 4
    if k == 0:
        return x, y
    if k == 1:
        return -y, x
    if k == 2:
        return -x, -y
    return y, -x


def compose(t1, t2):
    """Apply transform t1 then t2.  Transform = (steps, dx, dy, rot)."""
    s1, x1, y1, r1 = t1
    s2, x2, y2, r2 = t2
    x2r, y2r = rotate(x2, y2, r1)
    return (s1 + s2, x1 + x2r, y1 + y2r, (r1 + r2) % 4)


# Atomic transforms in the local frame (facing up = +y).
T_F = (1, 0, 1, 0)   # one step forward
T_L = (0, 0, 0, 1)   # turn left  (counterclockwise)
T_R = (0, 0, 0, 3)   # turn right (clockwise)
IDENTITY = (0, 0, 0, 0)


def build_tables(max_depth):
    """table[d]['a'/'b'] = total transform of that symbol expanded d times."""
    table = [{'a': IDENTITY, 'b': IDENTITY}]
    for d in range(1, max_depth + 1):
        a_prev = table[d - 1]['a']
        b_prev = table[d - 1]['b']
        # a -> a R b F R
        t_a = IDENTITY
        for t in (a_prev, T_R, b_prev, T_F, T_R):
            t_a = compose(t_a, t)
        # b -> L F a L b
        t_b = IDENTITY
        for t in (T_L, T_F, a_prev, T_L, b_prev):
            t_b = compose(t_b, t)
        table.append({'a': t_a, 'b': t_b})
    return table


def position_after(steps, depth, table):
    """Position after `steps` F-steps tracing D_depth (starting "Fa")."""
    x, y, rot = 0, 0, 0
    remaining = steps

    def apply(transform):
        nonlocal x, y, rot, remaining
        s, dx, dy, r = transform
        dxr, dyr = rotate(dx, dy, rot)
        x += dxr
        y += dyr
        rot = (rot + r) % 4
        remaining -= s

    def process(symbol, d):
        nonlocal remaining
        if remaining == 0:
            return
        if symbol == 'F':
            apply(T_F)
            return
        if symbol == 'L':
            apply(T_L)
            return
        if symbol == 'R':
            apply(T_R)
            return
        # symbol is 'a' or 'b'
        t = table[d][symbol]
        if t[0] <= remaining:
            apply(t)
            return
        expansion = "aRbFR" if symbol == 'a' else "LFaLb"
        for child in expansion:
            if remaining == 0:
                return
            process(child, d - 1)

    for sym in "Fa":
        if remaining == 0:
            break
        process(sym, depth)
    return x, y


def solve():
    table = build_tables(DEPTH)
    # Sanity check from the problem statement: 500 steps of D_10 -> (18, 16).
    assert position_after(500, 10, table) == (18, 16)
    x, y = position_after(TARGET, DEPTH, table)
    return f"{x},{y}"


if __name__ == "__main__":
    print(solve())
