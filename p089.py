#!/usr/bin/env python3
import urllib.request

def solve():
    url = "https://projecteuler.net/project/resources/p089_roman.txt"
    with urllib.request.urlopen(url) as f:
        numerals = [line.strip() for line in f.read().decode("utf-8").strip().split("\n")]

    roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}

    def from_roman(s):
        total = 0
        prev = 0
        for c in reversed(s):
            val = roman_map[c]
            if val < prev:
                total -= val
            else:
                total += val
            prev = val
        return total

    def to_roman(n):
        result = ""
        vals = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
                (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
                (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
        for v, r in vals:
            while n >= v:
                result += r
                n -= v
        return result

    saved = 0
    for num in numerals:
        saved += len(num) - len(to_roman(from_roman(num)))
    return saved

if __name__ == "__main__":
    print(solve())
