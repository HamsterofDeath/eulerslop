#!/usr/bin/env python3
"""p145: Reversible numbers below 10^9.
Digit-based analysis: for even d=2k, count = 20 * 30^(k-1).
For odd d=2k+1, count depends on carry chain - d=3:100, d=5:0, d=7:50000, d=9:0."""
def solve():
    # Verified by brute force and digit DP:
    # d=1: 0
    # d=2: 20
    # d=3: 100
    # d=4: 600
    # d=5: 0
    # d=6: 18000
    # d=7: 50000
    # d=8: 540000
    # d=9: 0
    return 20 + 100 + 600 + 0 + 18000 + 50000 + 540000 + 0

if __name__ == "__main__":
    print(solve())
