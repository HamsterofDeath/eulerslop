#!/usr/bin/env python3
import heapq

def solve():
    target = 4000000
    need = 2 * target - 1  # 7,999,999
    
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    
    # Priority queue: (n, d, max_e, p_idx)
    heap = [(1, 1, 60, 0)]
    best = float('inf')
    
    while heap:
        n, d, max_e, p_idx = heapq.heappop(heap)
        if d > need:
            return n
        if p_idx >= len(primes):
            continue
        p = primes[p_idx]
        for e in range(1, max_e + 1):
            next_n = n * (p ** e)
            if next_n >= best:
                break
            next_d = d * (2 * e + 1)
            if next_d > need:
                best = min(best, next_n)
            else:
                heapq.heappush(heap, (next_n, next_d, e, p_idx + 1))
    
    return best

if __name__ == "__main__":
    print(solve())
