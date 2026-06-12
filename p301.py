#!/usr/bin/env python3

def solve():
    # By Bouton's theorem the Nim function is X(n1,n2,n3) = n1 XOR n2 XOR n3,
    # so we need n ^ 2n ^ 3n == 0, i.e. 3n == n ^ 2n.  Since 3n = n + 2n and
    # XOR is addition without carries, this holds exactly when adding n and 2n
    # produces no carry, i.e. n & (n << 1) == 0: n has no two adjacent 1-bits.
    #
    # Count binary strings of length 30 with no two adjacent ones (Fibonacci
    # recurrence: a string is "...0" appended to any valid string, or "...01"
    # appended to any valid string).  That covers n in [0, 2^30 - 1]; then
    # drop n = 0 and add n = 2^30 (a single 1-bit, which qualifies) -- the two
    # corrections cancel.
    a, b = 1, 2  # valid strings of length 0 and length 1
    for _ in range(29):
        a, b = b, a + b
    return b

if __name__ == "__main__":
    print(solve())
