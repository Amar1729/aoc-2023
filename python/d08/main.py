#! /usr/bin/env python3

from __future__ import annotations

# commonly-used built-in imports. not all of these are necessarily used each day.
import math
import sys
from pathlib import Path
from pprint import pprint  # noqa: F401


def parse(fname: str) -> list[str]:
    """Read from data file. Returns problem specific formatted data."""
    with Path(fname).open() as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    directions = [c for c in lines[0]]

    return (directions, lines[1:])


def parse_node(s: str) -> tuple[str, tuple[str, str]]:
    src, dst = s.split(" = ")
    dst = dst.replace("(", "").replace(")", "")
    dl, dr = dst.split(", ")

    return (src, (dl, dr))


def part1(data, curr: str | None = None) -> int:
    mapp = {}
    for n in data[1]:
        src, dst = parse_node(n)
        mapp[src] = dst

    # curr = "AAA"
    # start_node is optionally specified (by p2)
    if not curr:
        # p1 default
        curr = "AAA"
        cond = lambda c: c == "ZZZ"  # noqa: E731
    else:
        # for p2
        cond = lambda c: c.endswith("Z")  # noqa: E731

    dirs = data[0]
    step = 0
    while not cond(curr):
        dir = dirs[step % len(dirs)]
        # print(dir, curr, mapp[curr], step)
        curr = mapp[curr][0] if dir == "L" else mapp[curr][1]
        step += 1

    return step


def part2(data) -> int:
    curr: set[str] = set()
    for n in data[1]:
        src, _ = parse_node(n)

        if src.endswith("A"):
            curr.update([src])

    # kind of gross forcing part1 to re-form the map each time but whatever
    steps = [part1(data, curr=p) for p in curr]
    return math.lcm(*steps)


if __name__ == "__main__":
    data = parse(sys.argv[1])

    # print(part1(data))
    print(part2(data))
