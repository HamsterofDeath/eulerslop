#!/usr/bin/env python3

def solve():
    limit = 12000
    min_ps = [2 * k for k in range(limit + 1)]  # min_ps[k] = min product-sum for k terms

    def factorize(prod, total, count, start):
        k = prod - total + count
        if k <= limit:
            if prod < min_ps[k]:
                min_ps[k] = prod
        for f in range(start, 2 * limit // prod + 1):
            new_prod = prod * f
            if new_prod > 2 * limit:
                break
            factorize(new_prod, total + f, count + 1, f)

    factorize(1, 1, 1, 2)
    return sum(set(min_ps[2:]))

if __name__ == "__main__":
    print(solve())
