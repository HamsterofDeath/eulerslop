#!/usr/bin/env python3
"""Project Euler 670: coloured tilings of a 2 by n strip."""

from collections import deque


MOD = 1_000_004_321
TARGET_N = 10**16
NONE = -1
START = (0, NONE, 0, NONE, NONE, NONE, 0)


def _column_transitions(state: tuple[int, ...]) -> dict[tuple[int, ...], int]:
    """Return one-column transitions for the profile state.

    A state stores, for each row, the remaining length and colour of a
    horizontal tile crossing the left boundary, the colours immediately to the
    left, and which left-side row tiles ended at the boundary.  The final mask
    enforces the "no four corners" rule when both rows also start new
    horizontal tiles at that same boundary.
    """

    carry = [state[0], state[2]]
    carry_colour = [state[1], state[3]]
    left_colour = [state[4], state[5]]
    ended_mask = state[6]
    occupied = [None, None]
    transitions: dict[tuple[int, ...], int] = {}

    for row in range(2):
        if carry[row]:
            occupied[row] = (row, carry_colour[row], carry[row], False)

    def colours_are_valid() -> bool:
        return (
            occupied[0] is None
            or occupied[1] is None
            or occupied[0][0] == occupied[1][0]
            or occupied[0][1] != occupied[1][1]
        )

    def add_transition(started_mask: int, next_tile_id: int) -> None:
        try:
            row = next(i for i, tile in enumerate(occupied) if tile is None)
        except StopIteration:
            if ended_mask == 3 and started_mask == 3:
                return
            if not colours_are_valid():
                return

            next_carry = []
            next_colour = []
            next_left = []
            next_ended = 0
            for r in range(2):
                _, colour, remaining, is_vertical = occupied[r]
                next_left.append(colour)
                if is_vertical:
                    next_carry.append(0)
                    next_colour.append(NONE)
                else:
                    remaining -= 1
                    if remaining:
                        next_carry.append(remaining)
                        next_colour.append(colour)
                    else:
                        next_carry.append(0)
                        next_colour.append(NONE)
                        next_ended |= 1 << r

            new_state = (
                next_carry[0],
                next_colour[0],
                next_carry[1],
                next_colour[1],
                next_left[0],
                next_left[1],
                next_ended,
            )
            transitions[new_state] = transitions.get(new_state, 0) + 1
            return

        if row == 0 and occupied[1] is None:
            for colour in range(4):
                if left_colour[0] == colour or left_colour[1] == colour:
                    continue
                tile = (next_tile_id, colour, 1, True)
                occupied[0] = tile
                occupied[1] = tile
                add_transition(started_mask, next_tile_id + 1)
                occupied[0] = None
                occupied[1] = None

        for width in (1, 2, 3):
            for colour in range(4):
                if left_colour[row] == colour:
                    continue
                occupied[row] = (next_tile_id, colour, width, False)
                if colours_are_valid():
                    add_transition(started_mask | (1 << row), next_tile_id + 1)
                occupied[row] = None

    add_transition(0, 2)
    return transitions


def _build_matrix() -> tuple[list[list[int]], list[int], int]:
    states = {START: 0}
    queue = deque([START])
    transition_by_state: list[dict[tuple[int, ...], int]] = []

    while queue:
        state = queue.popleft()
        transitions = _column_transitions(state)
        transition_by_state.append(transitions)
        for next_state in transitions:
            if next_state not in states:
                states[next_state] = len(states)
                queue.append(next_state)

    size = len(states)
    matrix = [[0] * size for _ in range(size)]
    for state, i in states.items():
        for next_state, count in transition_by_state[i].items():
            matrix[i][states[next_state]] = count % MOD

    final_states = [
        i
        for state, i in states.items()
        if state[0] == 0 and state[2] == 0
    ]
    return matrix, final_states, states[START]


def _vec_mul(vector: list[int], matrix: list[list[int]]) -> list[int]:
    size = len(vector)
    result = [0] * size
    for i, value in enumerate(vector):
        if value:
            row = matrix[i]
            for j in range(size):
                result[j] += value * row[j]
    return [value % MOD for value in result]


def _mat_mul(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    size = len(left)
    result = [[0] * size for _ in range(size)]
    for i, left_row in enumerate(left):
        result_row = result[i]
        for k, value in enumerate(left_row):
            if value:
                right_row = right[k]
                for j in range(size):
                    result_row[j] += value * right_row[j]
        result[i] = [value % MOD for value in result_row]
    return result


def tilings(n: int) -> int:
    matrix, final_states, start_index = _build_matrix()
    vector = [0] * len(matrix)
    vector[start_index] = 1

    while n:
        if n & 1:
            vector = _vec_mul(vector, matrix)
        n >>= 1
        if n:
            matrix = _mat_mul(matrix, matrix)

    return sum(vector[i] for i in final_states) % MOD


def solve() -> int:
    return tilings(TARGET_N)


if __name__ == "__main__":
    print(solve())
