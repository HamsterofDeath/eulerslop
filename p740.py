#!/usr/bin/env python3
"""Project Euler 740: Secret Santa with two slips."""

from collections import defaultdict


TARGET = 100


def failure_probability(people: int) -> float:
    states = {(0, people): 1.0}  # (names with one slip, names with two slips)

    for remaining_people in range(people, 1, -1):
        next_states = defaultdict(float)
        for (one_slip, two_slips), state_probability in states.items():
            zero_slips = remaining_people - one_slip - two_slips
            processed_slips = 2 * remaining_people - one_slip - 2 * two_slips

            for own_slips, current_count in ((0, zero_slips), (1, one_slip), (2, two_slips)):
                if current_count == 0:
                    continue
                probability = state_probability * current_count / remaining_people
                other_one = one_slip - (own_slips == 1)
                other_two = two_slips - (own_slips == 2)

                draw_states = {(other_one, other_two, processed_slips): 1.0}
                for _ in range(2):
                    after_draw = defaultdict(float)
                    for (draw_one, draw_two, old_processed), draw_probability in draw_states.items():
                        drawable = old_processed + draw_one + 2 * draw_two
                        if old_processed:
                            after_draw[(draw_one, draw_two, old_processed - 1)] += (
                                draw_probability * old_processed / drawable
                            )
                        if draw_one:
                            after_draw[(draw_one - 1, draw_two, old_processed)] += (
                                draw_probability * draw_one / drawable
                            )
                        if draw_two:
                            after_draw[(draw_one + 1, draw_two - 1, old_processed)] += (
                                draw_probability * (2 * draw_two) / drawable
                            )
                    draw_states = after_draw

                for (draw_one, draw_two, _), draw_probability in draw_states.items():
                    next_states[(draw_one, draw_two)] += probability * draw_probability
        states = next_states

    return sum(probability for (one_slip, two_slips), probability in states.items() if one_slip + two_slips == 1)


def solve() -> str:
    assert f"{failure_probability(3):.10f}" == "0.3611111111"
    assert f"{failure_probability(5):.10f}" == "0.2476095994"
    return f"{failure_probability(TARGET):.10f}"


if __name__ == "__main__":
    print(solve())
