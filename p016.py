#!/usr/bin/env python3

def solve():
    return sum(int(d) for d in str(2 ** 1000))

if __name__ == "__main__":
    print(solve())
