#! /usr/bin/env python3

from __future__ import annotations

# commonly-used built-in imports. not all of these are necessarily used each day.
import collections
import functools
import itertools
import re
import sys
import typing
from pathlib import Path
from pprint import pprint  # noqa: F401

# see parent directory
# from aoc_tools import *


def parse(fname: str) -> list[str]:
    """Read from data file. Returns problem specific formatted data."""
    with Path(fname).open() as f:
        return [line.strip() for line in f.read().splitlines() if line.strip()]


def part1(data) -> int:
    print(data)
    return 0


def part2(data) -> int:
    print(data)
    return 0


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(part1(data))
    # print(part2(data))
