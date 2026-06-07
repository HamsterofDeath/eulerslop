#!/usr/bin/env python3

def solve():
    limit = 28123
    abundant = [i for i in range(1, limit + 1) if sum(j for j in range(1, i) if i % j == 0) > i]
    can_sum = [False] * (limit + 1)
    for i, a in enumerate(abundant):
        for b in abundant[i:]:
            s = a + b
            if s > limit:
                break
            can_sum[s] = True
    return sum(i for i, ok in enumerate(can_sum) if not ok)

if __name__ == "__main__":
    print(solve())
