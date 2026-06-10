#!/usr/bin/env python3

def solve():
    numbers = []
    limit = 10 ** 15  # generous upper bound for a_30
    for base in range(2, 100):  # digit sum
        for exp in range(2, 50):
            n = base ** exp
            if n > limit:
                break
            if n < 10:
                continue
            if sum(int(d) for d in str(n)) == base:
                numbers.append(n)
    numbers.sort()
    return numbers[29]  # a_30 (0-indexed: index 29)

if __name__ == "__main__":
    print(solve())
