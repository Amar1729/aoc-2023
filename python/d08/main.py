#! /usr/bin/env python3

from __future__ import annotations

# commonly-used built-in imports. not all of these are necessarily used each day.
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


def part1(data) -> int:
    mapp = {}
    for n in data[1]:
        src, dst = parse_node(n)
        mapp[src] = dst

    curr = "AAA"
    dirs = data[0]
    step = 0
    while curr != "ZZZ":
        dir = dirs[step % len(dirs)]
        # print(dir, curr, mapp[curr], step)
        curr = mapp[curr][0] if dir == "L" else mapp[curr][1]
        step += 1

    return step


def part2(data) -> int:
    print(data)
    return 0


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(part1(data))
    # print(part2(data))
