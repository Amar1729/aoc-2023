#! /usr/bin/env python3

from __future__ import annotations

import math
import sys
from pathlib import Path
from pprint import pprint

# import numpy as np


def parse(fname: str, part2=False):
    """Read from data file. Returns problem specific formatted data."""
    with Path(fname).open() as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    if part2:
        time = lines[0].split(":")[1].replace(" ", "")
        distance = lines[1].split(":")[1].replace(" ", "")
        return int(time), int(distance)

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


def part2(data: tuple[int, int]) -> int:
    time, distance = data
    # couldn't get this to work nicely(?), but actually the naive solution isn't as slow as i feared.
    # ~ 5.5 sec
    # return np.roots([-1, time, -1 * distance])
    return sum(good_distance(time, distance))


if __name__ == "__main__":
    data = parse(sys.argv[1])

    # print(part1(data))
    print(part2(parse(sys.argv[1], True)))
