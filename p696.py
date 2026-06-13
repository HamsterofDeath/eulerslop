#!/usr/bin/env python3
"""Project Euler 696: Mahjong."""

from collections import defaultdict, deque


MOD = 1_000_000_007
N = 10**8
SUITS = 10**8
TRIPLES = 30
MAX_TILES = 3 * TRIPLES + 2


def _next_subset(subset, count, allow_pair):
    next_states = set()
    for state in subset:
        if allow_pair:
            active_chows, finishing_chows, pair_used = state
        else:
            active_chows, finishing_chows = state
            pair_used = 0

        for pair in (0, 1):
            if pair and (not allow_pair or pair_used):
                continue
            for pung in (0, 1):
                new_chows = count - active_chows - finishing_chows - 2 * pair - 3 * pung
                if new_chows < 0:
                    continue
                if allow_pair:
                    next_states.add((new_chows, active_chows, pair_used | pair))
                else:
                    next_states.add((new_chows, active_chows))
    return frozenset(next_states)


def _build_automaton(allow_pair):
    start = frozenset({(0, 0, 0) if allow_pair else (0, 0)})
    state_index = {start: 0}
    states = [start]
    queue = deque([start])
    transitions = []

    while queue:
        subset = queue.popleft()
        row = []
        for count in range(5):
            next_state = _next_subset(subset, count, allow_pair)
            if next_state not in state_index:
                state_index[next_state] = len(states)
                states.append(next_state)
                queue.append(next_state)
            row.append(state_index[next_state])
        transitions.append(row)

    accepting_marker = (0, 0, 1) if allow_pair else (0, 0)
    accepting = [accepting_marker in subset for subset in states]
    return transitions, accepting, state_index[frozenset()]


def _comb_large_n_small_k(n_value, k_value):
    if k_value < 0:
        return 0
    result = 1
    for index in range(1, k_value + 1):
        result = result * ((n_value - k_value + index) % MOD) % MOD
        result = result * pow(index, MOD - 2, MOD) % MOD
    return result


def _suit_polynomial(n_value, allow_pair, max_tiles):
    transitions, accepting, empty_state = _build_automaton(allow_pair)
    polynomial = [0] * (max_tiles + 1)
    if accepting[0]:
        polynomial[0] = 1

    current = defaultdict(int)
    for count in range(1, 5):
        state = transitions[0][count]
        if state != empty_state:
            current[(0, count, state)] += 1

    for nonzero_ranks in range(1, max_tiles + 1):
        for (positive_gaps, tiles, state), ways in current.items():
            if accepting[state]:
                placements = _comb_large_n_small_k(
                    n_value - nonzero_ranks + 1, positive_gaps + 1
                )
                polynomial[tiles] = (polynomial[tiles] + ways * placements) % MOD

        if nonzero_ranks == max_tiles:
            break

        next_current = defaultdict(int)
        for (positive_gaps, tiles, state), ways in current.items():
            for has_zero_gap in (0, 1):
                gap_state = transitions[state][0] if has_zero_gap else state
                if gap_state == empty_state:
                    continue
                next_positive_gaps = positive_gaps + has_zero_gap
                for count in range(1, 5):
                    next_tiles = tiles + count
                    if next_tiles > max_tiles:
                        continue
                    next_state = transitions[gap_state][count]
                    if next_state != empty_state:
                        key = (next_positive_gaps, next_tiles, next_state)
                        next_current[key] = (next_current[key] + ways) % MOD
        current = next_current
        if not current:
            break

    return polynomial


def _multiply(left, right, max_degree):
    product = [0] * (max_degree + 1)
    for i, left_value in enumerate(left):
        if left_value == 0:
            continue
        for j in range(max_degree + 1 - i):
            right_value = right[j]
            if right_value:
                product[i + j] = (product[i + j] + left_value * right_value) % MOD
    return product


def _power_polynomial(base, exponent, max_degree):
    result = [0] * (max_degree + 1)
    result[0] = 1
    while exponent:
        if exponent & 1:
            result = _multiply(result, base, max_degree)
        exponent >>= 1
        if exponent:
            base = _multiply(base, base, max_degree)
    return result


def solve():
    no_pair = _suit_polynomial(N, False, MAX_TILES)
    with_pair = _suit_polynomial(N, True, MAX_TILES)
    other_suits = _power_polynomial(no_pair, SUITS - 1, MAX_TILES)
    all_hands = _multiply(with_pair, other_suits, MAX_TILES)
    return SUITS % MOD * all_hands[MAX_TILES] % MOD


if __name__ == "__main__":
    print(solve())
