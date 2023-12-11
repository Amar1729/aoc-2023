#! /usr/bin/env python3

from __future__ import annotations

import itertools
import sys
import typing
from pathlib import Path
from pprint import pprint  # noqa: F401


class Point(typing.NamedTuple):
    x: int
    y: int


def parse(fname: str) -> set[Point]:
    """Read from data file. Returns problem specific formatted data."""
    with Path(fname).open() as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    points = set()

    for x, line in enumerate(lines):
        for y, c in enumerate(line):
            if c == "#":
                points.add(Point(x, y))
    return points


def expand_universe(points: set[Point], step: int=2) -> set[Point]:
    old_points = points
    new_points: set[Point] = set()
    empty_rows = set(range(max(p.x for p in points))) - set([p.x for p in points])
    for row in sorted(empty_rows, reverse=True):
        new_points = set()
        for point in old_points:
            if point.x > row:
                new_points.add(Point(point.x + step - 1, point.y))
            else:
                new_points.add(point)
        old_points = new_points

    empty_cols = set(range(max(p.y for p in old_points))) - set([p.y for p in old_points])
    for col in sorted(empty_cols, reverse=True):
        new_points = set()
        for point in old_points:
            if point.y > col:
                new_points.add(Point(point.x, point.y + step - 1))
            else:
                new_points.add(point)
        old_points = new_points

    return new_points


def distance(p1: Point, p2: Point) -> int:
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def part1(data) -> int:
    points = expand_universe(data)

    return sum(
        distance(p1, p2)
        for p1, p2 in itertools.combinations(points, 2)
    )


def part2(data) -> int:
    points = expand_universe(data, step=1_000_000)

    return sum(
        distance(p1, p2)
        for p1, p2 in itertools.combinations(points, 2)
    )


if __name__ == "__main__":
    data = parse(sys.argv[1])

    # print(part1(data))
    print(part2(data))
