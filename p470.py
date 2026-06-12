#!/usr/bin/env python3
from math import comb


def _level_visits(d):
    # Birth-death chain for the number of visible faces after each toggle.
    # out[k-1] is the expected total visits to level k before level 0,
    # starting from level d.
    out = []
    for target in range(1, d + 1):
        a = [0.0] * (d + 1)
        b = [0.0] * (d + 1)
        c = [0.0] * (d + 1)
        r = [0.0] * (d + 1)
        for k in range(1, d + 1):
            a[k] = -k / d if k > 1 else 0.0
            b[k] = 1.0
            c[k] = -(d - k) / d if k < d else 0.0
            r[k] = 1.0 if k == target else 0.0
        for k in range(2, d + 1):
            m = a[k] / b[k - 1]
            b[k] -= m * c[k - 1]
            r[k] -= m * r[k - 1]
        x = [0.0] * (d + 1)
        x[d] = r[d] / b[d]
        for k in range(d - 1, 0, -1):
            x[k] = (r[k] - c[k] * x[k + 1]) / b[k]
        out.append(x[d])
    return out


def _ramvok_values(mask, d, total, count):
    # V[t] is the optimal expected prize with t rolls and no up-front cost.
    v = total / count
    values = [v]
    for _ in range(2, 21):
        floor_v = int(v)
        low = mask & ((1 << floor_v) - 1) if floor_v < d else mask
        low_count = low.bit_count()
        v = (low_count * v + (total - _SUMS[low])) / count
        values.append(v)
    return values


def _all_super_values(d):
    visits = _level_visits(d)
    weights = [0.0] + [visits[k - 1] / comb(d, k) for k in range(1, d + 1)]
    acc = [0.0] * 21
    for mask in range(1, 1 << d):
        count = _COUNTS[mask]
        total = _SUMS[mask]
        w = weights[count]
        vals = _ramvok_values(mask, d, total, count)
        acc[0] += w * mask.bit_length()
        for cost in range(1, 21):
            best = 0.0
            for turns, prize in enumerate(vals, 1):
                best = max(best, prize - cost * turns)
            acc[cost] += w * best
    return acc


def solve():
    global _SUMS, _COUNTS
    max_size = 1 << 20
    _SUMS = [0] * max_size
    _COUNTS = [0] * max_size
    for mask in range(1, max_size):
        bit = mask & -mask
        prev = mask ^ bit
        _SUMS[mask] = _SUMS[prev] + bit.bit_length()
        _COUNTS[mask] = _COUNTS[prev] + 1

    assert round(_all_super_values(6)[1], 1) == 208.3
    total = sum(sum(_all_super_values(d)) for d in range(4, 21))
    return round(total)


if __name__ == "__main__":
    print(solve())
