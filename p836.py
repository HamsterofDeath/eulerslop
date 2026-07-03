#!/usr/bin/env python3
"""Project Euler 836: first letters of the bolded words."""

import re
from pathlib import Path


def solve() -> str:
    text = Path(__file__).with_name("descriptions").joinpath("p836.txt").read_text()
    words: list[str] = []
    for bold in re.findall(r"<b>(.*?)</b>", text):
        words.extend(re.findall(r"[A-Za-z]+", re.sub(r"<.*?>", " ", bold)))
    return "".join(word[0] for word in words)


if __name__ == "__main__":
    print(solve())
