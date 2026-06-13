#!/usr/bin/env python3
"""Project Euler 679: Freefarea."""

from collections import defaultdict, deque


ALPHABET = "AEFR"
KEYWORDS = ("FREE", "FARE", "AREA", "REEF")
TARGET_LENGTH = 30


def _build_automaton(patterns):
    nexts = []
    fail = []
    outputs = []

    def new_node():
        nexts.append({})
        fail.append(0)
        outputs.append(0)
        return len(nexts) - 1

    new_node()
    for index, pattern in enumerate(patterns):
        state = 0
        for char in pattern:
            if char not in nexts[state]:
                nexts[state][char] = new_node()
            state = nexts[state][char]
        outputs[state] |= 1 << index

    queue = deque(nexts[0].values())
    while queue:
        state = queue.popleft()
        outputs[state] |= outputs[fail[state]]
        for char, child in nexts[state].items():
            fallback = fail[state]
            while fallback and char not in nexts[fallback]:
                fallback = fail[fallback]
            fail[child] = nexts[fallback].get(char, 0)
            queue.append(child)

    transitions = []
    for state in range(len(nexts)):
        row = []
        for char in ALPHABET:
            fallback = state
            while fallback and char not in nexts[fallback]:
                fallback = fail[fallback]
            row.append(nexts[fallback].get(char, 0))
        transitions.append(row)

    return transitions, outputs


def _increment_counts(encoded_counts, matched_mask):
    for keyword in range(len(KEYWORDS)):
        if matched_mask & (1 << keyword):
            power = 3 ** keyword
            count = (encoded_counts // power) % 3
            if count == 1:
                return None
            encoded_counts += power
    return encoded_counts


def count_words(length):
    transitions, outputs = _build_automaton(KEYWORDS)
    target_counts = sum(3 ** i for i in range(len(KEYWORDS)))
    dp = {(0, 0): 1}

    for _ in range(length):
        next_dp = defaultdict(int)
        for (state, counts), ways in dp.items():
            for char_index in range(len(ALPHABET)):
                new_state = transitions[state][char_index]
                new_counts = _increment_counts(counts, outputs[new_state])
                if new_counts is not None:
                    next_dp[(new_state, new_counts)] += ways
        dp = next_dp

    return sum(
        ways
        for (_state, counts), ways in dp.items()
        if counts == target_counts
    )


def solve():
    return count_words(TARGET_LENGTH)


if __name__ == "__main__":
    print(solve())
