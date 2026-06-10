#!/usr/bin/env python3

A = ("14159265358979323846264338327950288419716939937510"
     "58209749445923078164062862089986280348253421170679")
B = ("82148086513282306647093844609550582231725359408128"
     "48111745028410270193852110555964462294895493038196")


def solve():
    # F_{A,B} = (A, B, AB, BAB, ABBAB, ...), each term = previous + current
    # i.e. F(n) = F(n-2) + F(n-1). Track lengths only.
    lengths = [len(A), len(B)]
    max_needed = (127 + 19 * 17) * 7 ** 17
    while lengths[-1] < max_needed:
        lengths.append(lengths[-2] + lengths[-1])

    def digit(k):
        # k is 1-indexed position; find first term with length >= k
        i = 0
        while lengths[i] < k:
            i += 1
        # descend the tree: F(i) = F(i-2) + F(i-1)
        while i >= 2:
            if k <= lengths[i - 2]:
                i -= 2
            else:
                k -= lengths[i - 2]
                i -= 1
        return int(A[k - 1]) if i == 0 else int(B[k - 1])

    total = 0
    for n in range(18):
        total += 10 ** n * digit((127 + 19 * n) * 7 ** n)
    return total


if __name__ == "__main__":
    print(solve())
