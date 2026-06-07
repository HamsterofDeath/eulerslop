#!/usr/bin/env python3

def solve():
    products = set()
    for a in range(1, 100):
        for b in range(a, 10000):
            c = a * b
            s = str(a) + str(b) + str(c)
            if len(s) > 9:
                break
            if len(s) == 9 and set(s) == set("123456789"):
                products.add(c)
    return sum(products)

if __name__ == "__main__":
    print(solve())
