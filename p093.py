#!/usr/bin/env python3
from itertools import combinations, permutations

def evaluate(a, b, c, d, ops):
    results = set()
    forms = [
        lambda a,b,c,d,o1,o2,o3: o3(o1(a, b), o2(c, d)),
        lambda a,b,c,d,o1,o2,o3: o3(o2(o1(a, b), c), d),
        lambda a,b,c,d,o1,o2,o3: o3(o2(a, o1(b, c)), d),
        lambda a,b,c,d,o1,o2,o3: o3(a, o2(o1(b, c), d)),
        lambda a,b,c,d,o1,o2,o3: o3(a, o2(b, o1(c, d))),
    ]
    for o1f, o2f, o3f in ((a,b,c) for a in ops for b in ops for c in ops):
        for f in forms:
            try:
                val = f(float(a),b,float(c),d, o1f,o2f,o3f)
                if val > 0 and abs(val - round(val)) < 1e-9:
                    results.add(int(round(val)))
            except ZeroDivisionError:
                pass
    return results

def apply(x, y, op):
    if op == '+': return x + y
    if op == '-': return x - y
    if op == '*': return x * y
    if op == '/': return x / y if y != 0 else None
    return None

def evaluate_all(nums):
    ops = [lambda x,y,a='+': apply(x,y,a),
           lambda x,y,a='-': apply(x,y,a),
           lambda x,y,a='*': apply(x,y,a),
           lambda x,y,a='/': apply(x,y,a)]
    results = set()
    for perm in set(permutations(nums)):
        a, b, c, d = perm
        for o1 in [add, sub, mul, div]:
            for o2 in [add, sub, mul, div]:
                for o3 in [add, sub, mul, div]:
                    # 5 parenthesizations
                    try:
                        v = o3(o1(float(a), b), o2(float(c), d))
                        if v > 0 and abs(v - round(v)) < 1e-9: results.add(int(round(v)))
                    except: pass
                    try:
                        v = o3(o2(o1(float(a), b), float(c)), d)
                        if v > 0 and abs(v - round(v)) < 1e-9: results.add(int(round(v)))
                    except: pass
                    try:
                        v = o3(o2(float(a), o1(float(b), c)), d)
                        if v > 0 and abs(v - round(v)) < 1e-9: results.add(int(round(v)))
                    except: pass
                    try:
                        v = o3(float(a), o2(o1(float(b), c), d))
                        if v > 0 and abs(v - round(v)) < 1e-9: results.add(int(round(v)))
                    except: pass
                    try:
                        v = o3(float(a), o2(float(b), o1(float(c), d)))
                        if v > 0 and abs(v - round(v)) < 1e-9: results.add(int(round(v)))
                    except: pass
    return results

def add(x, y):
    return x + y

def sub(x, y):
    return x - y

def mul(x, y):
    return x * y

def div(x, y):
    if y == 0:
        raise ZeroDivisionError
    return x / y

def consecutive(results):
    n = 1
    while n in results:
        n += 1
    return n - 1

def solve():
    ops = [add, sub, mul, div]
    best = (0, "")
    for a, b, c, d in combinations(range(1, 10), 4):
        results = evaluate_all([a, b, c, d])
        n = consecutive(results)
        if n > best[0]:
            best = (n, f"{a}{b}{c}{d}")
    return best[1]

if __name__ == "__main__":
    print(solve())
