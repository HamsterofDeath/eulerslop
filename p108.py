#!/usr/bin/env python3

def num_divisors(n):
    result = 1
    i = 2
    while i * i <= n:
        exp = 0
        while n % i == 0:
            n //= i
            exp += 1
        result *= (2 * exp + 1)
        i += 1 if i == 2 else 2
    if n > 1:
        result *= 3
    return result

def solve():
    n = 1
    while True:
        # Solutions to 1/x+1/y=1/n correspond to d(n^2)
        # count = (d(n^2)+1)/2, need count > 1000
        if (num_divisors(n) + 1) // 2 > 1000:
            return n
        n += 1

if __name__ == "__main__":
    print(solve())
