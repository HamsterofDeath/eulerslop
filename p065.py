#!/usr/bin/env python3

def solve():
    # Convergents of e: [2;1,2,1,1,4,1,1,6,1,1,8,1,1,...]
    # a[0]=2, a[1]=1, a[2]=2, a[3]=1, a[4]=1, a[5]=4, ...
    target = 100
    # Generate continued fraction terms for e
    terms = [2]
    for k in range(1, target):
        if k % 3 == 2:
            terms.append(2 * (k // 3 + 1))
        else:
            terms.append(1)

    # Compute convergent
    num_prev, num_cur = terms[0], terms[0] * terms[1] + 1
    den_prev, den_cur = 1, terms[1]

    for i in range(2, target):
        num_next = terms[i] * num_cur + num_prev
        den_next = terms[i] * den_cur + den_prev
        num_prev, num_cur = num_cur, num_next
        den_prev, den_cur = den_cur, den_next

    return sum(int(d) for d in str(num_cur))

if __name__ == "__main__":
    print(solve())
