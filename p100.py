#!/usr/bin/env python3
from math import isqrt

def solve():
    target = 10 ** 12
    # P(BB) = (b/B) * ((b-1)/(B-1)) = 1/2
    # => 2b(b-1) = B(B-1) where B = total discs, b = blue discs
    # => 2b^2 - 2b = B^2 - B
    # => 2b^2 - 2b - B^2 + B = 0
    # This is a Pell-type equation
    
    # Let's use the recurrence for solutions to b^2 - 2B^2 + B - b = 0
    # Known solution sequences:
    b = 15
    B = 21
    
    while B <= target:
        # Next solution: b' = 3b + 2B - 2, B' = 4b + 3B - 3
        b, B = 3 * b + 2 * B - 2, 4 * b + 3 * B - 3
    
    return b

if __name__ == "__main__":
    print(solve())
