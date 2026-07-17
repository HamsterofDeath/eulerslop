#!/usr/bin/env python3
"""Project Euler 883: remarkable triangles on a hexagonal lattice."""

from pathlib import Path

from _cpp_runner import run_cpp


TWICE_RADIUS = 2_000_000


def triangle_count(twice_radius: int) -> int:
    return int(
        run_cpp(
            Path(__file__).with_suffix(".cpp"),
            (twice_radius,),
        ).strip()
    )


def solve() -> int:
    assert triangle_count(1) == 2
    assert triangle_count(4) == 44
    assert triangle_count(20) == 1_302
    return triangle_count(TWICE_RADIUS)


if __name__ == "__main__":
    print(solve())
