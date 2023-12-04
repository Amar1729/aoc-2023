#! /usr/bin/env python3

from __future__ import annotations

# commonly-used built-in imports. not all of these are necessarily used each day.
import sys
from collections import Counter
from pathlib import Path
from typing import NamedTuple


class Card(NamedTuple):
    card_id: int
    winning: set[int]
    obtained: list[int]

    @classmethod
    def from_line(cls, line: str) -> Card:
        card, numbers = line.split(": ")
        return Card(
            card_id = int(card.split(" ")[-1]),
            winning = set([int(n) for n in numbers.split("|")[0].split(" ") if n]),
            obtained = [int(n) for n in numbers.split("|")[1].split(" ") if n],
        )

    def score(self) -> int:
        score = None
        for n in self.obtained:
            if n in self.winning:
                if not score:
                    score = 1
                else:
                    score *= 2

        return score or 0

    def copy_score(self) -> int:
        return sum([n in self.winning for n in self.obtained])

    def __repr__(self) -> str:
        return f"{self.card_id}: {self.winning} | {self.obtained}"


def parse(fname: str) -> list[Card]:
    """Read from data file. Returns problem specific formatted data."""
    with Path(fname).open() as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    return list(map(Card.from_line, lines))


def part1(data: list[Card]) -> int:
    # for card in data:
    #     print(card)
    return sum(map(lambda card: card.score(), data))


def part2(data: list[Card]) -> int:
    copies: Counter[int] = Counter()

    last_card_id = data[-1].card_id

    for card in data:
        copies[card.card_id] += 1  # add the original card
        mult = copies[card.card_id]
        for c in range(
            card.card_id + 1, min(last_card_id + 1, card.card_id + 1 + card.copy_score()),
        ):
            copies[c] += mult

    return copies.total()


if __name__ == "__main__":
    data = parse(sys.argv[1])

    # print(part1(data))
    print(part2(data))
