#! /usr/bin/env python3

from __future__ import annotations

# commonly-used built-in imports. not all of these are necessarily used each day.
import collections
import itertools
import sys
from pathlib import Path
from pprint import pprint  # noqa: F401

import numpy as np


def parse(fname: str) -> list[str]:
    """Read from data file. Returns problem specific formatted data."""
    with Path(fname).open() as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    return np.array([[c for c in line] for line in lines])


def new_p(p: tuple[int, int], d: int) -> tuple[int, int]:
    if d == 0:
        return (p[0], p[1] + 1)
    if d == 1:
        return (p[0] + 1, p[1])
    if d == 2:
        return (p[0], p[1] - 1)
    if d == 3:
        return (p[0] - 1, p[1])
    raise ValueError


def beam_tracer(h):
    # y, x because of numpy parse
    c = collections.Counter()

    # right, down, left, up : 0, 1, 2, 3
    curr: list[tuple[tuple[int, int], int]] = [((0, 0), 0)]

    while curr:
        p, d = curr.pop(0)
        new_curr = []

        # TODO: possible for part 2: actually count how many times a tile gets energized?
        if (p, d) in c:
            continue

        y, x = p
        if y < 0 or y >= h.shape[0] or x < 0 or x >= h.shape[1]:
            continue

        match h[p], d:
            case ".", _:
                newp = new_p(p, d)
                new_curr.append((newp, d))

            case "|", (0 | 2):
                new_curr.extend([
                    (new_p(p, 1), 1),
                    (new_p(p, 3), 3),
                ])
            case "|", (1 | 3):
                newp = new_p(p, d)
                new_curr.append((newp, d))

            case "-", (1 | 3):
                new_curr.extend([
                    (new_p(p, 0), 0),
                    (new_p(p, 2), 2),
                ])
            case "-", (0 | 2):
                newp = new_p(p, d)
                new_curr.append((newp, d))

            case "/", 0:
                new_curr.append((new_p(p, 3), 3))
            case "/", 1:
                new_curr.append((new_p(p, 2), 2))
            case "/", 2:
                new_curr.append((new_p(p, 1), 1))
            case "/", 3:
                new_curr.append((new_p(p, 0), 0))

            case "\\", 0:
                new_curr.append((new_p(p, 1), 1))
            case "\\", 1:
                new_curr.append((new_p(p, 0), 0))
            case "\\", 2:
                new_curr.append((new_p(p, 3), 3))
            case "\\", 3:
                new_curr.append((new_p(p, 2), 2))

        c[(p, d)] += 1
        for (p, d) in new_curr:
            # print(p, d)
            curr.append((p, d))

    return c


def debug(arr, c):
    for k in c:
        arr[k] = "#"

    print(arr)


def part1(data) -> int:
    d = beam_tracer(data)
    return len(set(k for k, _ in d))


def part2(data) -> int:
    print(data)
    return 0


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(part1(data))
    # print(part2(data))
