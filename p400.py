#!/usr/bin/env python3

def solve():
    # Fibonacci tree game: removing a node deletes its whole subtree; whoever
    # must take the overall root loses.  Taking the root voluntarily is an
    # immediate loss, so the game is normal play on the forest below the root:
    # the player left with only the root (no move) loses.
    #
    # For this tree-pruning poset game the Grundy value of a rooted tree is
    #   g(tree) = 1 + XOR(g(child) for each child)
    # (verified by brute-force mex search on small random trees: the "+1"
    # accounts for the removable root, the XOR for the independent child
    # subtrees).  Since T(k)'s root has children T(k-1) and T(k-2):
    #   G[0]=0, G[1]=1, G[k] = 1 + (G[k-1] ^ G[k-2]).
    #
    # A first move removes a node v from one of the root's child trees
    # A=T(K-1), B=T(K-2); it wins iff the remaining forest has XOR 0, i.e.
    # g(A') == G[K-2] or g(B') == G[K-1].  Let C(k,t) = number of nodes v in
    # T(k) whose removal leaves a tree of Grundy value t.  Removing the root
    # leaves the empty tree (t=0); removing v inside child A=T(k-1) gives
    # 1 + (g(A') ^ G[k-2]) = t, i.e. g(A') = (t-1) ^ G[k-2], and symmetrically
    # for B.  Hence
    #   C(0,t) = 0,  C(1,t) = [t==0],  C(k,0) = 1,
    #   C(k,t) = C(k-1, (t-1)^G[k-2]) + C(k-2, (t-1)^G[k-1])   (t >= 1)
    # and f(K) = C(K-1, G[K-2]) + C(K-2, G[K-1]).
    #
    # Grundy values stay small (max 8191 for k < 10000), so we first propagate
    # the set of needed t values downward, then fill C bottom-up mod 10^18.
    K = 10000
    MOD = 10 ** 18

    G = [0, 1]
    for k in range(2, K):
        G.append(1 + (G[-1] ^ G[-2]))

    def f(K):
        if K <= 1:
            return 0
        need = [set() for _ in range(K)]
        need[K - 1].add(G[K - 2])
        need[K - 2].add(G[K - 1])
        for k in range(K - 1, 1, -1):
            for t in need[k]:
                if t >= 1:
                    need[k - 1].add((t - 1) ^ G[k - 2])
                    need[k - 2].add((t - 1) ^ G[k - 1])
        C = [dict() for _ in range(K)]
        for t in need[0]:
            C[0][t] = 0
        for t in need[1]:
            C[1][t] = 1 if t == 0 else 0
        for k in range(2, K):
            Ck, C1, C2 = C[k], C[k - 1], C[k - 2]
            g2, g1 = G[k - 2], G[k - 1]
            for t in need[k]:
                Ck[t] = 1 if t == 0 else (C1[(t - 1) ^ g2] + C2[(t - 1) ^ g1]) % MOD
        return (C[K - 1][G[K - 2]] + C[K - 2][G[K - 1]]) % MOD

    assert f(5) == 1 and f(10) == 17  # test values from the statement
    return f(K)


if __name__ == "__main__":
    print(solve())
