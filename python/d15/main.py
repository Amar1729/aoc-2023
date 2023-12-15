#! /usr/bin/env python3

from __future__ import annotations

import math
import sys
from pathlib import Path
from pprint import pprint  # noqa: F401


def parse(fname: str) -> list[str]:
    """Read from data file. Returns problem specific formatted data."""
    with Path(fname).open() as f:
        return [line.strip() for line in f.read().splitlines() if line.strip()]


def calc(s: str) -> int:
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h = h % 256
    return h


def part1(data: list[str]) -> int:
    return sum(calc(s) for s in data[0].split(","))


def part2(data: list[str]) -> int:
    arr: list[list[tuple[str, int]]] = [[] for _ in range(256)]
    for s in data[0].split(","):
        if "-" in s:
            box_id = s.replace("-", "")
            lens = None
            box = calc(box_id)

            remove = None
            for idx, (label, _) in enumerate(arr[box]):
                if label == box_id:
                    remove = idx
            if remove is not None:
                arr[box].pop(remove)

        # if "=" in s:
        else:
            box_id, _lens = s.split("=")
            lens = int(_lens)
            box = calc(box_id)

            for idx in range(len(arr[box])):
                if arr[box][idx][0] == box_id:
                    arr[box][idx] = (box_id, lens)
                    break
            else:
                arr[box].append((box_id, lens))

    return sum(
        math.prod(
            [
                box_idx,
                lens_idx,
                lens_focal,
            ],
        )
        for box_idx, box in enumerate(arr, start=1)
        for lens_idx, (_, lens_focal) in enumerate(box, start=1)
    )


if __name__ == "__main__":
    data = parse(sys.argv[1])

    # print(part1(data))
    print(part2(data))
