#!/usr/bin/env python3

def is_prime(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def solve():
    for a in range(1001, 10000):
        if not is_prime(a):
            continue
        for d in range(2, (10000 - a) // 2 + 1, 2):
            b = a + d
            c = b + d
            if c >= 10000:
                break
            if not is_prime(b) or not is_prime(c):
                continue
            sa = "".join(sorted(str(a)))
            if sa == "".join(sorted(str(b))) == "".join(sorted(str(c))):
                if a != 1487:
                    return int(str(a) + str(b) + str(c))
    return 0

if __name__ == "__main__":
    print(solve())
