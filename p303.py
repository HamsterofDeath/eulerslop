#!/usr/bin/env python3

def min_multiple_over_n(n):
    """Return f(n)//n where f(n) is the least positive multiple of n
    whose decimal digits are all <= 2.

    BFS over residues mod n, building the number digit by digit.  BFS explores
    candidates in increasing length, and within one length in increasing
    numeric order (queue is FIFO, digits tried in ascending order), so the
    first time residue 0 is reached we have the minimal multiple.  Each
    residue is visited at most once; digits are recovered via parent links.
    """
    visited = [False] * n
    prev = [0] * n    # parent residue
    pdig = [0] * n    # digit appended to reach this residue
    queue = []
    for d in (1, 2):  # leading digit must be nonzero
        r = d % n
        if not visited[r]:
            visited[r] = True
            prev[r] = -1
            pdig[r] = d
            queue.append(r)
    head = 0
    while not visited[0]:
        r = queue[head]
        head += 1
        base = r * 10
        for d in (0, 1, 2):
            nr = (base + d) % n
            if not visited[nr]:
                visited[nr] = True
                prev[nr] = r
                pdig[nr] = d
                queue.append(nr)
    # reconstruct digits of f(n) by walking back from residue 0
    digits = []
    r = 0
    while True:
        digits.append(pdig[r])
        if prev[r] == -1:
            break
        r = prev[r]
    f = int(''.join(map(str, reversed(digits))))
    return f // n

def solve():
    # f(10m) ends in 0, so f(10m) = 10*f(m) and f(10m)/(10m) = f(m)/m.
    ratios = {}
    total = 0
    for n in range(1, 10001):
        if n % 10 == 0:
            ratios[n] = ratios[n // 10]
        else:
            ratios[n] = min_multiple_over_n(n)
        total += ratios[n]
    return total

if __name__ == "__main__":
    print(solve())
