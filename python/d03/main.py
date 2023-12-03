#! /usr/bin/env python3

# This solution was written on a friend's computer. Forgive my messiness.

import sys
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


def parse(fname: str):
    with open(fname) as f:
        lines = f.readlines()

    numbers = []
    grid = set()
    for y, line in enumerate(lines):
        n = ""
        for x, c in enumerate(line.strip()):
            if n and not c.isdigit():
                numbers.append((Point(x-1, y), int(n)))
                n = ""
                if c != ".":
                    grid.add(Point(x, y))
                continue

            if c == ".":
                continue
            if c.isdigit():
                n += c
                continue
            grid.add(Point(x, y))

        if n:
            # assumes x is not unbound
            numbers.append((Point(x, y), int(n)))
            n = ""

    return grid, numbers


def part1(fname: str) -> int:
    grid, numbers = parse(fname)

    def is_adj(n_len: int, point: Point) -> bool:
        points_around = set(
                Point(x, y)
                for x in range(point.x - n_len, point.x + 2)
                for y in range(point.y - 1, point.y + 2)
                )

        return bool( points_around.intersection(grid) )

    for p, num in numbers:
        x = is_adj(len(str(num)), p)
        print(p, num, x)

    return sum(
            elem[1] for elem in
            # check neighbors of each number
            filter(
                lambda elem: is_adj(len(str(elem[1])), elem[0]),
                numbers,
                )
            )


if __name__ == "__main__":
    print(part1(sys.argv[1]))
    # part2(data)
