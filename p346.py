#!/usr/bin/env python3

def solve():
    # Every integer n > 2 is the repunit "11" in base n-1, so that base is free.
    # A strong repunit therefore is any number that is also a repunit of length
    # >= 3 in some base b >= 2 (i.e. 1 + b + b^2 + ... < 10^12), plus the number 1,
    # which is a repunit "1" in every base.
    LIMIT = 10 ** 12
    strong = set()
    b = 2
    while b * b + b + 1 < LIMIT:
        n = b * b + b + 1  # repunit of length 3 in base b
        while n < LIMIT:
            strong.add(n)
            n = n * b + 1  # extend the repunit by one digit
        b += 1
    return sum(strong) + 1  # include 1

if __name__ == "__main__":
    print(solve())
