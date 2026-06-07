#!/usr/bin/env python3

def solve():
    pent = {n * (3 * n - 1) // 2 for n in range(1, 5000)}
    pent_list = sorted(pent)
    for j in range(len(pent_list)):
        pj = pent_list[j]
        for k in range(j + 1, len(pent_list)):
            pk = pent_list[k]
            if pk - pj in pent and pk + pj in pent:
                return pk - pj
    return 0

if __name__ == "__main__":
    print(solve())
