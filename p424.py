"""Project Euler 424: Kakuro (cross sums) with letter-encrypted clues.

Each puzzle maps letters A-J bijectively to digits 0-9. Solve each puzzle
with constraint propagation (bitmask domains for cells and letters,
sum-combination pruning per run) plus MRV backtracking. A puzzle's answer
is the 10-digit number formed by the digits of A..J in alphabetical order.
"""
import re
from itertools import combinations
from pathlib import Path

# digit-set combinations per (run length, sum): bitmasks over digits 1-9
COMBOS = {}
for _k in range(1, 10):
    for _c in combinations(range(1, 10), _k):
        _m = 0
        for _d in _c:
            _m |= 1 << _d
        COMBOS.setdefault((_k, sum(_c)), []).append(_m)


def bits(m):
    # yield indices of set bits
    while m:
        b = m & -m
        yield b.bit_length() - 1
        m ^= b


def propagate(ldom, cdom, runs, cell_letter):
    # fixpoint propagation; returns False on contradiction
    changed = True
    while changed:
        changed = False
        # letters form a bijection onto 0-9: singleton elimination
        for i in range(10):
            m = ldom[i]
            if not m:
                return False
            if m & (m - 1) == 0:
                for j in range(10):
                    if j != i and ldom[j] & m:
                        ldom[j] &= ~m
                        changed = True
        # a digit owned by exactly one letter is forced
        for d in range(10):
            b = 1 << d
            owner, cnt = -1, 0
            for i in range(10):
                if ldom[i] & b:
                    owner, cnt = i, cnt + 1
                    if cnt > 1:
                        break
            if cnt == 0:
                return False
            if cnt == 1 and ldom[owner] != b:
                ldom[owner] = b
                changed = True
        # white cells pre-filled with a letter equal that letter's digit
        for i, li in cell_letter.items():
            m = cdom[i] & ldom[li]
            if not m:
                return False
            if m != cdom[i]:
                cdom[i] = m
                changed = True
            if m != ldom[li]:
                ldom[li] = m
                changed = True
        # run constraints: distinct digits summing to the decoded clue
        for letters, cells in runs:
            k = len(cells)
            doms = [cdom[i] for i in cells]
            union = 0
            for d in doms:
                union |= d
            # candidate clue values from current letter domains
            if len(letters) == 1:
                cand = [(s, (s,)) for s in bits(ldom[letters[0]])]
            else:
                a, b = letters
                if a == b:
                    cand = [(11 * x, (x, x)) for x in bits(ldom[a]) if x]
                else:
                    cand = [(10 * x + y, (x, y))
                            for x in bits(ldom[a]) if x
                            for y in bits(ldom[b]) if y != x]
            new = [0] * k
            lall = [0] * len(letters)
            for s, lv in cand:
                ok = False
                for m in COMBOS.get((k, s), ()):
                    if m & union == m and all(d & m for d in doms):
                        ok = True
                        for t in range(k):
                            new[t] |= doms[t] & m
                if ok:
                    for t, v in enumerate(lv):
                        lall[t] |= 1 << v
            for t in range(k):
                if not new[t]:
                    return False
                if new[t] != doms[t]:
                    cdom[cells[t]] = new[t]
                    changed = True
            for t, li in enumerate(letters):
                m = ldom[li] & lall[t]
                if not m:
                    return False
                if m != ldom[li]:
                    ldom[li] = m
                    changed = True
            # no repeats within a run: singleton elimination
            for t in range(k):
                m = cdom[cells[t]]
                if m & (m - 1) == 0:
                    for u in range(k):
                        if u != t and cdom[cells[u]] & m:
                            cdom[cells[u]] &= ~m
                            if not cdom[cells[u]]:
                                return False
                            changed = True
    return True


def search(ldom, cdom, runs, cell_letter, white):
    ldom = ldom[:]
    cdom = dict(cdom)
    if not propagate(ldom, cdom, runs, cell_letter):
        return None
    # MRV branching: letters first, then cells
    best = None
    for i in range(10):
        c = ldom[i].bit_count()
        if c > 1 and (best is None or c < best[0]):
            best = (c, 'L', i)
    if best is None:
        for i in white:
            c = cdom[i].bit_count()
            if c > 1 and (best is None or c < best[0]):
                best = (c, 'C', i)
    if best is None:  # fully assigned and consistent
        return [next(bits(ldom[i])) for i in range(10)]
    _, kind, idx = best
    for v in bits(ldom[idx] if kind == 'L' else cdom[idx]):
        if kind == 'L':
            nl = ldom[:]
            nl[idx] = 1 << v
            res = search(nl, cdom, runs, cell_letter, white)
        else:
            nc = dict(cdom)
            nc[idx] = 1 << v
            res = search(ldom, nc, runs, cell_letter, white)
        if res is not None:
            return res
    return None


def solve_puzzle(line):
    n = int(line[0])
    toks = re.findall(r'\([^)]*\)|[A-JOX]', line[2:])
    assert len(toks) == n * n
    white = {i for i, t in enumerate(toks) if t != 'X' and not t.startswith('(')}
    cell_letter = {i: ord(toks[i]) - 65 for i in white if toks[i] != 'O'}
    runs = []
    for i, t in enumerate(toks):
        if not t.startswith('('):
            continue
        r, c = divmod(i, n)
        for part in t[1:-1].split(','):
            letters = [ord(ch) - 65 for ch in part[1:]]
            cells = []
            if part[0] == 'h':
                j = c + 1
                while j < n and r * n + j in white:
                    cells.append(r * n + j)
                    j += 1
            else:
                j = r + 1
                while j < n and j * n + c in white:
                    cells.append(j * n + c)
                    j += 1
            assert cells
            runs.append((letters, cells))
    ldom = [0b1111111111] * 10           # letters: digits 0-9
    cdom = {i: 0b1111111110 for i in white}  # cells: digits 1-9
    digits = search(ldom, cdom, runs, cell_letter, white)
    assert digits is not None
    return int(''.join(map(str, digits)))


def solve():
    path = Path(__file__).resolve().parent / "0424_kakuro200.txt"
    answers = [solve_puzzle(s) for s in path.read_text().split()]
    assert len(answers) == 200
    assert answers[0] == 8426039571          # example puzzle from the statement
    assert sum(answers[:10]) == 64414157580  # given check value
    return sum(answers)


if __name__ == "__main__":
    print(solve())
