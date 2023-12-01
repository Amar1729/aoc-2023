#! /usr/bin/env python3

import re
import sys


def parse(fname: str):
    """Read from data file. Returns problem specific formatted data."""
    with open(fname) as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    return lines


def part1(data) -> int:
    digits = []
    for line in data:
        stripped = re.sub(r"[a-z]", "", line)
        stripped = stripped[0] + stripped[-1]
        digits.append(int(stripped))

    return sum(digits)


def part2(data) -> int:
    total = 0

    # todo

    return total


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(part1(data))
    print(part2(data))
