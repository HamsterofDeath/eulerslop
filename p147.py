#!/usr/bin/env python3
"""p147: Rectangles in cross-hatched grids up to 47x43."""
def aa(m, n):
    """Axis-aligned rectangles in m x n grid."""
    return m * (m + 1) * n * (n + 1) // 4

def dd(m, n):
    """Diagonal (diamond) rectangles in m x n cross-hatched grid."""
    total = 0
    mn = min(m, n)
    for a in range(1, 2 * mn):
        for b in range(1, 2 * mn - a + 1):
            u_max = 2 * m - a - b
            v_min = b
            v_max = 2 * n - a
            if u_max < 0 or v_max < v_min:
                continue
            # Count u in [0, u_max], v in [v_min, v_max], u ≡ v (mod 2)
            # Partition u into even and odd
            u_even = u_max // 2 + 1
            u_odd = (u_max + 1) // 2
            
            # Even v in range
            ev_first = v_min if v_min % 2 == 0 else v_min + 1
            ev_last = v_max if v_max % 2 == 0 else v_max - 1
            v_even = (ev_last - ev_first) // 2 + 1 if ev_first <= ev_last else 0
            
            # Odd v in range
            od_first = v_min if v_min % 2 == 1 else v_min + 1
            od_last = v_max if v_max % 2 == 1 else v_max - 1
            v_odd = (od_last - od_first) // 2 + 1 if od_first <= od_last else 0
            
            total += u_even * v_even + u_odd * v_odd
    return total

def solve():
    total = 0
    for i in range(1, 48):
        for j in range(1, 44):
            total += aa(i, j) + dd(i, j)
    return total

if __name__ == "__main__":
    print(solve())
