#!/usr/bin/env python3
import math


def gauss_legendre_nodes(n):
    nodes = [0.0] * n
    weights = [0.0] * n
    half = (n + 1) // 2

    for i in range(half):
        x = math.cos(math.pi * (i + 0.75) / (n + 0.5))
        while True:
            p0, p1 = 1.0, x
            for k in range(2, n + 1):
                p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
            derivative = n * (x * p1 - p0) / (x * x - 1.0)
            nxt = x - p1 / derivative
            if abs(nxt - x) < 1e-15:
                x = nxt
                break
            x = nxt

        nodes[i] = -x
        nodes[n - 1 - i] = x
        weight = 2.0 / ((1.0 - x * x) * derivative * derivative)
        weights[i] = weight
        weights[n - 1 - i] = weight

    return nodes, weights


def solve():
    # Put the hypotenuse on the base.  If a point sees that side under angle
    # theta, exactly theta/(2*pi) of all directions leave through it.
    alpha = math.asin(4.0 / 5.0)
    beta = math.asin(3.0 / 5.0)
    if alpha < beta:
        alpha, beta = beta, alpha
    gamma = alpha + beta

    sin_beta = math.sin(beta)

    def inner_angle_slice(u):
        # After changing variables to the two base angles phi, psi, only
        # u=phi+psi remains.  This is integral sin(phi)sin(u-phi)dphi over
        # the feasible interval for fixed u.
        if u <= beta:
            if u < 1e-3:
                u2 = u * u
                return u * u2 * (1.0 / 6.0 - u2 / 60.0 + u2 * u2 / 1680.0)
            return 0.5 * (math.sin(u) - u * math.cos(u))
        if u <= alpha:
            return 0.5 * (sin_beta * math.cos(u - beta) - beta * math.cos(u))

        lower = u - beta
        upper = alpha
        return (
            0.25 * (math.sin(2.0 * upper - u) - math.sin(2.0 * lower - u))
            - 0.5 * (upper - lower) * math.cos(u)
        )

    def integrand(u):
        sine = math.sin(u)
        return (math.pi - u) * inner_angle_slice(u) / (sine * sine * sine)

    nodes, weights = gauss_legendre_nodes(64)
    integral = 0.0
    for left, right in ((0.0, beta), (beta, alpha), (alpha, gamma)):
        middle = 0.5 * (left + right)
        radius = 0.5 * (right - left)
        integral += radius * sum(
            weight * integrand(middle + radius * node)
            for node, weight in zip(nodes, weights)
        )

    area_over_hypotenuse_squared = 0.5 * math.sin(alpha) * math.sin(beta)
    probability = integral / (area_over_hypotenuse_squared * 2.0 * math.pi)
    return f"{probability:.10f}"


if __name__ == "__main__":
    print(solve())
