#!/usr/bin/env python3

def is_palindrome(n):
    s = str(n)
    return s == s[::-1]

def reverse(n):
    return int(str(n)[::-1])

def is_lychrel(n):
    for _ in range(50):
        n += reverse(n)
        if is_palindrome(n):
            return False
    return True

def solve():
    return sum(1 for n in range(1, 10000) if is_lychrel(n))

if __name__ == "__main__":
    print(solve())
