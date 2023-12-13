#! /usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path
from pprint import pprint  # noqa: F401


def parse(fname: str) -> list[str]:
    """Read from data file. Returns problem specific formatted data."""
    with Path(fname).open() as f:
        content = f.read()

    return [[line for line in chunk.split()] for chunk in content.split("\n\n")]


def fold(s: list[str]) -> int:
    for col in range(1, len(s[0])):
        if all(l == r for line in s for l, r in zip(line[:col][::-1], line[col:])):
            return col

    for row in range(1, len(s)):
        up = s[:row][::-1]
        down = s[row:]

        if all(u_row == d_row for u_row, d_row in zip(up, down)):
            return row * 100

    # print our stuff if we reach err state
    for l in s:
        print(l)
    raise ValueError


def fuzzy_fold(s: list[str]) -> int:
    for col in range(1, len(s[0])):
        b = sum(l == r for line in s for l, r in zip(line[:col][::-1], line[col:]))
        line = s[0]
        correct = min(len(line[col:]), len(line[:col])) * len(s)
        if b == correct - 1:
            return col

    for row in range(1, len(s)):
        up = s[:row][::-1]
        down = s[row:]

        b = sum(u_c == d_c for u_row, d_row in zip(up, down) for u_c, d_c in zip(u_row, d_row))
        correct = min(len(up), len(down)) * len(up[0])
        if b == correct - 1:
            return row * 100

    # print our stuff if we reach err state
    for l in s:
        print(l)
    raise ValueError


def part1(data) -> int:
    return sum(fold(chunk) for chunk in data)


def part2(data) -> int:
    return sum(fuzzy_fold(chunk) for chunk in data)


if __name__ == "__main__":
    data = parse(sys.argv[1])

    # print(part1(data))
    print(part2(data))
