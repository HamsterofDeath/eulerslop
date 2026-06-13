def arrangement(n):
    return [pow(3, i, n + 1) for i in range(1, n + 1)]


def g(n):
    pos = [0] * (n + 1)
    for i, card in enumerate(arrangement(n), 1):
        pos[card] = i

    # cost[left][right] is the cheapest way to make the increasing stack
    # left,left+1,...,right.  The last merge must drag the completed left part
    # onto the completed right part, so the resulting stack stays at card right.
    cost = [[0] * (n + 2) for _ in range(n + 2)]
    for width in range(2, n + 1):
        for left in range(1, n - width + 2):
            right = left + width - 1
            right_pos = pos[right]
            best = None
            for split in range(left, right):
                candidate = (
                    cost[left][split]
                    + cost[split + 1][right]
                    + abs(pos[split] - right_pos)
                )
                if best is None or candidate < best:
                    best = candidate
            cost[left][right] = best
    return cost[1][n]


def solve():
    assert arrangement(6) == [3, 2, 6, 4, 5, 1]
    assert g(6) == 8
    assert g(16) == 47
    return g(976)


if __name__ == "__main__":
    print(solve())
