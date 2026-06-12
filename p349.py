#!/usr/bin/env python3

def solve():
    # Langton's ant: after ~10000 chaotic steps it builds the "highway",
    # a periodic pattern with period 104 steps that adds exactly 12 black
    # squares per period.  Simulate past the chaotic phase to a step count S
    # with S == 10^18 (mod 104), then extrapolate linearly.
    TOTAL = 10 ** 18
    PERIOD = 104
    BASE = 11000  # safely beyond the chaotic phase
    S = BASE + (TOTAL - BASE) % PERIOD

    dirs = ((0, 1), (1, 0), (0, -1), (-1, 0))  # up, right, down, left
    black = set()
    x = y = 0
    d = 0
    for step in range(S + PERIOD):
        if step == S:
            count_at_S = len(black)
        pos = (x, y)
        if pos in black:
            black.discard(pos)
            d = (d - 1) % 4  # counterclockwise on black
        else:
            black.add(pos)
            d = (d + 1) % 4  # clockwise on white
        x += dirs[d][0]
        y += dirs[d][1]

    # sanity check: one full extra period added exactly 12 black squares
    assert len(black) == count_at_S + 12

    return count_at_S + 12 * (TOTAL - S) // PERIOD

if __name__ == "__main__":
    print(solve())
