#!/usr/bin/env python3
"""p156: Sum of solutions to f(n,d)=n for d=1..9."""
def count_digits(n, d):
    if n < 0:
        return 0
    total = 0
    factor = 1
    while factor <= n:
        lower = n % factor
        cur = (n // factor) % 10
        higher = n // (factor * 10)
        if d == 0:
            if higher == 0:
                break
            higher -= 1
        if cur > d:
            total += (higher + 1) * factor
        elif cur == d:
            total += higher * factor + lower + 1
        else:
            total += higher * factor
        factor *= 10
    return total + (1 if d == 0 else 0)

def find_solutions(d):
    sols = []
    n = 0
    while n < 10**13:
        f_n = count_digits(n, d)
        if f_n == n:
            sols.append(n)
            n += 1
        elif f_n > n:
            n += max(1, (f_n - n) // 10)
        else:
            digits = max(1, len(str(n)))
            max_growth = digits
            n += max(1, (n - f_n) // max(max_growth, 1))
    return sols

def solve():
    total = 0
    for d in range(1, 10):
        sols = find_solutions(d)
        total += sum(sols)
    return total

if __name__ == "__main__":
    print(solve())
