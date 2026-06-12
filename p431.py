import numpy as np
from math import tan, radians, pi, ceil, sqrt, floor


def solve():
    # Grain poured at horizontal offset x from the centre forms a cone of repose:
    # the grain surface drops by tan(alpha) per unit horizontal distance from the
    # apex (which sits at the silo top above the delivery point). The wasted
    # volume is the gap between the flat top and that surface:
    #   V(x) = tan(alpha) * integral over the disk of dist((u,v), (x,0)) dA.
    # In polar coordinates centred at the delivery point (x,0):
    #   V(x) = (tan(alpha)/3) * int_0^{2pi} rho(theta)^3 dtheta,
    # where rho(theta) = sqrt(R^2 - x^2 sin^2 theta) - x cos theta is the
    # distance from (x,0) to the silo wall in direction theta.
    # (Check: x=0 gives (2pi/3) tan(a) R^3; R=3, a=30deg -> 32.648388556, as stated.)
    R = 6.0
    tana = tan(radians(40.0))

    n = 4096  # trapezoid rule on a smooth periodic integrand: spectral accuracy
    th = np.arange(n) * (2.0 * pi / n)
    s2 = np.sin(th) ** 2
    c = np.cos(th)

    def V(x):
        rho = np.sqrt(R * R - x * x * s2) - x * c
        return (tana / 3.0) * (2.0 * pi / n) * float(np.sum(rho ** 3))

    # V is strictly increasing on [0, R]; closed forms for the range endpoints:
    # V(0) = (2pi/3) tan(a) R^3,  V(R) = (32/9) tan(a) R^3.
    v0 = (2.0 * pi / 3.0) * tana * R ** 3
    v1 = (32.0 / 9.0) * tana * R ** 3

    # All perfect squares m^2 reachable as wasted volume.
    total = 0.0
    for m in range(ceil(sqrt(v0)), floor(sqrt(v1)) + 1):
        target = float(m * m)
        lo, hi = 0.0, R
        for _ in range(100):
            mid = 0.5 * (lo + hi)
            if V(mid) < target:
                lo = mid
            else:
                hi = mid
        total += 0.5 * (lo + hi)

    return f"{total:.9f}"


if __name__ == "__main__":
    print(solve())
