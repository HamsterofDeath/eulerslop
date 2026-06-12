#!/usr/bin/env python3
from collections import Counter
from functools import lru_cache
from math import comb

PHRASE = "thereisasyetinsufficientdataforameaningfulanswer"
LIMIT = 15
LETTERS = tuple(sorted(Counter(PHRASE)))
START = tuple(Counter(PHRASE)[c] for c in LETTERS)


@lru_cache(None)
def _count_words(counts, room):
    dp = [0] * (room + 1)
    dp[0] = 1
    for available in counts:
        nxt = [0] * (room + 1)
        for used, value in enumerate(dp):
            if not value:
                continue
            for take in range(min(available, room - used) + 1):
                nxt[used + take] += value * comb(used + take, take)
        dp = nxt
    return sum(dp)


def P(word):
    counts = list(START)
    rank = 0
    for pos, ch in enumerate(word):
        idx = LETTERS.index(ch)
        for i in range(idx):
            if counts[i]:
                counts[i] -= 1
                rank += _count_words(tuple(counts), LIMIT - pos - 1)
                counts[i] += 1
        counts[idx] -= 1
        if pos == len(word) - 1:
            return rank + 1
        rank += 1
    raise ValueError("empty word")


def W(position):
    counts = list(START)
    out = []
    while True:
        room = LIMIT - len(out) - 1
        for i, ch in enumerate(LETTERS):
            if not counts[i]:
                continue
            counts[i] -= 1
            cnt = _count_words(tuple(counts), room)
            if position > cnt:
                position -= cnt
                counts[i] += 1
                continue
            out.append(ch)
            if position == 1:
                return "".join(out)
            position -= 1
            break


def solve():
    assert W(10) == "aaaaaacdee"
    assert P("aaaaaacdee") == 10
    assert W(115246685191495243) == "euler"
    assert P("euler") == 115246685191495243
    target = (
        P("legionary")
        + P("calorimeters")
        - P("annihilate")
        + P("orchestrated")
        - P("fluttering")
    )
    return W(target)


if __name__ == "__main__":
    print(solve())
