#!/usr/bin/env python3

def solve():
    limit = 28123
    div_sum = [0] * (limit + 1)
    for i in range(1, limit + 1):
        for j in range(2 * i, limit + 1, i):
            div_sum[j] += i
            
    abundant = [i for i in range(12, limit + 1) if div_sum[i] > i]
    
    can_sum = [False] * (limit + 1)
    for i, a in enumerate(abundant):
        for b in abundant[i:]:
            s = a + b
            if s > limit:
                break
            can_sum[s] = True
            
    return sum(i for i in range(1, limit + 1) if not can_sum[i])

if __name__ == "__main__":
    print(solve())
