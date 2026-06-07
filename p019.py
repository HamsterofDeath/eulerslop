#!/usr/bin/env python3

def solve():
    months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    day, count = 1, 0  # 1 Jan 1900 was Monday, day=0
    # advance to 1901
    for year in range(1900, 2001):
        for m in range(12):
            days = months[m]
            if m == 1:  # February
                if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                    days = 29
            if day == 6 and year >= 1901:  # Sunday
                count += 1
            day = (day + days) % 7
    return count

if __name__ == "__main__":
    print(solve())
