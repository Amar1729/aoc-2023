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


def parse_lazy(fname: str) -> tuple[list[int], list[set[Interval]]]:
    with Path(fname).open() as f:
        chunks = f.read().split("\n\n")

    seeds = list(map(int, chunks[0].split(": ")[1].split(" ")))

    transforms = []

    for chunk in chunks[1:]:
        transform = set()
        for line in chunk.split("\n")[1:]:
            if not line.strip():
                continue
            dst, src, r = list(map(int, line.split(" ")))
            transform.add(Interval(dst, src, r))
        transforms.append(transform)

    return seeds, transforms


def calc_seed(s: int, transforms: list[set[Interval]]) -> int:
    for chunk in transforms:

        for chunk_t in chunk:
            if s in range(chunk_t.src, chunk_t.src + chunk_t.range_):
                # print(f"Found {s} in chunk: {chunk_t}")
                s = (s - chunk_t.src) + chunk_t.dst
                break

    return s


def part1(data: tuple[list[int], list[set[Interval]]]) -> int:
    seeds, transforms = data
    return min(calc_seed(s, transforms) for s in seeds)


def reverse_search(seed_ranges: Disjoint, transforms: list[set[Interval]]) -> int:
    def search_loc(i: int) -> bool:
        queue = set([i])
        for chunk in transforms[::-1]:
            new_queue = set()
            while queue:
                loc = queue.pop()
                found = False
                for chunk_t in chunk:
                    s = loc - chunk_t.dst + chunk_t.src
                    if s >= 0 and s in range(chunk_t.src, chunk_t.src + chunk_t.range_):
                        found = True
                        new_queue.add(s)
                        break
                if not found:
                    new_queue.add(loc)
            queue = new_queue

        return bool(queue) and any(s in seed_ranges for s in queue)

    loc = 0
    while True:
        if loc % 1_000_000 == 0:
            print(loc)
        if search_loc(loc):
            return loc
        loc += 1


class Disjoint:
    def __init__(self):
        self.ranges = []

    def update(self, start: int, range_: int) -> None:
        stop = start + range_ - 1

        if not self.ranges:
            self.ranges.append((start, stop))
            return

        for idx in range(len(self.ranges)):
            if (self.ranges[idx][0] <= stop <= self.ranges[idx][1]) or (
                self.ranges[idx][0] <= start <= self.ranges[idx][1]
            ):
                # if stop >= self.ranges[idx][0] or start <= self.ranges[idx][1]:
                nstart, nstop = self.ranges.pop(idx)
                min_start = min(start, nstart)
                max_stop = max(stop, nstop)
                max_range = max_stop - min_start + 1
                self.update(min_start, max_range)
                return

        self.ranges.append((start, start + range_ - 1))

    def __iter__(self):
        for start, stop in self.ranges:
            yield from range(start, stop + 1)

    def __contains__(self, s: int) -> bool:
        return any(s in range(start, stop + 1) for start, stop in self.ranges)


# naive solution only took 19min ... that's fine, right?
def part2(data: tuple[list[int], list[set[Interval]]]) -> int:
    seeds, transforms = data

    # weirdly, my input seemed to have no overlapping seeds
    # so this didn't help at all :/
    seed_ranges = Disjoint()
    for i in range(0, len(seeds), 2):
        seed_ranges.update(seeds[i], seeds[i+1])

    return reverse_search(seed_ranges, transforms)


if __name__ == "__main__":
    data = parse_lazy(sys.argv[1])

    # print(part1(data))
    print(part2(data))
