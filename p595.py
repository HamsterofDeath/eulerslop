#!/usr/bin/env python3
from fractions import Fraction
from math import comb, factorial


def succession_counts(bundle_count):
    """Counts permutations by directed successions i immediately followed by i+1."""
    counts = []
    for exact in range(bundle_count):
        total = 0
        for chosen in range(exact, bundle_count):
            # Contracting any chosen set of directed successions leaves
            # bundle_count - chosen objects.  Binomial inversion converts
            # "at least this chosen set" into "exactly exact".
            total += (
                (-1) ** (chosen - exact)
                * comb(chosen, exact)
                * comb(bundle_count - 1, chosen)
                * factorial(bundle_count - chosen)
            )
        counts.append(total)
    assert sum(counts) == factorial(bundle_count)
    return counts


def expected_from_random_deck(card_count):
    expected_by_bundle_count = [Fraction(0) for _ in range(card_count + 1)]

    for bundles in range(2, card_count + 1):
        counts = succession_counts(bundles)
        total_permutations = factorial(bundles)

        same_state = Fraction(counts[0], total_permutations)
        rhs = Fraction(1)
        for successions in range(1, bundles):
            next_bundles = bundles - successions
            rhs += (
                Fraction(counts[successions], total_permutations)
                * expected_by_bundle_count[next_bundles]
            )

        expected_by_bundle_count[bundles] = rhs / (1 - same_state)

    # The initial deck is checked before any shuffle, so first merge the
    # successions already present in the random permutation of single cards.
    counts = succession_counts(card_count)
    total_permutations = factorial(card_count)
    return sum(
        Fraction(counts[successions], total_permutations)
        * expected_by_bundle_count[card_count - successions]
        for successions in range(card_count)
    )


def solve():
    assert expected_from_random_deck(2) == 1
    assert expected_from_random_deck(5) == Fraction(4213, 871)
    return f"{float(expected_from_random_deck(52)):.8f}"


if __name__ == "__main__":
    print(solve())
