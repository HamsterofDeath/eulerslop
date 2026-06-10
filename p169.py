#!/usr/bin/env python3
"""p169: f(n) = number of ways to express n as sum of powers of 2 using each at most twice.
f(0)=1, f(2n+1)=f(n), f(2n)=f(n)+f(n-1). Compute f(10^25)."""
from functools import lru_cache

def solve():
    @lru_cache(maxsize=None)
    def f(n):
        if n == 0:
            return 1
        if n % 2 == 1:
            return f(n // 2)
        else:
            return f(n // 2) + f(n // 2 - 1)
    
    return f(10**25)

if __name__ == "__main__":
    print(solve())
