#!/usr/bin/env python3

def solve():
    total = 0
    for n in range(10, 6 * 9**5):  # 6*9^5 = 354294
        if n == sum(int(d) ** 5 for d in str(n)):
            total += n
    return total

if __name__ == "__main__":
    print(solve())
