#!/usr/bin/env python3
"""p168: Sum of numbers 10<n<10^100 where n divides its right-rotation. Output last 5 digits."""
def solve():
    MOD = 100000
    total = 0
    
    for m in range(1, 10):
        D = 10 * m - 1
        for d in range(1, 10):
            # n = d * (10^k - 1) / D must be integer
            # Need D | d*(10^k-1) i.e., d*(10^k-1) ≡ 0 mod D
            # Find k (order) such that 10^k ≡ 1 mod (D/gcd(d,D))
            g = D
            # Actually we iterate k and check
            R = 9  # (10^1 - 1) mod D
            for k in range(2, 101):
                R = (R * 10 + 9) % D  # (10^k - 1) mod D
                if (d * R) % D == 0:
                    # n = d * (10^k - 1) // D
                    # Check n has exactly k digits
                    n = d * (10**k - 1) // D
                    if n >= 10**(k-1) and n < 10**k and n > 10:
                        total = (total + n) % MOD
    
    return total

if __name__ == "__main__":
    print(solve())
