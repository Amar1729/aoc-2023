#! /usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path
from pprint import pprint  # noqa: F401

D = {d: i for i, d in enumerate("RDLU")}
Point = tuple[int, int]


def parse(fname: str) -> list[str]:
    """Read from data file. Returns problem specific formatted data."""
    with Path(fname).open() as f:
        return [line.strip() for line in f.read().splitlines() if line.strip()]


def line_parse(line: str) -> tuple[int, int]:
    d, m, _ = line.split(" ")
    return D[d], int(m)


def true_line_parse(line: str) -> tuple[int, int]:
    _, _, s_hex = line.split(" ")
    s_hex = s_hex[2:-1]
    m = int(s_hex[:-1], 16)
    return int(s_hex[-1]), m


def find_vertices(lines: list[str], p2: bool = False) -> tuple[int, list[Point]]:
    vertices: list[Point] = [(0, 0)]

    perimeter = 0
    for d, m in map(true_line_parse if p2 else line_parse, lines):
        x, y = vertices[-1]
        match d:
            case 0:
                curr = (x + m, y)
            case 1:
                curr = (x, y + m)
            case 2:
                curr = (x - m, y)
            case 3:
                curr = (x, y - m)
            case _:
                raise ValueError

        perimeter += m
        vertices.append(curr)

    vertices.pop()
    return perimeter, vertices


def shoelace(vertices: list[Point]) -> int:
    # calculate the area of our shape
    s = 0
    for (x1, y1), (x2, y2) in zip(vertices, [*vertices[1:], vertices[0]]):
        s += (x1 * y2) - (y1 * x2)

    return abs(s) // 2


def picks(perimeter: int, vertices: list[Point]) -> int:
    # count points strictly inside our shape
    # A = i + b/2 - 1
    # i = points inside
    # b = points on perim
    return shoelace(vertices) + 1 - (perimeter // 2)


def part1(data: list[str]) -> int:
    # initially, i used a very naive approach of adding each point on the perimeter to a set,
    # then iterating over points outside the set to create a negative, then taking the length
    # of what was remaining. This was fast to implement, but clearly too slow for the magnitude
    # of numbers in part2. I'm going back and rewriting for consistency.
    perimeter, vertices = find_vertices(data)

    inside_area = picks(perimeter, vertices)

    # correct to include the points on the perimeter
    return inside_area + perimeter



def part2(data: list[str]) -> int:
    perimeter, vertices = find_vertices(data, p2=True)

    inside_area = picks(perimeter, vertices)

    # correct to include the points on the perimeter
    return inside_area + perimeter


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(part1(data))
    print(part2(data))
