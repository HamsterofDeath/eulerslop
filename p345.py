#!/usr/bin/env python3

MATRIX = """
  7  53 183 439 863 497 383 563  79 973 287  63 343 169 583
627 343 773 959 943 767 473 103 699 303 957 703 583 639 913
447 283 463  29  23 487 463 993 119 883 327 493 423 159 743
217 623   3 399 853 407 103 983  89 463 290 516 212 462 350
960 376 682 962 300 780 486 502 912 800 250 346 172 812 350
870 456 192 162 593 473 915  45 989 873 823 965 425 329 803
973 965 905 919 133 673 665 235 509 613 673 815 165 992 326
322 148 972 962 286 255 941 541 265 323 925 281 601  95 973
445 721  11 525 473  65 511 164 138 672  18 428 154 448 848
414 456 310 312 798 104 566 520 302 248 694 976 430 392 198
184 829 373 181 631 101 969 613 840 740 778 458 284 760 390
821 461 843 513  17 901 711 993 293 157 274  94 192 156 574
 34 124   4 878 450 476 712 914 838 669 875 299 823 329 699
815 559 813 459 522 788 168 586 966 232 308 833 251 631 107
813 883 451 509 615  77 281 613 459 205 380 274 302  35 805
"""

def solve():
    # Maximum-weight assignment on a 15x15 matrix: pick one element per row,
    # all in distinct columns, maximizing the sum.  Bitmask DP: best[mask] is
    # the maximum sum using the first popcount(mask) rows with the column set
    # 'mask' already used.  O(2^15 * 15).
    m = [list(map(int, line.split())) for line in MATRIX.strip().splitlines()]
    n = len(m)
    NEG = float("-inf")
    best = [NEG] * (1 << n)
    best[0] = 0
    for mask in range(1 << n):
        if best[mask] == NEG:
            continue
        row = bin(mask).count("1")
        if row == n:
            continue
        for col in range(n):
            bit = 1 << col
            if not mask & bit:
                nv = best[mask] + m[row][col]
                if nv > best[mask | bit]:
                    best[mask | bit] = nv
    return best[(1 << n) - 1]

if __name__ == "__main__":
    print(solve())
