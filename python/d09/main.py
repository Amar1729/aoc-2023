#! /usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path
from pprint import pprint  # noqa: F401


def parse(fname: str) -> list[list[int]]:
    """Read from data file. Returns problem specific formatted data."""
    with Path(fname).open() as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    return [[int(i) for i in l.split(" ")] for l in lines]


def diff_solve(l: list[int]) -> int:
    naive_lists = [l]
    while True:
        naive = [y - x for x, y in zip(l, l[1:])]
        naive_lists.append(naive)
        l = naive
        if all(n == 0 for n in naive):
            break

    for down, up in zip(naive_lists[::-1], naive_lists[::-1][1:]):
        up.append(up[-1] + down[-1])

    return naive_lists[0][-1]


def part1(data) -> int:
    return sum(map(diff_solve, data))


def part2(data) -> int:
    print(data)
    return 0


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(part1(data))
    # print(part2(data))
