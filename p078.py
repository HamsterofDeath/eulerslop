#!/usr/bin/env python3

def solve():
    mod = 1_000_000
    # Partition function using pentagonal number theorem
    partitions = [1]
    n = 1
    while True:
        total = 0
        k = 1
        while True:
            # Pentagonal numbers: k(3k-1)/2 and k(3k+1)/2
            pent1 = k * (3 * k - 1) // 2
            pent2 = k * (3 * k + 1) // 2
            if pent1 > n and pent2 > n:
                break
            sign = 1 if k % 2 == 1 else -1
            if pent1 <= n:
                total = (total + sign * partitions[n - pent1]) % mod
            if pent2 <= n:
                total = (total + sign * partitions[n - pent2]) % mod
            k += 1
        partitions.append(total)
        if total == 0:
            return n
        n += 1

if __name__ == "__main__":
    print(solve())
