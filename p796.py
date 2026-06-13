#!/usr/bin/env python3
"""Project Euler 796: collecting suits, ranks, and deck designs."""

from decimal import Decimal, ROUND_HALF_UP, getcontext
from fractions import Fraction
from math import comb


def rounded(value: Fraction, places: int) -> str:
    getcontext().prec = 50
    scale = "0." + "0" * (places - 1) + "1"
    decimal = Decimal(value.numerator) / Decimal(value.denominator)
    return str(decimal.quantize(Decimal(scale), rounding=ROUND_HALF_UP))


def expected_rank_collection() -> Fraction:
    cards = 54
    total = Fraction(0, 1)
    for ranks in range(1, 14):
        sign = 1 if ranks % 2 else -1
        total += sign * comb(13, ranks) * Fraction(cards + 1, 4 * ranks + 1)
    return total


def expected_full_collection() -> Fraction:
    total_cards = 10 * 54
    total = Fraction(0, 1)
    for suits in range(5):
        for ranks in range(14):
            per_unselected_deck = 13 * suits + 4 * ranks - suits * ranks
            for decks in range(11):
                selected = suits + ranks + decks
                if selected == 0:
                    continue
                marked = decks * 54 + (10 - decks) * per_unselected_deck
                sign = 1 if selected % 2 else -1
                total += (
                    sign
                    * comb(4, suits)
                    * comb(13, ranks)
                    * comb(10, decks)
                    * Fraction(total_cards + 1, marked + 1)
                )
    return total


def solve() -> str:
    assert rounded(expected_rank_collection(), 8) == "29.05361725"
    return rounded(expected_full_collection(), 8)


if __name__ == "__main__":
    print(solve())
