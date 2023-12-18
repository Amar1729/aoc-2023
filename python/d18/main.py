#! /usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path
from pprint import pprint  # noqa: F401


def parse(fname: str) -> list[str]:
    """Read from data file. Returns problem specific formatted data."""
    with Path(fname).open() as f:
        return [line.strip() for line in f.read().splitlines() if line.strip()]


def line_parse(line: str) -> tuple[str, int]:
    d, m, _ = line.split(" ")
    return d, int(m)


def true_line_parse(line: str) -> tuple[int, int]:
    _, _, s_hex = line.split(" ")
    s_hex = s_hex[2:-1]
    m = int(s_hex[:-1], 16)
    return int(s_hex[-1]), m


def find_vertices(lines: list[str], p2: bool=False) -> tuple[int, list[tuple[int, int]]]:
    vertices: list[tuple[int, int]] = [(0, 0)]

    perimeter = 0
    for (d, m) in map(true_line_parse if p2 else line_parse, lines):
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


def shoelace(vertices: list[tuple[int, int]]) -> int:
    # calculate the area of our shape
    s = 0
    for (x1, y1), (x2, y2) in zip(vertices, [*vertices[1:], vertices[0]]):
        s += (x1 * y2) - (y1 * x2)

    return abs(s) // 2


def picks(perimeter: int, vertices: list[tuple[int, int]]) -> int:
    # count points strictly inside our shape
    # A = i + b/2 - 1
    # i = points inside
    # b = points on perim
    return shoelace(vertices) + 1 - (perimeter // 2)


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
    perimeter, vertices = find_vertices(data, p2=True)

    inside_area = picks(perimeter, vertices)

    # correct to include the points on the perimeter
    return inside_area + perimeter


if __name__ == "__main__":
    data = parse(sys.argv[1])

    # print(part1(data))
    print(part2(data))
