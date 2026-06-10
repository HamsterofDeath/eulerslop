import math

def f(x):
    val = 2 ** (30.403243784 - x*x)
    return math.floor(val) * 1e-9

def solve():
    u = -1.0
    for _ in range(1000):
        u = f(u)
    # The sum of two consecutive terms
    u_next = f(u)
    print(u + u_next)

if __name__ == "__main__":
    solve()
