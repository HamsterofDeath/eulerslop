MOD = 1000267129
INV2 = (MOD + 1) // 2
DIGITS = 10
ALL_MASKS = 1 << DIGITS


def digit_mask_counts(max_digits):
    counts = [0] * ALL_MASKS
    current = [0] * ALL_MASKS

    for first in range(1, DIGITS):
        current[1 << first] += 1
    for mask, count in enumerate(current):
        counts[mask] += count

    for _ in range(2, max_digits + 1):
        nxt = [0] * ALL_MASKS
        for mask, count in enumerate(current):
            if count:
                for digit in range(DIGITS):
                    nxt[mask | (1 << digit)] += count
        current = nxt
        for mask, count in enumerate(current):
            counts[mask] += count

    return [count % MOD for count in counts]


def solve(max_digits=18):
    counts = digit_mask_counts(max_digits)
    total_numbers = (10**max_digits - 1) % MOD
    total_pairs = total_numbers * (total_numbers - 1) * INV2

    disjoint_ordered = 0
    for left_mask, left_count in enumerate(counts):
        if left_count == 0:
            continue
        allowed = ((ALL_MASKS - 1) ^ left_mask)
        right_mask = allowed
        while right_mask:
            disjoint_ordered = (disjoint_ordered + left_count * counts[right_mask]) % MOD
            right_mask = (right_mask - 1) & allowed

    return (total_pairs - disjoint_ordered * INV2) % MOD


if __name__ == "__main__":
    print(solve())
