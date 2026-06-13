from itertools import combinations_with_replacement


START = (45, 90)


def apply_word(word):
    x, y = START
    hits = []
    for step, op in enumerate(word, 1):
        if op == "r":
            x, y = x + 1, 2 * y
        else:
            x, y = 2 * x, y + 1
        if x == y:
            hits.append((step, x))
    return x, y, hits


def word_from_blocks(blocks):
    # blocks[j] is the number of r moves made while j s moves remain.
    parts = []
    for remaining_s in range(len(blocks) - 1, -1, -1):
        parts.append("r" * blocks[remaining_s])
        if remaining_s:
            parts.append("s")
    return "".join(parts)


def lower_block_solutions(m):
    """Find words with m r moves and m s moves.

    For m r moves and m s moves, write the word as
        r^a_m s r^a_{m-1} s ... s r^a_0.

    The final equality condition is A - B = 45 * 2^m, where
      A = sum(a_j * 2^j)
      B = sum(2^prefix_j) over the s moves.
    The leading block must be close to 45 for the first possible m values, so
    only a small number of lower r moves need to be enumerated.
    """
    solutions = []
    pow_m = 1 << m

    # If a_m is smaller than this, even placing all other r moves in block
    # m-1 cannot make A large enough.  If a_m > 45, A - B is already too big
    # for the first candidate m values considered by solve().
    min_top = max(0, 90 - m)
    max_top = min(45, m)

    for top in range(min_top, max_top + 1):
        h = m - top
        target = (45 - top) * pow_m
        max_b = m * (1 << h)

        for positions in combinations_with_replacement(range(m), h):
            lower_a = sum(1 << pos for pos in positions)
            if not target <= lower_a <= target + max_b:
                continue

            prefix = 0
            idx = 0
            b = 0
            for pos in range(m):
                while idx < h and positions[idx] == pos:
                    prefix += 1
                    idx += 1
                b += 1 << prefix

            if lower_a - b == target:
                blocks = [0] * (m + 1)
                for pos in positions:
                    blocks[pos] += 1
                blocks[m] = top
                solutions.append(word_from_blocks(blocks))

    return solutions


def candidate_count_pairs(total_ops):
    """Operation-count pairs not eliminated by crude A/B bounds."""
    pairs = []
    for r_count in range(total_ops + 1):
        s_count = total_ops - r_count
        delta = START[1] * (1 << r_count) - START[0] * (1 << s_count)

        min_a_minus_b = r_count - s_count * (1 << r_count)
        max_a_minus_b = r_count * (1 << s_count) - s_count
        if min_a_minus_b <= delta <= max_a_minus_b:
            pairs.append((r_count, s_count))
    return pairs


def solve():
    # The official example is the shortest path of any parity.
    assert apply_word("rssssrsrr")[0] == 1476

    total_ops = 0
    while True:
        # Odd path length means an even number of operations.
        candidates = candidate_count_pairs(total_ops)
        words = []
        for r_count, s_count in candidates:
            # Before the first solution, the bounds leave only equal counts.
            assert r_count == s_count
            words.extend(lower_block_solutions(r_count))

        valid = []
        for word in words:
            x, y, hits = apply_word(word)
            if x == y and hits == [(len(word), x)]:
                valid.append((word, x))

        if valid:
            assert len(valid) == 1
            return valid[0][1]

        total_ops += 2


if __name__ == "__main__":
    print(solve())
