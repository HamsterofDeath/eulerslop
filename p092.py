#!/usr/bin/env python3

def solve():
    limit = 10_000_000
    # For each starting number, compute chain until 1 or 89
    count = 0
    memo = {1: 1, 89: 89}
    for n in range(1, limit):
        chain = []
        cur = n
        while cur not in memo:
            chain.append(cur)
            cur = sum(int(d) ** 2 for d in str(cur))
        end = memo[cur]
        for x in chain:
            memo[x] = end
        if end == 89:
            count += 1
    return count

if __name__ == "__main__":
    print(solve())
