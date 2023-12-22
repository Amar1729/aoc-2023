#! /usr/bin/env python3

from __future__ import annotations

import sys
import typing
from pathlib import Path
from pprint import pprint  # noqa: F401

import numpy as np


def parse(fname: str) -> list[str]:
    """Read from data file. Returns problem specific formatted data."""
    with Path(fname).open() as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    return np.array([[c for c in line] for line in lines])


def neighbors(p, dim = None) -> typing.Generator[tuple[int, int], None, None]:
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


def part2(data) -> int:
    print(data)
    return 0


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(part1(data))
    # print(part2(data))
