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

def is_truncatable(p):
    s = str(p)
    for i in range(len(s)):
        if not is_prime(int(s[i:])):
            return False
        if not is_prime(int(s[:len(s) - i])):
            return False
    return True

def solve():
    total = 0
    count = 0
    n = 11
    while count < 11:
        if is_prime(n) and is_truncatable(n):
            total += n
            count += 1
        n += 2
    return total

if __name__ == "__main__":
    print(solve())
