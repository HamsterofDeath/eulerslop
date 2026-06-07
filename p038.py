#!/usr/bin/env python3

def solve():
    best = "918273645"
    for n in range(1, 10000):
        concat = ""
        k = 1
        while len(concat) < 9:
            concat += str(n * k)
            k += 1
        if len(concat) == 9 and set(concat) == set("123456789") and concat > best:
            best = concat
    return int(best)

if __name__ == "__main__":
    print(solve())
