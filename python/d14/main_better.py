#! /usr/bin/env python3

# numpy makes matrix manipulation a lot easier, didn't think of it when writing my initial impl :(
# another thing for debugging: numpy matrices basically have pretty-printing repr built-in


import sys
from pathlib import Path

import numpy as np


def parse(fname: str):
    with Path(fname).open() as f:
        return np.array([[*line.strip()] for line in f])


def shift_rocks(h):
    rocks = np.argwhere(h == "O")

    for col in set(r[1] for r in rocks):
        empty = []
        for y in range(h.shape[0]):
            p = (y, col)
            match h[p], bool(empty):
                case ".", _:
                    empty.append(p)
                case "#", _:
                    empty = []
                case "O", True:
                    # move this rock, if possible
                    h[empty.pop(0)] = "O"
                    empty.append(p)
                    h[p] = "."

    return h


def calc(h) -> int:
    return sum(
        rock[0] + 1
        for rock in np.argwhere(np.rot90(np.rot90(h)) == "O")
    )


def part1(data):
    return calc(shift_rocks(data))


def cycle(h):
    for _ in range(4):
        h = shift_rocks(h)
        h = np.rot90(h)
    return h


def part2(data):
    # for part2, cycle detection is basically the same as in ./main.py, just don't feel like
    # writing it out. (I might try to write it with a proper cycle detection alg?)
    # The point more is that doing a cycle with numpy is much easier than the horrible way
    # i did it on first pass.
    r = 1_000_000_000
    i = 0
    cycle_len = 0

    while i < r:
        data = cycle(data)
        i += 1

        # TODO
        break

    return calc(data)


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(part1(data))
    # print(part2(data))
