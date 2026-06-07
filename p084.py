#!/usr/bin/env python3
import random

def solve():
    # Monopoly simulation with 4-sided dice
    # Squares: GO=0, A1=1, CC1=2, A2=3, T1=4, R1=5, B1=6, CH1=7, B2=8, B3=9,
    # JAIL=10, C1=11, U1=12, C2=13, C3=14, R2=15, D1=16, CC2=17, D2=18, D3=19,
    # FP=20, E1=21, CH2=22, E2=23, E3=24, R3=25, F1=26, F2=27, U2=28, F3=29,
    # G2J=30, G1=31, G2=32, CC3=33, G3=34, R4=35, CH3=36, H1=37, T2=38, H2=39

    square_names = ["GO", "A1", "CC1", "A2", "T1", "R1", "B1", "CH1", "B2", "B3",
                    "JAIL", "C1", "U1", "C2", "C3", "R2", "D1", "CC2", "D2", "D3",
                    "FP", "E1", "CH2", "E2", "E3", "R3", "F1", "F2", "U2", "F3",
                    "G2J", "G1", "G2", "CC3", "G3", "R4", "CH3", "H1", "T2", "H2"]

    CC = [2, 17, 33]
    CH = [7, 22, 36]
    R = [5, 15, 25, 35]
    U = [12, 28]

    def cc_card(pos):
        card = random.randint(1, 16)
        if card == 1:
            return 0  # GO
        elif card == 2:
            return 10  # JAIL
        return pos

    def ch_card(pos):
        card = random.randint(1, 16)
        if card == 1:
            return 0  # GO
        elif card == 2:
            return 10  # JAIL
        elif card == 3:
            return 11  # C1
        elif card == 4:
            return 24  # E3
        elif card == 5:
            return 39  # H2
        elif card == 6:
            return 5   # R1
        elif card in (7, 8):
            for r in R:
                if r > pos:
                    return r
            return R[0]
        elif card == 9:
            for u in U:
                if u > pos:
                    return u
            return U[0]
        elif card == 10:
            return (pos - 3) % 40
        return pos

    visits = [0] * 40
    pos = 0
    doubles = 0
    N = 2_000_000

    for _ in range(N):
        d1 = random.randint(1, 4)
        d2 = random.randint(1, 4)
        if d1 == d2:
            doubles += 1
            if doubles == 3:
                pos = 10
                doubles = 0
                visits[pos] += 1
                continue
        else:
            doubles = 0
        pos = (pos + d1 + d2) % 40
        if pos == 30:  # G2J
            pos = 10
        elif pos in CC:
            pos = cc_card(pos)
        elif pos in CH:
            pos = ch_card(pos)
        # Check if landed on CC/CH after card movement
        if pos == 30:
            pos = 10
        elif pos in CC:
            pos = cc_card(pos)
        elif pos in CH:
            pos = ch_card(pos)
        visits[pos] += 1

    # Get top 3 visited squares
    order = sorted(range(40), key=lambda i: visits[i], reverse=True)
    return int(f"{order[0]:02d}{order[1]:02d}{order[2]:02d}")

if __name__ == "__main__":
    random.seed(42)
    print(solve())
