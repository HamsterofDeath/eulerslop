#!/usr/bin/env python3

def sum_divisors(n):
    total = 1
    d = 2
    while d * d <= n:
        if n % d == 0:
            total += d
            if d * d != n:
                total += n // d
        d += 1
    return total

def solve():
    limit = 1_000_000
    divisor_sums = [0] * (limit + 1)
    for i in range(1, limit + 1):
        for j in range(2 * i, limit + 1, i):
            divisor_sums[j] += i

    longest_chain = 0
    best_min = 0
    visited = [0] * (limit + 1)
    
    for start in range(2, limit + 1):
        if visited[start]:
            continue
        chain = []
        cur = start
        while cur <= limit and not visited[cur]:
            visited[cur] = start
            chain.append(cur)
            cur = divisor_sums[cur]
        if cur <= limit and visited[cur] == start:
            # Found a cycle
            idx = chain.index(cur)
            cycle = chain[idx:]
            if len(cycle) > longest_chain:
                longest_chain = len(cycle)
                best_min = min(cycle)
    return best_min

if __name__ == "__main__":
    print(solve())
