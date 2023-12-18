#! /usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path
from pprint import pprint  # noqa: F401


def parse(fname: str) -> list[str]:
    """Read from data file. Returns problem specific formatted data."""
    with Path(fname).open() as f:
        return [line.strip() for line in f.read().splitlines() if line.strip()]


def debug(points):
    min_x = min(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_x = max(p[0] for p in points)
    max_y = max(p[1] for p in points)

    for y in range(min_y, max_y + 1):
        l = "".join(["#" if (x, y) in points else " " for x in range(min_x, max_x + 1)])
        print(l)


def part1(data) -> int:
    points = set()
    curr = (0, 0)
    points.add(curr)

    for line in data:
        d, m, col = line.split(" ")

        for i in range(int(m)):
            x, y = curr
            if d == "R":
                curr = (x + 1, y)
            if d == "D":
                curr = (x, y + 1)
            if d == "L":
                curr = (x - 1, y)
            if d == "U":
                curr = (x, y - 1)
            points.add(curr)

    min_x = min(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_x = max(p[0] for p in points)
    max_y = max(p[1] for p in points)

    # reverse floodfill
    outer_points = set([
        (x, y)
        for y in range(min_y - 1, max_y + 2)
        for x in range(min_x - 1, max_x + 2)
    ])

    curr = (min_x - 1, min_y - 1)
    outer_points -= set([curr])
    q = [curr]

    while q:
        curr = q.pop(0)
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            x, y = curr
            n = (x + dx, y + dy)
            if n in outer_points and n not in points:
                outer_points.remove(n)
                q.append(n)

    # debug(points)

    return len(outer_points)


def part2(data) -> int:
    print(data)
    return 0


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(part1(data))
    # print(part2(data))
