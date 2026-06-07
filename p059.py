#!/usr/bin/env python3
import urllib.request

def solve():
    url = "https://projecteuler.net/project/resources/p059_cipher.txt"
    with urllib.request.urlopen(url) as f:
        data = [int(n) for n in f.read().decode("utf-8").split(",")]

    # Try all 3-letter lowercase key combinations
    for a in range(ord('a'), ord('z') + 1):
        for b in range(ord('a'), ord('z') + 1):
            for c in range(ord('a'), ord('z') + 1):
                key = [a, b, c]
                decrypted = [data[i] ^ key[i % 3] for i in range(len(data))]
                text = "".join(chr(d) for d in decrypted)
                if " the " in text and " and " in text:
                    return sum(decrypted)
    return 0

if __name__ == "__main__":
    print(solve())
