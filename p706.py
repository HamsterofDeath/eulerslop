#!/usr/bin/env python3
"""Project Euler 706: 3-like numbers."""


MOD = 1_000_000_007
DIGITS = 100_000


def _encode(current, c0, c1, c2, remainder):
    return (((current * 3 + c0) * 3 + c1) * 3 + c2) * 3 + remainder


def _decode(state):
    remainder = state % 3
    state //= 3
    c2 = state % 3
    state //= 3
    c1 = state % 3
    state //= 3
    c0 = state % 3
    current = state // 3
    return current, c0, c1, c2, remainder


def _build_transitions():
    transitions = []
    for state in range(3**5):
        current, c0, c1, c2, remainder = _decode(state)
        counts = [c0, c1, c2]
        state_transitions = []
        for digit_remainder in range(3):
            new_current = (current + digit_remainder) % 3
            new_remainder = (remainder + counts[new_current]) % 3
            new_counts = counts[:]
            new_counts[new_current] = (new_counts[new_current] + 1) % 3
            state_transitions.append(
                _encode(new_current, new_counts[0], new_counts[1], new_counts[2], new_remainder)
            )
        transitions.append(tuple(state_transitions))
    return transitions


def solve():
    transitions = _build_transitions()
    dp = [0] * (3**5)
    dp[_encode(0, 1, 0, 0, 0)] = 1

    for position in range(DIGITS):
        weights = (3, 3, 3) if position == 0 else (4, 3, 3)
        next_dp = [0] * (3**5)
        for state, value in enumerate(dp):
            if value:
                state_transitions = transitions[state]
                for digit_remainder, weight in enumerate(weights):
                    target = state_transitions[digit_remainder]
                    next_dp[target] = (next_dp[target] + value * weight) % MOD
        dp = next_dp

    return sum(value for state, value in enumerate(dp) if state % 3 == 0) % MOD


if __name__ == "__main__":
    print(solve())
