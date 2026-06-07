#!/usr/bin/env python3

def solve():
    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
            "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
            "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

    def word(n):
        if n == 1000:
            return "onethousand"
        if n >= 100:
            h = ones[n // 100] + "hundred"
            if n % 100 == 0:
                return h
            return h + "and" + word(n % 100)
        if n >= 20:
            return tens[n // 10] + ones[n % 10]
        return ones[n]

    return sum(len(word(i)) for i in range(1, 1001))

if __name__ == "__main__":
    print(solve())
