#!/usr/bin/env python3

def build_automaton(patterns):
    # Aho-Corasick over digit strings: returns transition table and terminal flags.
    children = [{}]
    term = [False]
    for pat in patterns:
        s = 0
        for ch in pat:
            d = int(ch)
            if d not in children[s]:
                children.append({})
                term.append(False)
                children[s][d] = len(children) - 1
            s = children[s][d]
        term[s] = True
    # BFS fail links, fold terminal status down fail chains, build full table
    n = len(children)
    fail = [0] * n
    trans = [[0] * 10 for _ in range(n)]
    queue = list(children[0].values())
    for d, c in children[0].items():
        trans[0][d] = c
    i = 0
    while i < len(queue):
        s = queue[i]
        i += 1
        term[s] = term[s] or term[fail[s]]
        for d in range(10):
            c = children[s].get(d)
            if c is None:
                trans[s][d] = trans[fail[s]][d]
            else:
                fail[c] = trans[fail[s]][d]
                trans[s][d] = c
                queue.append(c)
    return trans, term


def make_counter(max_digits):
    # patterns: powers of 11 (>= 11) that could fit in max_digits digits
    pats = []
    p = 11
    while len(str(p)) <= max_digits:
        pats.append(str(p))
        p *= 11
    trans, term = build_automaton(pats)
    n_states = len(trans)

    def count(x):
        # number of eleven-free integers in [1, x]; pad with leading zeros
        # (no pattern starts with '0', so padding never creates/destroys a match)
        digits = [int(ch) for ch in str(x).zfill(max_digits)]
        free = [0] * n_states  # prefix counts for already-below-x numbers
        tight_state, tight_ok = 0, True
        for d0 in digits:
            new = [0] * n_states
            for st, cnt in enumerate(free):
                if cnt:
                    row = trans[st]
                    for d in range(10):
                        ns = row[d]
                        if not term[ns]:
                            new[ns] += cnt
            if tight_ok:
                row = trans[tight_state]
                for d in range(d0):
                    ns = row[d]
                    if not term[ns]:
                        new[ns] += 1
                tight_state = row[d0]
                if term[tight_state]:
                    tight_ok = False
            free = new
        return sum(free) + (1 if tight_ok else 0) - 1  # drop the all-zero number

    return count


def solve():
    count = make_counter(20)
    # sanity checks from the statement
    assert count(3) == 3 and count(213) == 200 and count(531563) == 500000
    assert count(212) == 199 and count(531562) == 499999

    n = 10 ** 18
    # binary search smallest x with count(x) == n; that x is eleven-free
    lo, hi = n, 2 * n
    assert count(hi) >= n
    while lo < hi:
        mid = (lo + hi) // 2
        if count(mid) >= n:
            hi = mid
        else:
            lo = mid + 1
    return lo

if __name__ == "__main__":
    print(solve())
