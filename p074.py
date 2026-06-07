#!/usr/bin/env python3
from math import factorial

def digit_factorial(n):
    return sum(factorial(int(d)) for d in str(n))

def solve():
    target = 60
    memo = {}
    count = 0
    for n in range(1, 1_000_000):
        chain = [n]
        cur = n
        while True:
            nxt = digit_factorial(cur)
            if nxt in memo:
                length = len(chain) + memo[nxt]
                break
            if nxt in chain:
                # Found a loop
                idx = chain.index(nxt)
                # All in the loop
                loop_len = len(chain) - idx
                base_len = len(tuple(chain[:idx]))
                length = base_len + loop_len
                break
            chain.append(nxt)
            cur = nxt
        memo[n] = length
        if length == target:
            count += 1
    return count

if __name__ == "__main__":
    print(solve())
