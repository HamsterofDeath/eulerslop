"""Project Euler Problem 919: Fortunate Triangles.

For a vertex A, AH = 2R*|cos(A)|. Thus the required condition is
|cos(A)| = 1/4. The law of cosines can then be parametrized through

    w^2 + 15*y^2 = (4*z)^2,

using coprime positive u,v. After a common scaling, the two possible adjacent
sides are

    x = |u^2 - 15v^2 +/- 2uv|,
    y = 8uv,
    z = u^2 + 15v^2.

The parameter symmetries give four representations of each primitive
triangle. Selecting the smallest rational parameter in each orbit reduces to
the two integer inequalities used below, giving one canonical representation.
"""

from math import isqrt

import numpy as np


TARGET = 10**7


def fortunate_perimeter_sum(limit: int) -> int:
    result = 0

    # For coprime u,v, gcd(x,y,z) divides 120. A canonical raw perimeter is
    # at least 30v^2, so v <= sqrt(4*limit) covers every primitive triangle.
    for v in range(1, isqrt(4 * limit) + 1):
        u = np.arange(1, 2 * v, dtype=np.int64)
        v_value = np.int64(v)
        u_squared = u * u
        uv = u * v_value
        v_squared = v_value * v_value

        coprime = np.gcd(u, v_value) == 1
        y = 8 * uv
        z = u_squared + 15 * v_squared

        # x = 15v^2-u^2-2uv. Canonical t=u/v satisfies
        # t <= 5(3-t)/(t+5), yielding t^2+10t <= 15.
        canonical = coprime & (
            u_squared + 10 * uv <= 15 * v_squared
        )
        x = 15 * v_squared - u_squared - 2 * uv
        raw_perimeter = 30 * v_squared + 6 * uv
        result += branch_sum(
            x, y, z, raw_perimeter, canonical, limit
        )

        # x = 15v^2-u^2+2uv. The corresponding smallest-orbit condition is
        # t <= 3(5-t)/(t+3), yielding t^2+6t <= 15.
        canonical = coprime & (
            u_squared + 6 * uv <= 15 * v_squared
        )
        x = 15 * v_squared - u_squared + 2 * uv
        raw_perimeter = 30 * v_squared + 10 * uv
        result += branch_sum(
            x, y, z, raw_perimeter, canonical, limit
        )

    return result


def branch_sum(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    raw_perimeter: np.ndarray,
    canonical: np.ndarray,
    limit: int,
) -> int:
    common_divisor = np.gcd(np.gcd(x, y), z)
    primitive_perimeter = raw_perimeter // common_divisor
    primitive_perimeter = primitive_perimeter[
        canonical & (primitive_perimeter <= limit)
    ]
    if primitive_perimeter.size == 0:
        return 0

    multiples = limit // primitive_perimeter
    contributions = (
        primitive_perimeter * multiples * (multiples + 1) // 2
    )
    return int(np.sum(contributions, dtype=np.int64))


def solve() -> int:
    assert fortunate_perimeter_sum(10) == 24
    assert fortunate_perimeter_sum(100) == 3_331
    return fortunate_perimeter_sum(TARGET)


if __name__ == "__main__":
    print(solve())
