LETTERS = "IVXLCDM"


def roman_below_1000(n):
    hundreds = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"]
    tens = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
    ones = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]
    return hundreds[n // 100] + tens[(n // 10) % 10] + ones[n % 10]


def solve():
    values = {roman_below_1000(n): n for n in range(1, 1000)}
    expected = {}

    for state in sorted(values, key=len, reverse=True):
        next_states = [state + letter for letter in LETTERS if state + letter in values]
        expected[state] = (
            values[state] + 7.0 * sum(expected[nxt] for nxt in next_states)
        ) / (1 + 7 * len(next_states))

    starts = sum(expected[letter] for letter in "IVXLCD")
    # From a pure run of leading Ms, any Roman letter is acceptable.  Appending
    # M returns to the same state with the represented value shifted by 1000.
    empty_expected = (7000.0 + 7.0 * starts) / 43.0
    return f"{empty_expected:.8f}"


if __name__ == "__main__":
    print(solve())
