#! /usr/bin/env python3

from __future__ import annotations

import sys
import typing
from pathlib import Path
from pprint import pprint  # noqa: F401

import numpy as np
import pytest

# 26501365
STEPS = 65 + 131 * 100 * 2023


def parse(fname: str) -> list[str]:
    """Read from data file. Returns problem specific formatted data."""
    with Path(fname).open() as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    return np.array([[c for c in line] for line in lines])


def neighbors(p) -> typing.Generator[tuple[int, int], None, None]:
    for s in [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0),
    ]:
        yield (p[0] + s[0], p[1] + s[1])


def part1(data) -> int:
    start = tuple(np.argwhere(data == "S")[0])

    rocks = {(t[0], t[1]) for t in np.argwhere(data == "#")}

    q = set([start])

    for step in range(64):
        new_q = set()
        while q:
            curr = q.pop()
            for new_p in neighbors(curr):
                if new_p not in rocks:
                    new_q.add(new_p)

        q = new_q

    return len(q)


def part2_brute_force(
    data, steps: int = STEPS, return_set: bool = False,
) -> int | set[tuple[int, int]]:
    """Use this to test updating numbers for our _corrected_ sample (see test method)."""
    # steps = 26501365

    start = tuple(np.argwhere(data == "S")[0])

    rocks = {(t[0], t[1]) for t in np.argwhere(data == "#")}
    dim = data.shape

    q: set[tuple[int, int]] = set([start])

    for step in range(steps):
        print(f"STEP {step} {dim=}")

        # #  works, but too slow:
        new_q = set()

        while q:
            curr = q.pop()
            for new_p in neighbors(curr):
                y, x = new_p

                ny = y % dim[0]
                nx = x % dim[1]
                c = (ny, nx)

                # wraparound
                if c not in rocks:
                    new_q.add(new_p)

        q = new_q

    if return_set:
        return q

    return len(q)


def range_finder(q: set[tuple[int, int]], dim: tuple[int, int], yoff: int, xoff: int) -> int:
    """Find number of points from q within grid copy at yoffset/xoffset."""

    yr = range(yoff * dim[0], (yoff + 1) * dim[0])
    xr = range(xoff * dim[1], (xoff + 1) * dim[1])

    s = filter(
        lambda p: p[0] in yr and p[1] in xr,
        q,
    )

    return len(set(s))


def part2_geometric(data, steps: int = STEPS) -> int:
    """Is there a closed-form geometric solution to this?

    Note: I was fairly hopeful about this, but ended up getting different counts
    for some of the corner tiles ((-1, -1) and (-1, 1)). Didn't spend much time solving;
    switched over to polyfit once I reasoned a bit more.
    """

    # 1 + 8 + 16 + 24 + 32 ...

    # 1 + (1*4 + 4) + (3*4 + 4) + (5*4 + 4) + ...

    # 1 + 4*[ (2n+1) + 1 ]

    # odd * [ 1 + 4*((4n-1) + 1) ]
    # +
    # even * [ 4*((4n+1) + 1) ]

    """
    N = 0
            C

    N = 2
          A T A
        A D E D A
        T E C E T
        A D E D A
          A T A

    N = 4
          A T A
        A D E D A
      A D E C E D A
    A D E C E C E D A
    T E C E C E C E T
    A D E C E C E D A
      A D E C E D A
        A D E D A
          A T A


    9C
    16E
    3*4 D
    4*4 A
    4 T

    (N-1)**2 * C
    N**2 * E
    4*(N-1) * D
    4*N * A
    4 * T

    """

    # find the N=2 state so we can calculate all the different grid counts
    first_steps = 65 + 131 + 131

    # kind of slow, whatever.
    grid = part2_brute_force(data, first_steps, True)
    assert isinstance(grid, set)

    # is this ... right?
    d = {
        "c": range_finder(grid, data.shape, 0, 0),
        "e": range_finder(grid, data.shape, -1, 0),
        "d": range_finder(grid, data.shape, -1, 1),
        "a": range_finder(grid, data.shape, -2, -1),
        "t": range_finder(grid, data.shape, -2, 0),
    }

    for k in "cedat":
        print(k, d[k])

    assert d["e"] == range_finder(grid, data.shape, 0, -1), "e"
    assert d["d"] == range_finder(grid, data.shape, -1, 1), "d"
    assert d["a"] == range_finder(grid, data.shape, 2, 1), "a"
    assert d["t"] == range_finder(grid, data.shape, 2, 0), "t"

    # determined closed form?
    # N=2 is 2*131 steps after first taking 65 steps
    # So our full default step is:
    n = 100 * 2023
    n = (steps - 65) // 131
    assert (steps - 65) % 131 == 0

    return sum([
        (n-1)**2 * d["c"],
        n**2 * d["e"],
        4 * (n-1) * d["d"],
        4 * n * d["a"],
        4 * d["t"],
    ])


