#!/usr/bin/env python3
import math


def simpson(f, a, b, intervals):
    if intervals % 2:
        intervals += 1
    step = (b - a) / intervals
    total = f(a) + f(b)
    for i in range(1, intervals):
        total += (4 if i % 2 else 2) * f(a + i * step)
    return total * step / 3


def C(a, b):
    aa = a * a
    bb = b * b
    diff = bb - aa

    def speed(theta):
        s = math.sin(theta)
        c = math.cos(theta)
        h2 = aa * c * c + bb * s * s
        hp = diff * s * c / math.sqrt(h2)
        return math.sqrt(h2 + hp * hp)

    # For a rolling convex curve with support function h(theta), the center
    # has speed sqrt(h(theta)^2 + h'(theta)^2) with respect to tangent angle.
    return 4 * simpson(speed, 0.0, math.pi / 2, 100_000)


def solve():
    assert f"{C(2, 4):.8f}" == "21.38816906"
    return f"{C(1, 4) + C(3, 4):.8f}"


if __name__ == "__main__":
    print(solve())
