#!/usr/bin/env python3
import math

def solve():
    # Fragments launched in every direction from height h with speed v trace
    # parabolas whose envelope is the "safety paraboloid":
    #   z(r) = H - g*r^2/(2*v^2),  where H = h + v^2/(2*g).
    # Every point between the ground and the envelope is crossed by some
    # fragment, so the region is the solid of revolution under the envelope.
    # Volume = int_0^R 2*pi*r*z(r) dr with z(R)=0, i.e. R^2 = 2*v^2*H/g.
    # The elementary integral evaluates to V = pi * v^2 * H^2 / g.
    h, v, g = 100.0, 20.0, 9.81
    H = h + v * v / (2 * g)
    V = math.pi * v * v * H * H / g
    return f"{V:.4f}"

if __name__ == "__main__":
    print(solve())
