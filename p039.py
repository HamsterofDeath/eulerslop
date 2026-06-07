#!/usr/bin/env python3

def solve():
    best_p = 0
    best_count = 0
    for p in range(12, 1001):
        count = 0
        for a in range(1, p // 3):
            # a^2 + b^2 = c^2 and a+b+c = p
            # b = (p^2 - 2pa) / (2p - 2a)
            # c = p - a - b
            b = (p * p - 2 * p * a) // (2 * (p - a))
            c = p - a - b
            if a * a + b * b == c * c and a < b < c:
                count += 1
        if count > best_count:
            best_count, best_p = count, p
    return best_p

if __name__ == "__main__":
    print(solve())
