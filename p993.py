#!/usr/bin/env python3
"""Project Euler Problem 993: Banana Beaver.

Ignore the finite carried supply temporarily and always apply the fourth
rule.  Every finite game follows this universal trajectory until a blank
pair is reached with fewer than three carried bananas.  Consequently it
stops at the first record-high on-line banana count greater than N-3.

A finite certificate in the universal trajectory gives the macro-step

    (record bananas, head) -> (record bananas + 71, head + 118).

At record size 930 the configuration from 100 cells behind the head
onwards repeats after translation by 118.  During the macro-step the
head goes only 50 cells behind its starting point, so the untranslated
prefix is never inspected.  This proves the macro-step can repeat
indefinitely.
"""


TARGET = 10**18
BASE_RECORD = 930
BANANA_PERIOD = 71
POSITION_SHIFT = 118
ACTIVE_MARGIN = 100


def apply_rule(position: int, bananas: set[int]) -> int:
    here = position in bananas
    right = position + 1 in bananas

    if here and right:
        bananas.remove(position + 1)
        return position - 1
    if here:
        bananas.remove(position)
        return position + 2
    if right:
        bananas.remove(position + 1)
        bananas.add(position)
        return position + 2

    assert position - 1 not in bananas
    bananas.update((position - 1, position, position + 1))
    return position - 2


def finite_position(supply: int) -> int:
    position = 0
    bananas: set[int] = set()

    while True:
        here = position in bananas
        right = position + 1 in bananas
        if not here and not right and supply - len(bananas) < 3:
            return position
        position = apply_rule(position, bananas)


def macro_certificate() -> tuple[int, int]:
    targets = (
        BASE_RECORD,
        BASE_RECORD + BANANA_PERIOD,
        BASE_RECORD + 2 * BANANA_PERIOD,
    )
    snapshots: dict[int, tuple[int, frozenset[int], int]] = {}
    head_trace: list[int] = []

    position = 0
    bananas: set[int] = set()
    record = -1
    steps = 0

    while targets[-1] not in snapshots:
        head_trace.append(position)
        if position not in bananas and position + 1 not in bananas:
            size = len(bananas)
            if size > record:
                record = size
                if size in targets:
                    snapshots[size] = (
                        position,
                        frozenset(bananas),
                        steps,
                    )
        position = apply_rule(position, bananas)
        steps += 1

    for first_size, second_size in zip(targets, targets[1:]):
        first_head, first_bananas, first_step = snapshots[first_size]
        second_head, second_bananas, second_step = snapshots[second_size]

        assert second_head - first_head == POSITION_SHIFT
        assert second_step - first_step == 4168
        assert min(head_trace[first_step : second_step + 1]) >= (
            first_head - 50
        )

        first_suffix = {
            point - first_head
            for point in first_bananas
            if point >= first_head - ACTIVE_MARGIN
        }
        second_suffix = {
            point - second_head
            for point in second_bananas
            if point >= second_head - ACTIVE_MARGIN
        }
        assert first_suffix == second_suffix

    base_head = snapshots[BASE_RECORD][0]
    return BASE_RECORD, base_head


def solve() -> int:
    base_record, base_head = macro_certificate()
    terminal_record = TARGET - 2
    periods, remainder = divmod(
        terminal_record - base_record, BANANA_PERIOD
    )
    assert remainder == 0
    return base_head + periods * POSITION_SHIFT


if __name__ == "__main__":
    assert finite_position(1000) == 1499
    print(solve())
