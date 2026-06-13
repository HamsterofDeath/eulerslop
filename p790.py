#!/usr/bin/env python3
"""Project Euler 790: clock grid rectangle updates."""

from collections import defaultdict
import sys


GRID = 50_515_093
SEED = 290_797
HOURS = [12] + list(range(1, 12))
TARGET_STEPS = 100_000


class SegmentTree:
    def __init__(self, coords: list[int]):
        self.coords = coords
        self.count = len(coords) - 1
        self.size = 4 * self.count + 5
        self.buckets = [[0] * self.size for _ in range(12)]
        self.lazy = [0] * self.size
        self._build(1, 0, self.count)

    def _build(self, node: int, left: int, right: int) -> None:
        self.buckets[0][node] = self.coords[right] - self.coords[left]
        if right - left == 1:
            return
        mid = (left + right) // 2
        self._build(node * 2, left, mid)
        self._build(node * 2 + 1, mid, right)

    def _shift(self, node: int, amount: int) -> None:
        amount %= 12
        if amount == 0:
            return
        old = [self.buckets[i][node] for i in range(12)]
        for i, value in enumerate(old):
            self.buckets[(i + amount) % 12][node] = value
        self.lazy[node] = (self.lazy[node] + amount) % 12

    def _push(self, node: int) -> None:
        amount = self.lazy[node]
        if amount:
            self._shift(node * 2, amount)
            self._shift(node * 2 + 1, amount)
            self.lazy[node] = 0

    def _pull(self, node: int) -> None:
        left = node * 2
        right = left + 1
        for i in range(12):
            self.buckets[i][node] = self.buckets[i][left] + self.buckets[i][right]

    def add(self, query_left: int, query_right: int, amount: int) -> None:
        self._add(1, 0, self.count, query_left, query_right, amount)

    def _add(
        self,
        node: int,
        left: int,
        right: int,
        query_left: int,
        query_right: int,
        amount: int,
    ) -> None:
        if query_left <= left and right <= query_right:
            self._shift(node, amount)
            return
        self._push(node)
        mid = (left + right) // 2
        if query_left < mid:
            self._add(node * 2, left, mid, query_left, query_right, amount)
        if mid < query_right:
            self._add(node * 2 + 1, mid, right, query_left, query_right, amount)
        self._pull(node)

    def hour_sum(self) -> int:
        return sum(HOURS[i] * self.buckets[i][1] for i in range(12))


def rectangles(steps: int) -> list[tuple[int, int, int, int]]:
    out = []
    value = SEED
    for _ in range(steps):
        values = []
        for _ in range(4):
            values.append(value)
            value = value * value % GRID
        x0, x1 = sorted(values[:2])
        y0, y1 = sorted(values[2:])
        out.append((x0, x1 + 1, y0, y1 + 1))
    return out


def clock_sum(steps: int) -> int:
    if steps == 0:
        return 12 * GRID * GRID

    rects = rectangles(steps)
    y_coords = {0, GRID}
    events: dict[int, list[tuple[int, int, int]]] = defaultdict(list)
    for x0, x1, y0, y1 in rects:
        y_coords.add(y0)
        y_coords.add(y1)
        events[x0].append((y0, y1, 1))
        events[x1].append((y0, y1, -1))

    coords = sorted(y_coords)
    index = {value: i for i, value in enumerate(coords)}
    tree = SegmentTree(coords)

    total = 0
    previous_x = 0
    for x in sorted(events):
        if x > previous_x:
            total += (x - previous_x) * tree.hour_sum()
        for y0, y1, delta in events[x]:
            tree.add(index[y0], index[y1], delta)
        previous_x = x
    if previous_x < GRID:
        total += (GRID - previous_x) * tree.hour_sum()
    return total


def solve() -> int:
    sys.setrecursionlimit(1_000_000)
    assert clock_sum(0) == 30_621_295_449_583_788
    assert clock_sum(1) == 30_613_048_345_941_659
    assert clock_sum(10) == 21_808_930_308_198_471
    assert clock_sum(100) == 16_190_667_393_984_172
    return clock_sum(TARGET_STEPS)


if __name__ == "__main__":
    print(solve())
