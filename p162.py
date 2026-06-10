#!/usr/bin/env python3
"""p162: Count hex numbers with ≤16 digits containing 0,1,A at least once. Print as hex."""
def solve():
    total = 0
    for k in range(1, 17):
        U = 15 * (16 ** (k - 1))
        A0 = 15 * (15 ** (k - 1))
        A1 = 14 * (15 ** (k - 1))
        AA = 14 * (15 ** (k - 1))
        A01 = 14 * (14 ** (k - 1))
        A0A = 14 * (14 ** (k - 1))
        A1A = 13 * (14 ** (k - 1))
        A01A = 13 * (13 ** (k - 1))
        total += U - (A0 + A1 + AA) + (A01 + A0A + A1A) - A01A
    return hex(total)[2:].upper()

if __name__ == "__main__":
    print(solve())
