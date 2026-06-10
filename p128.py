#!/usr/bin/env python3

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True

def solve():
    target = 2000
    count = 1  # tile 1

    r = 1
    while True:
        # First tile of ring r: 3r^2 - 3r + 2
        if is_prime(6*r - 1) and is_prime(6*r + 1) and is_prime(12*r + 5):
            count += 1
            if count == target:
                return 3*r*r - 3*r + 2

        # Last tile of ring r: 3r^2 + 3r + 1 (only for r >= 2)
        if r >= 2 and is_prime(6*r - 1) and is_prime(6*r + 5) and is_prime(12*r - 7):
            count += 1
            if count == target:
                return 3*r*r + 3*r + 1

        r += 1

if __name__ == "__main__":
    print(solve())
