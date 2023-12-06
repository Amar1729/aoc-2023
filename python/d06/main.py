#! /usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path
from pprint import pprint



def parse(fname: str) -> list[str]:
    """Read from data file. Returns problem specific formatted data."""
    with Path(fname).open() as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    time = [int(x) for x in lines[0].split(":")[1].split(" ") if x.strip()]
    distance = [int(x) for x in lines[1].split(":")[1].split(" ") if x.strip()]

    return list(zip(time, distance))


def good_distance(time: int, distance: int):
    found = False
    for t in range(time):
        tot = t * (time - t)
        if tot > distance:
            found = True
        yield tot > distance

        if found and tot < distance:
            break

    return


def part1(data: list[tuple[int, int]]) -> int:
    return math.prod(sum(good_distance(t, d)) for t, d in data)


def part2(data: list[str]) -> int:
    total = 0

    # todo

    return total


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(part1(data))
    # print(part2(data))
