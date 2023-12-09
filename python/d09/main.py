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


# yeah, i wrote this without ANY recursion, sue me
# tbh, it was probably slower to write without it - i only thought of it as
# recursive once i was halfway done typing it out anyway...
def diff_solve(l: list[int], part2=False) -> int:
    naive_lists = [l]
    while True:
        naive = [y - x for x, y in zip(l, l[1:])]
        naive_lists.append(naive)
        l = naive
        if all(n == 0 for n in naive):
            break

    if not part2:
        for down, up in zip(naive_lists[::-1], naive_lists[::-1][1:]):
            up.append(up[-1] + down[-1])

        return naive_lists[0][-1]

    # part2 solution: extrapolate beginning
    for down, up in zip(naive_lists[::-1], naive_lists[::-1][1:]):
        up.insert(0, up[0] - down[0])

    return naive_lists[0][0]


def part1(data) -> int:
    return sum(map(diff_solve, data))


def part2(data) -> int:
    return sum(map(lambda l: diff_solve(l, True), data))


if __name__ == "__main__":
    data = parse(sys.argv[1])

    # print(part1(data))
    print(part2(data))
