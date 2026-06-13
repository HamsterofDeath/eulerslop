MOD = 1_000_000_007


def perimeter_prefix(q):
    """Sum of minimum 2D perimeters for areas 1..q."""
    if q <= 0:
        return 0

    r = int(q**0.5)
    while (r + 1) * (r + 1) <= q:
        r += 1
    while r * r > q:
        r -= 1

    n = r - 1
    total = 8 * n * (n + 1) * (2 * n + 1) // 6 + 10 * n * (n + 1) // 2

    rem = q - r * r
    total += 4 * r
    first_band = min(rem, r)
    total += first_band * (4 * r + 2)
    second_band = max(0, rem - r)
    total += second_band * (4 * r + 4)
    return total


def rectangle_perimeter_prefix(q, a, b):
    if q <= 0:
        return 0
    if a > b:
        a, b = b, a
    if q <= a * a:
        return perimeter_prefix(q)
    return perimeter_prefix(a * a) + (q - a * a) * 2 * (a + b)


def surface_sum(limit):
    total = 0
    a = 1
    while a**3 <= limit:
        # Start with an a x a x a cube and add a layer on an a x a face.
        qmax = min(a * a, limit - a**3)
        total += (qmax + 1) * 6 * a * a + rectangle_perimeter_prefix(qmax, a, a)

        # Then continue from an a x a x (a+1) cuboid.
        start = a * a * (a + 1)
        if limit > start:
            qmax = min(a * (a + 1), limit - start)
            total += qmax * (6 * a * a + 4 * a)
            total += rectangle_perimeter_prefix(qmax, a, a + 1)

        # Finally continue from an a x (a+1) x (a+1) cuboid.  The terminal
        # full cube belongs to the next iteration, so stop one cell early.
        start = a * (a + 1) * (a + 1)
        if limit > start:
            qmax = min((a + 1) * (a + 1) - 1, limit - start)
            total += qmax * (6 * a * a + 8 * a + 2)
            total += rectangle_perimeter_prefix(qmax, a + 1, a + 1)

        a += 1
    return total


def g_sum(limit):
    separate_wrapping = 3 * limit * (limit + 1)
    return (separate_wrapping - surface_sum(limit)) % MOD


def solve():
    assert g_sum(18) == 530
    assert g_sum(10**6) == 951640919
    return g_sum(10**16)


if __name__ == "__main__":
    print(solve())
