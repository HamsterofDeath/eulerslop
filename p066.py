#!/usr/bin/env python3

def solve():
    best_x = 0
    best_D = 0
    for D in range(2, 1001):
        a0 = int(D ** 0.5)
        if a0 * a0 == D:
            continue
        m, d, a = 0, 1, a0
        p1, p2 = a0, 1
        q1, q2 = 1, 0

        while True:
            m = d * a - m
            d = (D - m * m) // d
            a = (a0 + m) // d
            p = a * p1 + p2
            q = a * q1 + q2
            p2, p1 = p1, p
            q2, q1 = q1, q
            if p * p - D * q * q == 1:
                break
        if p > best_x:
            best_x, best_D = p, D
    return best_D

if __name__ == "__main__":
    print(solve())
