#! /usr/bin/env python3

from __future__ import annotations

import sys
from enum import Enum
from pathlib import Path
from pprint import pprint  # noqa: F401
from typing import NamedTuple


class Direction(Enum):
    N = 1
    W = 2
    S = 3
    E = 4


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


# set this for cycling
MAX_COORDS = []


def parse(fname: str) -> list[str]:
    """Read from data file. Returns problem specific formatted data."""
    with Path(fname).open() as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    g = {}
    for y, row in enumerate(lines):
        for x, c in enumerate(row):
            if c in "#O":
                g[Point(x, y)] = c

    # global state is gross, but speeds up bounds checking for moving stones later
    # (otherwise i have to keep calculating max coords from a dict, which is slow)
    MAX_COORDS.append(Point(x, y))

    return g


def final_resting(g, p: Point) -> Point:
    # assumes y=0 as top
    curr = p
    for y in range(p.y, -1, -1):
        if Point(p.x, y) in g:
            break
        curr = Point(p.x, y)

    return curr


def final_resting_cached(g, p: Point, d: Direction) -> Point:
    curr = p

    if d == Direction.N:
        for y in range(p.y, -1, -1):
            if Point(p.x, y) in g:
                break
            curr = Point(p.x, y)
        return curr

    if d == Direction.W:
        for x in range(p.x, -1, -1):
            if Point(x, p.y) in g:
                break
            curr = Point(x, p.y)
        return curr

    if d == Direction.S:
        # top_y = max(p.y for p in g) if g else 0
        top_y = MAX_COORDS[0].y
        for y in range(p.y, top_y + 1):
            if Point(p.x, y) in g:
                break
            curr = Point(p.x, y)
        return curr

    if d == Direction.E:
        # top_x = max(p.x for p in g) if g else 0
        top_x = MAX_COORDS[0].x
        for x in range(p.x, top_x + 1):
            if Point(x, p.y) in g:
                break
            curr = Point(x, p.y)
        return curr

    raise ValueError


def calc(g) -> int:
    tot = 0
    for x in range(0, max(p.x for p in g) + 1):
        top_y = max(p.y for p in g)
        for row in range(top_y + 1):
            val = top_y - row + 1
            if g.get(Point(x, row), "") == "O":
                # print(Point(x, row))
                tot += val

    return tot


def part1(data) -> int:
    g = data

    new_g = {k: v for k, v in g.items() if v == "#"}
    for p in filter(lambda p: g[p] == "O", g):
        newp = final_resting(new_g, p)
        new_g[newp] = "O"

    return calc(new_g)


def run_cycle(g):
    for d in Direction:
        new_g = {k: v for k, v in g.items() if v == "#"}
        it = filter(lambda p: g[p] == "O", g)
        it = sorted(it) if d in (Direction.N, Direction.W) else sorted(it, reverse=True)
        for p in it:
            newp = final_resting_cached(new_g, p, d)
            new_g[newp] = "O"

        g = new_g
    return g


def pretty_print(g):
    print("-" * 10)
    for y in range(max(p.y for p in g) + 1):
        s = (
            "|"
            + "".join([g.get(Point(x, y), " ") for x in range(max(p.x for p in g) + 1)])
            + "|"
        )
        print(s)
    print("-" * 10)


def hash_state(g) -> int:
    return hash(tuple(sorted(g.items())))


def part2(g) -> int:
    r = 1_000_000_000
    d = {}
    i = 0
    cycle_len = 0
    while i < r:
        h = hash_state(g)

        if h in d:
            print(f"Found prev state for {i}: {d[h][0]}")

            # sure there's NICE math i could do here, but where's the fun in that?
            g = d[h][1]
            cycle_len = i - d[h][0]
            dr = (r - cycle_len) // cycle_len
            i += dr * cycle_len
            while i > r:
                i -= cycle_len

            print(f"Iteration done at: {i}")
        else:
            g = run_cycle(g)
            d[h] = (i, g)

        i += 1

    return calc(g)


if __name__ == "__main__":
    data = parse(sys.argv[1])

    # print(part1(data))
    print(part2(data))
