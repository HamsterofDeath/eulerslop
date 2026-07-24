#!/usr/bin/env python3
"""Project Euler Problem 987: Straight Eight.

Scan the thirteen ranks while retaining the straights that still need
cards.  At most four can be active because every active straight needs
a distinct suit at the current rank.

Hands are made canonical by ordering them first by their straight's
starting rank and then by their suit at that first rank.  This counts
unordered collections directly, including when several hands use the
same rank interval.  A track also records whether all suits seen so far
are identical, so flushes can be rejected when the fifth card arrives.

The high-ace interval wraps around the rank order.  Conditioning on its
ace suits makes those hands dormant until rank ten and leaves an ordinary
linear transfer over the other nine intervals.
"""

from collections import defaultdict
from itertools import combinations, permutations


SUIT_COUNT = 4
CHANGED_SUIT = SUIT_COUNT
RANK_COUNT = 13
TARGET_STRAIGHTS = 8

# A track is (canonical hand id, ranks still to process, monochrome suit).
Track = tuple[int, int, int]
State = tuple[int, tuple[Track, ...]]


def straight_collections(straight_count: int) -> int:
    answer = 0

    for high_count in range(min(SUIT_COUNT, straight_count) + 1):
        ordinary_count = straight_count - high_count
        high_ids = range(ordinary_count, straight_count)

        for high_ace_suits in combinations(
            range(SUIT_COUNT), high_count
        ):
            dormant_high_tracks = tuple(
                (hand_id, 4, suit)
                for hand_id, suit in zip(high_ids, high_ace_suits)
            )
            states: dict[State, int] = {(0, ()): 1}

            for rank in range(RANK_COUNT):
                next_states: defaultdict[State, int] = defaultdict(int)

                for (next_id, stored_tracks), ways in states.items():
                    tracks = list(stored_tracks)
                    if rank == 9:
                        tracks.extend(dormant_high_tracks)

                    free_suits = [
                        suit
                        for suit in range(SUIT_COUNT)
                        if not (
                            rank == 0 and suit in high_ace_suits
                        )
                    ]
                    maximum_new = 0
                    if rank <= 8:
                        maximum_new = min(
                            SUIT_COUNT - len(tracks),
                            ordinary_count - next_id,
                        )

                    for new_count in range(maximum_new + 1):
                        # Rank 9 is the last possible ordinary start.
                        if (
                            rank == 8
                            and next_id + new_count != ordinary_count
                        ):
                            continue

                        for old_suits in permutations(
                            free_suits, len(tracks)
                        ):
                            unused_suits = [
                                suit
                                for suit in free_suits
                                if suit not in old_suits
                            ]
                            for new_suits in combinations(
                                unused_suits, new_count
                            ):
                                updated: list[Track] = []
                                valid = True

                                for track, suit in zip(
                                    tracks, old_suits
                                ):
                                    hand_id, remaining, mono = track
                                    if (
                                        mono != CHANGED_SUIT
                                        and suit != mono
                                    ):
                                        mono = CHANGED_SUIT
                                    remaining -= 1
                                    if remaining == 0:
                                        if mono != CHANGED_SUIT:
                                            valid = False
                                            break
                                    else:
                                        updated.append(
                                            (hand_id, remaining, mono)
                                        )

                                if not valid:
                                    continue

                                for offset, suit in enumerate(new_suits):
                                    updated.append(
                                        (next_id + offset, 4, suit)
                                    )
                                updated.sort()
                                state = (
                                    next_id + new_count,
                                    tuple(updated),
                                )
                                next_states[state] += ways

                states = next_states

            answer += states.get((ordinary_count, ()), 0)

    return answer


def solve() -> int:
    assert straight_collections(1) == 10_200
    assert straight_collections(2) == 31_832_952
    return straight_collections(TARGET_STRAIGHTS)


if __name__ == "__main__":
    print(solve())
