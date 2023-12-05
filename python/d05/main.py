#! /usr/bin/env python3

from __future__ import annotations

# commonly-used built-in imports. not all of these are necessarily used each day.
import sys
import typing
from pathlib import Path
from pprint import pprint

# see parent directory
# from aoc_tools import *


class Interval(typing.NamedTuple):
    dst: int
    src: int
    range_: int


def parse_lazy(fname: str) -> tuple[set[int], list[list[Interval]]]:
    with Path(fname).open() as f:
        chunks = f.read().split("\n\n")

    seeds = set(list(map(int, chunks[0].split(": ")[1].split(" "))))

    transforms = []

    for chunk in chunks[1:]:
        transform = []
        for line in chunk.split("\n")[1:]:
            if not line.strip():
                continue
            dst, src, r = list(map(int, line.split(" ")))
            transform.append(Interval(dst, src, r))
        transforms.append(transform)

    return seeds, transforms


def calc_seed(s: int, transforms) -> int:
    for chunk in transforms:

        for chunk_t in chunk:
            if s in range(chunk_t.src, chunk_t.src + chunk_t.range_):
                # print(f"Found {s} in chunk: {chunk_t}")
                s = (s - chunk_t.src) + chunk_t.dst
                break

    return s


def part1(data: list[str]) -> int:
    seeds, transforms = data
    return min(calc_seed(s, transforms) for s in seeds)


def part2(data: list[str]) -> int:
    total = 0

    # todo

    return total


if __name__ == "__main__":
    data = parse_lazy(sys.argv[1])

    print(part1(data))
    # print(part2(data))
