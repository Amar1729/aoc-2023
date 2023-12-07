#! /usr/bin/env python3

from __future__ import annotations

# commonly-used built-in imports. not all of these are necessarily used each day.
import functools
import sys
import typing
from collections import Counter
from enum import Enum, auto
from pathlib import Path
from pprint import pprint

# ace is high
CARDS = {c: idx for idx, c in enumerate("23456789TJQKA")}


@functools.total_ordering
class HandType(Enum):
    five = auto()
    four = auto()
    full = auto()
    three = auto()
    two_p = auto()
    one_p = auto()
    high = auto()

    @classmethod
    def from_line(cls, s: str) -> HandType:
        cards = Counter(Counter(s).values())

        if 5 in cards:
            return HandType.five
        if 4 in cards:
            return HandType.four
        if 3 in cards and 2 in cards:
            return HandType.full
        if 3 in cards:
            return HandType.three
        if 2 in cards and cards[2] == 2:
            return HandType.two_p
        if 2 in cards and cards[2] == 1:
            return HandType.one_p

        return HandType.high

    def __le__(self, other):
        return (self.value > other.value) or (self == other)

    def __eq__(self, other):
        return self.value == other.value


@functools.total_ordering
class Hand(typing.NamedTuple):
    type_: HandType
    cards: tuple[str, str, str, str, str]
    bid: int

    @classmethod
    def from_line(cls, s: str) -> Hand:
        cards, bid = s.split(" ")

        return Hand(
            type_ = HandType.from_line(cards),
            cards = tuple([c for c in cards]),
            bid = int(bid),
        )

    def __eq__(self, other) -> bool:
        if self.type_ == other.type_:
            return all(CARDS[c1] == CARDS[c2] for c1, c2 in zip(self.cards, other.cards))
        return False

    def __lt__(self, other) -> bool:
        if self.type_ < other.type_:
            return True

        if self.type_ > other.type_:
            return False

        for c1, c2 in zip(self.cards, other.cards):
            if CARDS[c1] < CARDS[c2]:
                return True
            if CARDS[c1] > CARDS[c2]:
                return False
            # if they're equal, keep checking

        return False


def parse(fname: str) -> list[Hand]:
    """Read from data file. Returns problem specific formatted data."""
    with Path(fname).open() as f:
        return [Hand.from_line(line.strip()) for line in f.read().splitlines() if line.strip()]


def part1(data: list[Hand]) -> int:
    return sum(
        hand.bid * rank
        for rank, hand in enumerate(sorted(data), start=1)
    )


def part2(data) -> int:
    print(data)
    return 0


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(part1(data))
    # print(part2(data))
