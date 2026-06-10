#!/usr/bin/env python3

def u(n):
    # u_n = sum_{i=0}^{10} (-1)^i * n^i
    total = 0
    for i in range(11):
        if i % 2 == 0:
            total += n ** i
        else:
            total -= n ** i
    return total

def lagrange(x, y, n):
    result = 0
    for i in range(len(x)):
        term = y[i]
        for j in range(len(x)):
            if i != j:
                term *= (n - x[j]) / (x[i] - x[j])
        result += term
    return round(result)

def solve():
    total = 0
    terms = [u(n) for n in range(1, 12)]
    for k in range(1, 11):
        x = list(range(1, k + 1))
        y = terms[:k]
        fit = lagrange(x, y, k + 1)
        total += fit
    return total

if __name__ == "__main__":
    print(solve())
