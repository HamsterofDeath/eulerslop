#!/usr/bin/env python3
import urllib.request
from math import isqrt

def solve():
    url = "https://projecteuler.net/project/resources/p098_words.txt"
    with urllib.request.urlopen(url) as f:
        words = [w.strip('"') for w in f.read().decode("utf-8").split(",")]
    
    # Group by sorted letters (anagrams)
    anagram_groups = {}
    for w in words:
        key = "".join(sorted(w))
        anagram_groups.setdefault(key, []).append(w)
    
    pairs = []
    for group in anagram_groups.values():
        if len(group) >= 2:
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    pairs.append((group[i], group[j]))
    
    best_square = 0
    max_len = max(len(w) for p in pairs for w in p)
    
    # Precompute squares by digit length
    squares_by_len = {}
    n = 1
    while True:
        s = n * n
        ss = str(s)
        if len(ss) > max_len:
            break
        squares_by_len.setdefault(len(ss), []).append(s)
        n += 1
    
    for w1, w2 in pairs:
        L = len(w1)
        if L not in squares_by_len:
            continue
        for sq in squares_by_len[L]:
            sq_str = str(sq)
            # Map letters to digits
            mapping = {}
            reverse_map = {}
            valid = True
            for c1, d in zip(w1, sq_str):
                if c1 in mapping:
                    if mapping[c1] != d:
                        valid = False
                        break
                else:
                    if d in reverse_map:
                        valid = False
                        break
                    mapping[c1] = d
                    reverse_map[d] = c1
            if not valid:
                continue
            # Apply to w2
            w2_num_str = "".join(mapping[c] for c in w2)
            if w2_num_str[0] == '0':
                continue
            w2_num = int(w2_num_str)
            if isqrt(w2_num) ** 2 == w2_num:
                best_square = max(best_square, sq, w2_num)
    
    return best_square

if __name__ == "__main__":
    print(solve())
