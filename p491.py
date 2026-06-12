#!/usr/bin/env python3
from math import factorial


def solve():
    fact = [factorial(i) for i in range(11)]
    total = 0

    def dfs(d, slots, digit_sum, counts):
        nonlocal total
        if d == 10:
            if slots == 10 and digit_sum % 11 == 1:
                odd_den = even_den = 1
                for c in counts:
                    odd_den *= fact[c]
                    even_den *= fact[2 - c]
                odd = fact[10] // odd_den
                if counts[0]:
                    lead_zero_den = fact[counts[0] - 1]
                    for c in counts[1:]:
                        lead_zero_den *= fact[c]
                    odd -= fact[9] // lead_zero_den
                total += odd * (fact[10] // even_den)
            return

        for c in range(3):
            if slots + c <= 10:
                counts.append(c)
                dfs(d + 1, slots + c, digit_sum + d * c, counts)
                counts.pop()

    dfs(0, 0, 0, [])
    return total


if __name__ == "__main__":
    print(solve())
