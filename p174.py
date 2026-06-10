#!/usr/bin/env python3
"""p174: Count N(t) in [1,10] for hollow square laminae up to 1M tiles."""
def solve():
    N = 1_000_000
    freq = [0] * (N + 1)
    k = 1
    while True:
        max_a = N // (4 * k) + k
        min_a = 2 * k + 1
        if min_a > max_a:
            break
        for a in range(min_a, max_a + 1):
            tiles = 4 * k * (a - k)
            freq[tiles] += 1
        k += 1
    
    count_hist = [0] * 100
    for t in range(1, N + 1):
        f = freq[t]
        if 1 <= f <= 10:
            count_hist[f] += 1
    
    return sum(count_hist[1:11])

if __name__ == "__main__":
    print(solve())
