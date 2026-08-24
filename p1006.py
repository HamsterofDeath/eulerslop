#!/usr/bin/env python3
"""Project Euler Problem 1006: Fibonacci Subwords.

Put alpha = phi^-2.  The Fibonacci word is the mechanical word of slope
alpha, and its length-k factors are obtained by varying the intercept rho:

    b_i(rho) = floor((i + 1) alpha + rho) - floor(i alpha + rho).

The k breakpoints are {-j alpha} = {j / phi}, 1 <= j <= k.  Starting
just to the right of zero gives ``0`` followed by the first k-1 Fibonacci
digits.  Crossing breakpoint j swaps 01 to 10 and therefore adds
9*10^(k-1-j); the last breakpoint, j=k, instead adds 1.  The sweep visits
all k+1 factors once and in increasing numerical order.

It remains to aggregate the breakpoint sweep without sorting k items.
Let

    A_0, A_1, ... = 1, 2, 5, 13, ...,
    A_(m+1) = 3 A_m - A_(m-1).

These are the odd-index Fibonacci numbers and the denominators that
approach 1/phi from below.  Rotate the breakpoint order so it begins at
j=1.  In this cyclic order, j-1 is written canonically as

    j - 1 = sum d_i A_i,       d_i in {0, 1, 2},

and the items are in lexicographic order of (d_0,d_1,...).  Canonical
digit strings are recognized by a two-state automaton.  If ``low`` says
that the value of the lower digits is below A_i-A_(i-1), then

    digit 0: low <- true
    digit 1: low is unchanged
    digit 2: allowed only when low; low <- false.

The initial state is false.  A three-way comparison state simultaneously
restricts the represented value to j <= k.  Thus a digit DP with only
O(log k) states produces the ordered sequence of weights 10^(-j).

For a weight sequence, retain its total and the sums of its prefix sums
and squared prefix sums.  These four quantities compose under sequence
concatenation.  Splitting at j=k and at the first actual breakpoint (the
largest A_m <= k) rotates the digit-DP order back, replaces the exceptional
last weight by 1, and yields Psi(k) in O(log k) time.
"""

from functools import cache
from typing import NamedTuple


MOD = 101_001_001
INV10 = pow(10, -1, MOD)


class Summary(NamedTuple):
    """Monoid summary for weights and all their nonempty prefix sums."""

    length: int
    total: int
    prefix_sum: int
    prefix_square_sum: int


EMPTY = Summary(0, 0, 0, 0)


def singleton(weight: int = 1) -> Summary:
    weight %= MOD
    return Summary(1, weight, weight, weight * weight % MOD)


def concatenate(left: Summary, right: Summary) -> Summary:
    """Summary of the concatenation ``left + right``."""
    shifted = right.length % MOD
    return Summary(
        left.length + right.length,
        (left.total + right.total) % MOD,
        (left.prefix_sum + right.prefix_sum + shifted * left.total) % MOD,
        (
            left.prefix_square_sum
            + right.prefix_square_sum
            + 2 * left.total * right.prefix_sum
            + shifted * left.total * left.total
        )
        % MOD,
    )


def scaled(summary: Summary, factor: int) -> Summary:
    """Multiply every weight represented by ``summary`` by ``factor``."""
    factor %= MOD
    return Summary(
        summary.length,
        summary.total * factor % MOD,
        summary.prefix_sum * factor % MOD,
        summary.prefix_square_sum * factor * factor % MOD,
    )


def without_prefix(full: Summary, prefix: Summary) -> Summary:
    """Recover B from summaries for A+B and A."""
    length = full.length - prefix.length
    if length < 0:
        raise ValueError("prefix is longer than the full sequence")
    total = (full.total - prefix.total) % MOD
    prefix_sum = (
        full.prefix_sum - prefix.prefix_sum - (length % MOD) * prefix.total
    ) % MOD
    prefix_square_sum = (
        full.prefix_square_sum
        - prefix.prefix_square_sum
        - 2 * prefix.total * prefix_sum
        - (length % MOD) * prefix.total * prefix.total
    ) % MOD
    return Summary(length, total, prefix_sum, prefix_square_sum)


