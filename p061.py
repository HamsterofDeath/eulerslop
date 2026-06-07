#!/usr/bin/env python3

def triangle(n): return n * (n + 1) // 2
def square(n): return n * n
def pentagonal(n): return n * (3 * n - 1) // 2
def hexagonal(n): return n * (2 * n - 1)
def heptagonal(n): return n * (5 * n - 3) // 2
def octagonal(n): return n * (3 * n - 2)

def gen4(func):
    nums = []
    n = 1
    while True:
        val = func(n)
        if val >= 10000:
            break
        if val >= 1000:
            nums.append(val)
        n += 1
    return nums

def solve():
    polys = [
        gen4(triangle),
        gen4(square),
        gen4(pentagonal),
        gen4(hexagonal),
        gen4(heptagonal),
        gen4(octagonal),
    ]

    def search(chain, used_types):
        if len(chain) == 6:
            if chain[0] // 100 == chain[-1] % 100:
                return sum(chain)
            return 0
        last2 = chain[-1] % 100
        for ptype in range(6):
            if ptype in used_types:
                continue
            for num in polys[ptype]:
                if num // 100 == last2 and num % 100 >= 10:
                    result = search(chain + [num], used_types | {ptype})
                    if result:
                        return result
        return 0

    # Start from octagonal numbers (smallest set)
    for num in polys[5]:
        result = search([num], {5})
        if result:
            return result
    return 0

if __name__ == "__main__":
    print(solve())
