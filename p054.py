#!/usr/bin/env python3
import urllib.request

def rank_hand(hand):
    values = "23456789TJQKA"
    suits = "CDHS"
    cards = [(values.index(c[0]), suits.index(c[1])) for c in hand]
    cards.sort(reverse=True)
    vals = [c[0] for c in cards]
    suits_list = [c[1] for c in cards]
    flush = len(set(suits_list)) == 1
    straight = len(set(vals)) == 5 and vals[0] - vals[4] == 4
    counts = {}
    for v in vals:
        counts[v] = counts.get(v, 0) + 1
    count_vals = sorted(counts.items(), key=lambda x: (x[1], x[0]), reverse=True)

    if straight and flush:
        return (8, vals, [])
    if count_vals[0][1] == 4:
        return (7, [count_vals[0][0]], [count_vals[1][0]])
    if count_vals[0][1] == 3 and count_vals[1][1] == 2:
        return (6, [count_vals[0][0]], [count_vals[1][0]])
    if flush:
        return (5, vals, [])
    if straight:
        return (4, vals, [])
    if count_vals[0][1] == 3:
        return (3, [count_vals[0][0]], [v for v in vals if v != count_vals[0][0]])
    if count_vals[0][1] == 2 and count_vals[1][1] == 2:
        return (2, [count_vals[0][0], count_vals[1][0]], [count_vals[2][0]])
    if count_vals[0][1] == 2:
        return (1, [count_vals[0][0]], [v for v in vals if v != count_vals[0][0]])
    return (0, vals, [])

def solve():
    url = "https://projecteuler.net/project/resources/p054_poker.txt"
    with urllib.request.urlopen(url) as f:
        data = f.read().decode("utf-8")
    p1_wins = 0
    for line in data.strip().split("\n"):
        cards = line.split()
        p1 = cards[:5]
        p2 = cards[5:]
        if rank_hand(p1) > rank_hand(p2):
            p1_wins += 1
    return p1_wins

if __name__ == "__main__":
    print(solve())
