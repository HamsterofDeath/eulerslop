#!/usr/bin/env python3
import numpy as np


def chocolate(a, b, r=1.0):
    # Candy centre: b^2 x^2 + b^2 y^2 + a^2 z^2 = a^2 b^2, i.e. the spheroid
    # x^2/a^2 + y^2/a^2 + z^2/b^2 = 1 (semi-axes a, a, b) - a convex body K.
    # Steiner formula for the outer parallel body of a convex K in 3D:
    #   V(K_r) = V + S*r + M*r^2 + (4*pi/3)*r^3,
    # where S is the surface area and M = integral of the mean curvature
    # (k1+k2)/2 over the surface.  Chocolate volume = V(K_r) - V.
    #
    # Parametrise: x = a sin(t) cos(phi), y = a sin(t) sin(phi), z = b cos(t),
    # w(t) = sqrt(a^2 cos^2 t + b^2 sin^2 t).  Then
    #   dA = a sin(t) w dt dphi,
    #   principal curvatures: k1 = a*b/w^3 (meridian), k2 = b/(a*w) (parallel),
    # giving
    #   S = 2*pi * int_0^pi a sin(t) w dt
    #   M = pi  * int_0^pi (a^2 b / w^2 + b) sin(t) dt.
    x, wt = np.polynomial.legendre.leggauss(200)
    t = 0.5 * np.pi * (x + 1.0)
    wt = wt * 0.5 * np.pi
    w = np.sqrt((a * np.cos(t)) ** 2 + (b * np.sin(t)) ** 2)
    S = 2.0 * np.pi * np.sum(wt * a * np.sin(t) * w)
    M = np.pi * np.sum(wt * (a * a * b / (w * w) + b) * np.sin(t))
    return S * r + M * r * r + (4.0 / 3.0) * np.pi * r ** 3


def solve():
    # Validate against the two examples from the statement.
    assert abs(chocolate(1, 1) - 28.0 / 3.0 * np.pi) < 1e-9
    assert abs(chocolate(2, 1) - 60.35475635) < 5e-8
    return f"{chocolate(3, 1):.8f}"


if __name__ == "__main__":
    print(solve())