class ColexSweep:
    """The cyclic breakpoint order beginning at j=1.

    Items carry the geometric weight INV10**j.  Besides the full summary,
    prefixes before named indices can be extracted in logarithmic time.
    """

    def __init__(self, limit: int):
        if limit < 1:
            raise ValueError("limit must be positive")
        self.limit = limit

        capacities = [1]
        if limit > 1:
            capacities.append(2)
            while capacities[-1] < limit:
                capacities.append(3 * capacities[-1] - capacities[-2])

        # A capacity A_m uses digit places A_0 through A_(m-1).
        self.places = tuple(capacities[:-1])
        self.bound_digits = self._digits(limit - 1)
        self.place_powers = tuple(pow(INV10, place, MOD) for place in self.places)
        self.full = scaled(self._all(0, False, 0), INV10)
        if self.full.length != limit:
            raise AssertionError("Fibonacci numeral DP produced the wrong item count")

    def _digits(self, value: int) -> tuple[int, ...]:
        """Greedy canonical digits, returned from low place to high."""
        digits = [0] * len(self.places)
        for i in range(len(self.places) - 1, -1, -1):
            digits[i] = min(2, value // self.places[i])
            value -= digits[i] * self.places[i]
        if value:
            raise AssertionError("value is outside the numeral-system capacity")
        return tuple(digits)

    @staticmethod
    def _next_low(low: bool, digit: int) -> bool:
        if digit == 0:
            return True
        if digit == 1:
            return low
        return False

    def _next_comparison(self, comparison: int, digit: int, pos: int) -> int:
        """A higher digit overrides comparisons made by all lower digits."""
        bound = self.bound_digits[pos]
        if digit < bound:
            return -1
        if digit > bound:
            return 1
        return comparison

    @cache
    def _all(self, pos: int, low: bool, comparison: int) -> Summary:
        """All accepted completions from one digit-DP state."""
        if pos == len(self.places):
            return singleton() if comparison <= 0 else EMPTY

        result = EMPTY
        for digit in range(3 if low else 2):
            child = self._all(
                pos + 1,
                self._next_low(low, digit),
                self._next_comparison(comparison, digit, pos),
            )
            result = concatenate(
                result, scaled(child, pow(self.place_powers[pos], digit, MOD))
            )
        return result

    def prefix_before(self, index: int) -> Summary:
        """Summary of all items before ``index`` in the colex order."""
        if not 1 <= index <= self.limit:
            raise ValueError("index is outside the sweep")
        target = self._digits(index - 1)

        def visit(pos: int, low: bool, comparison: int) -> Summary:
            if pos == len(self.places):
                return EMPTY

            result = EMPTY
            wanted = target[pos]
            for digit in range(3 if low else 2):
                next_low = self._next_low(low, digit)
                next_comparison = self._next_comparison(comparison, digit, pos)
                factor = pow(self.place_powers[pos], digit, MOD)
                if digit < wanted:
                    result = concatenate(
                        result,
                        scaled(
                            self._all(pos + 1, next_low, next_comparison), factor
                        ),
                    )
                elif digit == wanted:
                    result = concatenate(
                        result,
                        scaled(visit(pos + 1, next_low, next_comparison), factor),
                    )
                    break
                else:
                    break
            return result

        # The digit DP represents index-1; restore the extra power INV10.
        return scaled(visit(0, False, 0), INV10)


def first_breakpoint_index(k: int) -> int:
    """Largest member of 1,2,5,13,... not exceeding k."""
    if k == 1:
        return 1
    previous, current = 1, 2
    while current <= k:
        previous, current = current, 3 * current - previous
    return previous


def event_summary(k: int) -> Summary:
    """Prefix-sum summary of the actual decimal changes in breakpoint order."""
    sweep = ColexSweep(k)
    start = first_breakpoint_index(k)

    before_start = sweep.prefix_before(start)
    start_item = singleton(pow(INV10, start, MOD))
    through_start = concatenate(before_start, start_item)
    after_start = without_prefix(sweep.full, through_start)

    before_last = sweep.prefix_before(k)
    last_item = singleton(pow(INV10, k, MOD))
    through_last = concatenate(before_last, last_item)

    # Rotate Q_k (which starts at j=1) so it starts at the smallest
    # fractional breakpoint, j=start, and split immediately around j=k.
    if start == k:
        before = EMPTY
        after = concatenate(after_start, before_start)
    elif before_last.length > before_start.length:
        middle = without_prefix(before_last, through_start)
        before = concatenate(start_item, middle)
        after = concatenate(without_prefix(sweep.full, through_last), before_start)
    else:
        before = concatenate(concatenate(start_item, after_start), before_last)
        after = without_prefix(before_start, through_last)

    if before.length + 1 + after.length != k:
        raise AssertionError("breakpoint rotation lost an event")

    # For j<k the decimal change is 9*10^(k-1-j).  The formula would
    # assign 9/10 to j=k, whose true endpoint change is instead exactly 1.
    geometric_scale = 9 * pow(10, k - 1, MOD) % MOD
    return concatenate(
        concatenate(scaled(before, geometric_scale), singleton(1)),
        scaled(after, geometric_scale),
    )


def fibonacci_prefix_value(length: int) -> int:
    """Base-10 value modulo MOD of the first ``length`` Fibonacci digits."""
    if length <= 0:
        return 0

    # S_0="0", S_1="01", and S_n=S_(n-1)S_(n-2).
    lengths = [1, 2]
    values = [0, 1]
    while lengths[-1] < length:
        right_length = lengths[-2]
        lengths.append(lengths[-1] + right_length)
        values.append((values[-1] * pow(10, right_length, MOD) + values[-2]) % MOD)

    def prefix(block: int, wanted: int) -> int:
        if wanted == 0:
            return 0
        if wanted == lengths[block]:
            return values[block]
        if wanted <= lengths[block - 1]:
            return prefix(block - 1, wanted)
        right_wanted = wanted - lengths[block - 1]
        return (
            values[block - 1] * pow(10, right_wanted, MOD)
            + prefix(block - 2, right_wanted)
        ) % MOD

    return prefix(len(lengths) - 1, length)


def psi(k: int) -> int:
    """Return Psi(k) modulo 101001001."""
    changes = event_summary(k)
    # At rho=0+ the factor is 0 followed by the first k-1 Fibonacci
    # digits, which has the same integer value as that shorter prefix.
    initial = fibonacci_prefix_value(k - 1)
    return (
        ((k + 1) % MOD) * initial * initial
        + 2 * initial * changes.prefix_sum
        + changes.prefix_square_sum
    ) % MOD


def solve() -> int:
    return psi(10**18)


if __name__ == "__main__":
    assert psi(3) == 20_302
    assert psi(10) == 10_699_667
    print(solve())