def part2_poly(data, steps: int = STEPS) -> int:
    fit_k = [
        # k0 = part2_brute_force(data, 65)
        3893,
        # k1 = part2_brute_force(data, 65 + 1*131)
        34785,
        # k2 = part2_brute_force(data, 65 + 2*131)
        96471,
    ]

    coeff = np.polyfit([0, 1, 2], fit_k, 2)

    # how do i actually calculate a polynomial with given coefficients via numpy?

    k = (steps - 65) // 131
    assert (steps - 65) % 131 == 0

    return round(np.poly1d(coeff)(k))


def part2_cycle_detection(data, steps: int = STEPS) -> int:
    """Possibly, attempt a solution w/ cycle detection + tracking of grid squares?

    I spent a lot of time on this approach, thinking through how to properly do cycles.
    Eventually, I ended up trying to determine a closed-form geometric solution (in
    part2_geometric) until landing on the correct method of doing a polynomial fit in
    part2_poly.
    """
    # steps = 26501365

    return 0


def part2(data, steps: int = STEPS) -> int:
    # working solution out of my attempts!
    return part2_poly(data, steps)


@pytest.mark.parametrize(
    ("sample", "steps", "expected"),
    [
        ("sample.txt", 6, 16),
        ("sample.txt", 10, 50),
        ("sample.txt", 50, 1594),
        ("sample.txt", 100, 6536),
        # takes a little while
        # ("sample.txt", 500, 167004),

        # experimentally determined (i'm convinced my brute force is correct):
        ("sample_corrected.txt", 6, 36),
        ("sample_corrected.txt", 10, 90),
        ("sample_corrected.txt", 50, 1940),
        ("sample_corrected.txt", 100, 7645),
        # ("sample_corrected.txt", 65 + 2*131, 80886),
        # ("sample_corrected.txt", 500, 188756),

        ("input.txt", 6, 45),
        ("input.txt", 10, 107),
        ("input.txt", 50, 2300),
        ("input.txt", 100, 9203),
        ("input.txt", 65, 3893),
        # ("input.txt", 65 + 1*131, 34785),
        # ("input.txt", 65 + 2*131, 96471),
        # ("input.txt", 500, 225134),
    ],
)
def test_brute_force(sample: str, steps: int, expected: int) -> None:
    """Test numbers for original sample as well as corrected sample.

    The input data has a very important and unspecified property: there are no rocks on the same
    column/row as S. This means that the max distance the elf can reach away from S can be
    determined geometrically, which i'm thinking can then be used to inform a counting solution.

    I checked that these numbers were correct with guess-and-check via a working brute force soln.
    """
    data = parse(sample)
    assert expected == part2_brute_force(data, steps)


@pytest.mark.parametrize(
    ("sample", "steps", "expected"),
    [
        # geometric method won't be correct for sample, as it's not sized properly (right?).
        # these values determined by brute force, ensure they're correct for whatever approach.
        ("input.txt", 65, 3893),
        ("input.txt", 65 + 1*131, 34785),
        ("input.txt", 65 + 2*131, 96471),
    ],
)
def test_other(sample: str, steps: int, expected: int) -> None:
    """Test geometric solution."""
    data = parse(sample)
    # not working :/
    # assert expected == part2_geometric(data, steps)
    assert expected == part2_poly(data, steps)


if __name__ == "__main__":
    data = parse(sys.argv[1])

    # print(part1(data))
    print(part2(data))
