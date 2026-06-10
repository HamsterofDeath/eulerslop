#!/usr/bin/env python3

def cost(n):
    # Huffman-like greedy: start with one codeword (the empty string, cost 0)
    # and repeatedly split the cheapest leaf (cost c) into two children with
    # costs c+1 and c+4.  Each split adds one codeword and raises the total
    # cost by (c+1) + (c+4) - c = c + 5.  All leaves at the minimum cost
    # level are interchangeable, so they can be expanded in bulk.
    counts = {0: 1}  # cost level -> number of leaves at that level
    leaves = 1
    total = 0
    while leaves < n:
        m = min(counts)
        k = counts.pop(m)
        expand = min(k, n - leaves)
        total += expand * (m + 5)
        counts[m + 1] = counts.get(m + 1, 0) + expand
        counts[m + 4] = counts.get(m + 4, 0) + expand
        leftover = k - expand
        if leftover:
            counts[m] = leftover
        leaves += expand
    return total

def solve():
    assert cost(6) == 35
    return cost(10**9)

if __name__ == "__main__":
    print(solve())
