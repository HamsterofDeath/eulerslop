#!/usr/bin/env python3
import math
from decimal import Decimal, getcontext

def solve():
    # The optimum is symmetric in x -> -x and y -> -y, so work in the first
    # quadrant with gridlines 0 = x_0 < x_1 < ... < x_m < x_{m+1} = 1 where
    # m = N/2.  A cell is red iff its corner nearest the origin lies strictly
    # inside the circle, so column i (between x_i and x_{i+1}) is red up to
    # the lowest horizontal line >= g(x_i) with g(x) = sqrt(1 - x^2).  Given
    # the vertical lines, the optimal horizontal lines drop onto the circle:
    # y_{m+1-i} = g(x_i).  The red area is then 4*F(x) with
    #   F(x) = sum_{i=0}^{m} (x_{i+1} - x_i) * g(x_i),
    # a smooth convex-near-optimum function minimized by Newton's method;
    # its Hessian is tridiagonal, so each step is a Thomas solve.
    #   grad_k  = g(x_{k-1}) - g(x_k) + (x_{k+1} - x_k) g'(x_k)
    #   H[k][k] = -2 g'(x_k) + (x_{k+1} - x_k) g''(x_k)
    #   H[k][k+-1] = g'(x_min(k,k+-1)),  g' = -x/g,  g'' = -1/g^3.

    def newton_step(x, m, sqrt, zero, one, two):
        g = [sqrt(one - t * t) for t in x]
        gp = [-x[k] / g[k] for k in range(m + 1)]
        gpp = [-one / g[k] ** 3 for k in range(m + 1)]
        grad = [g[k - 1] - g[k] + (x[k + 1] - x[k]) * gp[k] for k in range(1, m + 1)]
        diag = [-two * gp[k] + (x[k + 1] - x[k]) * gpp[k] for k in range(1, m + 1)]
        off = [gp[k] for k in range(1, m)]  # H[k][k+1] = H[k+1][k]
        # Thomas algorithm for H * d = grad
        cp, dp = [zero] * m, [zero] * m
        cp[0] = off[0] / diag[0]
        dp[0] = grad[0] / diag[0]
        for i in range(1, m):
            den = diag[i] - off[i - 1] * cp[i - 1]
            if i < m - 1:
                cp[i] = off[i] / den
            dp[i] = (grad[i] - off[i - 1] * dp[i - 1]) / den
        d = [zero] * m
        d[m - 1] = dp[m - 1]
        for i in range(m - 2, -1, -1):
            d[i] = dp[i] - cp[i] * d[i + 1]
        return d

    def minimize(n_lines):
        m = n_lines // 2
        # float64 phase from a smooth initial guess (uniform in angle)
        x = [math.sin(i * math.pi / 2 / (m + 1)) for i in range(m + 2)]
        x[0], x[m + 1] = 0.0, 1.0
        for _ in range(60):
            d = newton_step(x, m, math.sqrt, 0.0, 1.0, 2.0)
            step = 1.0
            while True:  # damp to preserve 0 < x_1 < ... < x_m < 1
                xn = [0.0] + [x[k] - step * d[k - 1] for k in range(1, m + 1)] + [1.0]
                if all(xn[k] < xn[k + 1] for k in range(m + 1)):
                    break
                step /= 2
            x = xn
            if max(abs(t) for t in d) * step < 1e-15:
                break
        # high-precision polish (quadratic convergence: 3 steps suffice)
        getcontext().prec = 45
        one = Decimal(1)
        X = [Decimal(repr(t)) for t in x]
        X[0], X[m + 1] = Decimal(0), one
        for _ in range(3):
            d = newton_step(X, m, lambda t: t.sqrt(), Decimal(0), one, Decimal(2))
            for k in range(1, m + 1):
                X[k] -= d[k - 1]
        F = sum((X[i + 1] - X[i]) * (one - X[i] * X[i]).sqrt() for i in range(m + 1))
        return 4 * F

    # validate against the value given in the statement for N = 10
    assert str(minimize(10).quantize(Decimal("1.0000000000"))) == "3.3469640797"

    return minimize(400).quantize(Decimal("1.0000000000"))

if __name__ == "__main__":
    print(solve())
