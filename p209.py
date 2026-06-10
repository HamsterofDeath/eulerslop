#!/usr/bin/env python3
# Project Euler 209: Circular Logic
#
# The map sigma(a,b,c,d,e,f) = (b,c,d,e,f, a XOR (b AND c)) is a bijection on
# the 64 possible 6-bit inputs (it is invertible: given the image we recover
# a = last_bit XOR (b AND c)). The condition tau(x) AND tau(sigma(x)) = 0
# means that along every cycle of this permutation, tau may never be 1 on two
# consecutive elements. The number of binary labelings of a cycle of length n
# with no two adjacent 1s is the Lucas number L(n). The answer is the product
# of L(len) over all cycles of sigma.

def solve():
    def sigma(x):
        a = (x >> 5) & 1
        b = (x >> 4) & 1
        c = (x >> 3) & 1
        # shift left, drop a, append a XOR (b AND c)
        return ((x << 1) & 0x3F) | (a ^ (b & c))

    def lucas(n):
        # L(1)=1, L(2)=3, L(n)=L(n-1)+L(n-2)
        a, b = 2, 1  # L(0), L(1)
        for _ in range(n):
            a, b = b, a + b
        return a

    seen = [False] * 64
    result = 1
    for start in range(64):
        if seen[start]:
            continue
        length = 0
        x = start
        while not seen[x]:
            seen[x] = True
            x = sigma(x)
            length += 1
        result *= lucas(length)
    return result

if __name__ == "__main__":
    print(solve())
