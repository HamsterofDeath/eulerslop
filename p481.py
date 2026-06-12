#!/usr/bin/env python3


def _game(skills):
    n = len(skills)
    full = 1 << n
    wins = [None] * full
    dishes = [None] * full

    for i in range(n):
        mask = 1 << i
        w = [[0.0] * n for _ in range(n)]
        w[i][i] = 1.0
        wins[mask] = w
        dishes[mask] = [0.0] * n

    def next_alive(mask, p):
        q = (p + 1) % n
        while not (mask >> q) & 1:
            q = (q + 1) % n
        return q

    def solve_cycle(players, a, b):
        out = {}
        k = len(players)
        for start in range(k):
            term = 1.0
            const = 0.0
            for off in range(k):
                p = players[(start + off) % k]
                const += term * b[p]
                term *= a[p]
            out[players[start]] = const / (1 - term)
        return out

    for size in range(2, n + 1):
        for mask in range(full):
            if mask.bit_count() != size:
                continue
            players = [i for i in range(n) if (mask >> i) & 1]
            after_win = {}
            after_dishes = {}

            for p in players:
                # Tie order is the turn order starting with the next chef.
                order = []
                q = (p + 1) % n
                while q != p:
                    if (mask >> q) & 1:
                        order.append(q)
                    q = (q + 1) % n

                best = -1.0
                best_w = None
                best_e = None
                for victim in order:
                    nm = mask ^ (1 << victim)
                    q = next_alive(nm, p)
                    value = wins[nm][q][p]
                    if value > best + 1e-15:
                        best = value
                        best_w = wins[nm][q]
                        best_e = dishes[nm][q]
                after_win[p] = best_w
                after_dishes[p] = best_e

            cont = {p: 1 - skills[p] for p in players}
            wcur = [[0.0] * n for _ in range(n)]
            for winner in range(n):
                rhs = {p: skills[p] * after_win[p][winner] for p in players}
                sol = solve_cycle(players, cont, rhs)
                for p in players:
                    wcur[p][winner] = sol[p]

            ecur = [0.0] * n
            rhs = {p: 1 + skills[p] * after_dishes[p] for p in players}
            sol = solve_cycle(players, cont, rhs)
            for p in players:
                ecur[p] = sol[p]

            wins[mask] = wcur
            dishes[mask] = ecur

    return wins[full - 1][0], dishes[full - 1][0]


def _fib_skills(n):
    fib = [0, 1, 1]
    for _ in range(n):
        fib.append(fib[-1] + fib[-2])
    return [fib[i] / fib[n + 1] for i in range(1, n + 1)]


def solve():
    w3, _ = _game([0.25, 0.5, 1.0])
    assert round(w3[0], 5) == 0.29375
    w7, e7 = _game(_fib_skills(7))
    assert [round(x, 8) for x in w7] == [
        0.08965042, 0.20775702, 0.15291406, 0.14554098,
        0.15905291, 0.10261412, 0.14247050,
    ]
    assert round(e7, 8) == 42.28176050
    return f"{_game(_fib_skills(14))[1]:.8f}"


if __name__ == "__main__":
    print(solve())
