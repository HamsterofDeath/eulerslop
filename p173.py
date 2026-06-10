#!/usr/bin/env python3
"""p173: Hollow square laminae with at most 100 tiles.
tiles = 4k(a-k), a > 2k, count pairs (a,k) with tiles <= N."""
def solve():
    N = 1_000_000
    count = 0
    k = 1
    while True:
        # a from 2k+1 to N/(4k)+k
        max_a = N // (4 * k) + k
        min_a = 2 * k + 1
        if min_a > max_a:
            break
        count += max_a - min_a + 1
        k += 1
    return count

if __name__ == "__main__":
    print(solve())
