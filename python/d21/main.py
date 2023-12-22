#! /usr/bin/env python3

from __future__ import annotations

import sys
import typing
from pathlib import Path
from pprint import pprint  # noqa: F401

import numpy as np
import pytest


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


def part2_brute_force(data, steps: int = 65 + 100 * 131 * 2023) -> int:
    """Use this to test updating numbers for our _corrected_ sample (see test method)."""
    # steps = 26501365

    start = tuple(np.argwhere(data == "S")[0])

    rocks = {(t[0], t[1]) for t in np.argwhere(data == "#")}
    dim = data.shape

    q = set([start])

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

    return len(q)


def part2_algebraic(data, steps: int = 65 + 100 * 131 * 2023) -> int:
    """Is there a closed-form algebraic solution to this?"""
    # steps = 26501365
    return 0


def part2(data, steps: int = 65 + 100 * 131 * 2023) -> int:
    """Possibly, attempt a solution w/ cycle detection + tracking of grid squares?"""
    # steps = 26501365

    # nothing yet, still spinning wheels.
    print(data)
    return 0


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
    ],
)
def test_sample(sample: str, steps: int, expected: int) -> None:
    """Test numbers for original sample as well as corrected sample.

    The input data has a very important and unspecified property: there are no rocks on the same
    column/row as S. This means that the max distance the elf can reach away from S can be
    determined algebraically, which i'm thinking can then be used to inform a counting solution.

    I checked that these numbers were correct with guess-and-check via a working brute force soln.
    """
    data = parse(sample)
    assert expected == part2_brute_force(data, steps)


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(part1(data))
    # print(part2(data))
