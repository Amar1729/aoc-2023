#! /usr/bin/env python3

from __future__ import annotations

# commonly-used built-in imports. not all of these are necessarily used each day.
import functools
import sys
from pathlib import Path

# see parent directory
# from aoc_tools import *


class Set:
    red: int = 0
    blue: int = 0
    green: int = 0


class Game:
    def __init__(self, s: str):
        game_id, sets = s.split(": ")

        self.game_id = int(game_id.split(" ")[-1])
        self.sets = []
        for set_ in sets.split("; "):
            # red, blue, green
            set_q = Set()
            for c in set_.split(", "):
                i, col = c.split(" ")
                if col == "red":
                    set_q.red = int(i)
                if col == "blue":
                    set_q.blue = int(i)
                if col == "green":
                    set_q.green = int(i)
            self.sets.append(set_q)

    def possible(self) -> bool:
        return all(
            s.red <= 12 and s.blue <= 14 and s.green <= 13
            for s in self.sets
        )


def parse(fname: str) -> list[str]:
    """Read from data file. Returns problem specific formatted data."""
    with Path(fname).open() as f:
        return [line.strip() for line in f.read().splitlines() if line.strip()]


def part1(data: list[str]) -> int:
    games = list(map(Game, data))
    return sum(g.game_id for g in filter(lambda g: g.possible(), games))


def part2(data: list[str]) -> int:
    total = 0

    # todo

    return total


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(part1(data))
    print(part2(data))
