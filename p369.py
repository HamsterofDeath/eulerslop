#!/usr/bin/env python3

def solve():
    # A hand is fully described by the suit-subset S_r it holds at each of the
    # 13 ranks (card (r, s) present iff s in S_r).  It contains a Badugi iff
    # the bipartite graph ranks->suits with edges (r, s in S_r) has a matching
    # covering all 4 suits (4 cards, pairwise distinct ranks and suits).
    #
    # DP over the 13 ranks.  State M is a 16-bit mask: bit U is set iff some
    # partial matching using distinct ranks seen so far covers exactly the
    # suit set U.  Adding a rank with subset S either skips the rank (keep U)
    # or matches it to one suit s in S \ U (extend U).  M is downward closed,
    # so few states actually occur.  Track the card count, capped at 13 since
    # we only need hands of size n <= 13 (n >= 4 is automatic for a Badugi).
    RANKS, MAXN = 13, 13
    popcount = [bin(S).count("1") for S in range(16)]

    # precompute the state transition for each rank suit-subset S
    trans = {}

    def step(M, S):
        key = (M, S)
        if key not in trans:
            NM = M
            for U in range(16):
                if M >> U & 1:
                    for s in range(4):
                        if S >> s & 1 and not U >> s & 1:
                            NM |= 1 << (U | 1 << s)
            trans[key] = NM
        return trans[key]

    dp = {(1, 0): 1}  # only the empty suit set is matchable; 0 cards held
    for _ in range(RANKS):
        ndp = {}
        for (M, c), cnt in dp.items():
            for S in range(16):
                nc = c + popcount[S]
                if nc > MAXN:
                    continue
                key = (step(M, S), nc)
                ndp[key] = ndp.get(key, 0) + cnt
        dp = ndp

    # bit 15 set <=> all four suits matched <=> hand contains a Badugi
    return sum(cnt for (M, c), cnt in dp.items() if M >> 15 & 1)

if __name__ == "__main__":
    print(solve())
