#!/usr/bin/env python3
from bisect import bisect_right
from math import sqrt


ROOT2 = sqrt(2.0)
EPS = 1e-11


def _add_union_interval(intervals, start, end):
    if end <= start + 1e-14:
        return

    starts = [interval[0] for interval in intervals]
    index = bisect_right(starts, start) - 1
    if index >= 0 and intervals[index][1] >= start - 1e-12:
        start = min(start, intervals[index][0])
        end = max(end, intervals[index][1])
        merge_from = index
    else:
        merge_from = index + 1

    merge_to = merge_from
    while merge_to < len(intervals) and intervals[merge_to][0] <= end + 1e-12:
        end = max(end, intervals[merge_to][1])
        merge_to += 1
    intervals[merge_from:merge_to] = [(start, end)]


def grundy_intervals(limit):
    """Return maximal half-open intervals on which the segment Grundy value is constant."""
    covers = {}
    cover_starts = {}
    intervals = []

    def add_cover(value, start, end):
        if start >= limit or end <= 0.0:
            return
        start = max(start, 0.0)
        end = min(end, limit + 2.0)
        if end <= start:
            return
        _add_union_interval(covers.setdefault(value, []), start, end)
        cover_starts.pop(value, None)

    def add_known_segment(start, end, value):
        if intervals and intervals[-1][2] == value and abs(intervals[-1][1] - start) < 1e-9:
            intervals[-1] = (intervals[-1][0], end, value)
        else:
            intervals.append((start, end, value))

        # A move removes length 1 or sqrt(2); the two remaining subsegments
        # can have any lengths summing to one of these interval sums.
        for other_start, other_end, other_value in intervals:
            cover_value = value ^ other_value
            summed_start = start + other_start
            summed_end = end + other_end
            add_cover(cover_value, summed_start + 1.0, summed_end + 1.0)
            add_cover(cover_value, summed_start + ROOT2, summed_end + ROOT2)

    def cover_state(value, point):
        value_covers = covers.get(value)
        if not value_covers:
            return False, limit

        starts = cover_starts.get(value)
        if starts is None:
            starts = [interval[0] for interval in value_covers]
            cover_starts[value] = starts

        index = bisect_right(starts, point) - 1
        if index >= 0 and value_covers[index][1] > point + 1e-13:
            return True, value_covers[index][1]
        index += 1
        if index < len(value_covers):
            return False, value_covers[index][0]
        return False, limit

    add_known_segment(0.0, 1.0, 0)
    current = 1.0
    while current < limit - 1e-12:
        point = current + EPS
        mex = 0
        while cover_state(mex, point)[0]:
            mex += 1

        next_change = min(limit, current + 1.0, cover_state(mex, point)[1])
        for value in range(mex):
            covered, end = cover_state(value, point)
            if not covered:
                raise RuntimeError("incomplete Grundy cover")
            next_change = min(next_change, end)
        if next_change <= current + 1e-10:
            raise RuntimeError("Grundy sweep made no progress")

        add_known_segment(current, next_change, mex)
        current = next_change

    return intervals


def equality_events(intervals):
    """Slope-change events for measure{x in [0,t] : g(x) == g(t-x)}."""
    by_value = {}
    for start, end, value in intervals:
        by_value.setdefault(value, []).append((start, end))

    events = []
    for value_intervals in by_value.values():
        for a, b in value_intervals:
            for c, d in value_intervals:
                events.append((a + c, 1.0))
                events.append((min(a + d, b + c), -1.0))
                events.append((max(a + d, b + c), -1.0))
                events.append((b + d, 1.0))

    events.sort()
    merged = []
    for point, delta in events:
        if merged and abs(merged[-1][0] - point) < 1e-10:
            merged[-1] = (merged[-1][0], merged[-1][1] + delta)
        else:
            merged.append((point, delta))
    return [(point, delta) for point, delta in merged if abs(delta) > 1e-12]


def _value_and_slope(events, point):
    value = 0.0
    slope = 0.0
    previous = 0.0
    for event_point, delta in events:
        if event_point > point + 1e-12:
            break
        value += slope * (event_point - previous)
        previous = event_point
        slope += delta
    value += slope * (point - previous)
    return value, slope


def maximum_expected_gain(low, high, intervals):
    events = equality_events(intervals)
    y_straight, slope_straight = _value_and_slope(events, low - 1.0)
    y_diagonal, slope_diagonal = _value_and_slope(events, low - ROOT2)

    shifted_events = []
    for point, delta in events:
        straight_point = point + 1.0
        if low - 1e-10 <= straight_point <= high + 1e-10:
            shifted_events.append((straight_point, 0, delta))
        diagonal_point = point + ROOT2
        if low - 1e-10 <= diagonal_point <= high + 1e-10:
            shifted_events.append((diagonal_point, 1, delta))
    shifted_events.sort()

    def expected_at(length, base):
        offset = length - base
        straight = y_straight + slope_straight * offset
        diagonal = y_diagonal + slope_diagonal * offset
        return 0.5 * length * (straight / (length - 1.0) + diagonal / (length - ROOT2))

    def derivative(length, straight_constant, diagonal_constant):
        return 0.5 * (
            slope_straight
            + slope_diagonal
            - straight_constant / (length - 1.0) ** 2
            - ROOT2 * diagonal_constant / (length - ROOT2) ** 2
        )

    current = low
    index = 0
    while index < len(shifted_events) and shifted_events[index][0] <= current + 1e-10:
        index += 1

    best = expected_at(low, low)
    while current < high - 1e-12:
        next_point = high
        if index < len(shifted_events):
            next_point = min(next_point, shifted_events[index][0])

        if next_point > current + 1e-11:
            best = max(best, expected_at(current, current), expected_at(next_point, current))

            straight_constant = y_straight - slope_straight * (current - 1.0)
            diagonal_constant = y_diagonal - slope_diagonal * (current - ROOT2)
            probes = [current + (next_point - current) * k / 8.0 for k in range(9)]
            derivatives = [
                derivative(point, straight_constant, diagonal_constant) for point in probes
            ]
            for left_index in range(8):
                if derivatives[left_index] > 0.0 and derivatives[left_index + 1] < 0.0:
                    left = probes[left_index]
                    right = probes[left_index + 1]
                    for _ in range(60):
                        middle = (left + right) / 2.0
                        if derivative(middle, straight_constant, diagonal_constant) > 0.0:
                            left = middle
                        else:
                            right = middle
                    best = max(best, expected_at((left + right) / 2.0, current))

            step = next_point - current
            y_straight += slope_straight * step
            y_diagonal += slope_diagonal * step
            current = next_point

        while index < len(shifted_events) and shifted_events[index][0] <= current + 1e-10:
            _, which, delta = shifted_events[index]
            if which == 0:
                slope_straight += delta
            else:
                slope_diagonal += delta
            index += 1

    return best


def solve():
    intervals = grundy_intervals(500.0)
    assert f"{maximum_expected_gain(2.0, 10.0, intervals):.8f}" == "2.61969775"
    assert f"{maximum_expected_gain(10.0, 20.0, intervals):.8f}" == "5.99374121"
    return f"{maximum_expected_gain(200.0, 500.0, intervals):.8f}"


if __name__ == "__main__":
    print(solve())
