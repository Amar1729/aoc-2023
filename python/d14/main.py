#! /usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path
from pprint import pprint  # noqa: F401
from typing import NamedTuple


class Point(NamedTuple):
    """Commonly-used grid math

    Yes i know about complex(), but with that you have to do int() casts all over
    to use imag or real components as indices.
    """
    x: int
    y: int

    # violates liskov substitution, since supertype NamedTuple has an __add__ method.
    # just ignore type error for this line.
    def __add__(self: Point, other: Point) -> Point:  # type: ignore[override]
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self: Point, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)


def parse(fname: str) -> list[str]:
    """Read from data file. Returns problem specific formatted data."""
    with Path(fname).open() as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    g = {}
    for y, row in enumerate(lines):
        for x, c in enumerate(row):
            if c in "#O":
                g[Point(x, y)] = c

    return g


def final_resting(g, p: Point) -> Point:
    # assumes y=0 as top
    curr = p
    for y in range(p.y, -1, -1):
        if Point(p.x, y) in g:
            break
        curr = Point(p.x, y)

    return curr


def calc(g) -> int:
    tot = 0
    for x in range(0, max(p.x for p in g) + 1):
        top_y = max(p.y for p in g)
        for row in range(top_y + 1):
            val = top_y - row + 1
            if g.get(Point(x, row), "") == "O":
                tot += val

    return tot


def part1(data) -> int:
    g = data

    new_g = {k: v for k, v in g.items() if v == "#"}
    for p in filter(lambda p: g[p] == "O", g):
        newp = final_resting(new_g, p)
        new_g[newp] = "O"

    return calc(new_g)


def part2(data) -> int:
    print(data)
    return 0


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(part1(data))
    # print(part2(data))
