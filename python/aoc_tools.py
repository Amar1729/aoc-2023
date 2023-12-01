from __future__ import annotations

from enum import Enum
from typing import Generator, NamedTuple


class Color(Enum):
    red = "\033[31m"  # ]
    noc = "\033[0m"  # ]


def colorize(s: str) -> str:
    """Colorize an input string"""
    return Color.red.value + s + Color.noc.value


class Point(NamedTuple):
    """Commonly-used grid math

    Yes i know about complex(), but with that you have to do int() casts all over
    to use imag or real components as indices.
    """
    x: int
    y: int

    # violates liskov substitution, since supertype NamedTuple has an __add__ method.
    # just ignore type error for this line.
    def __add__(self: Point, other: Point) -> Point:  # type: ignore[override]
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self: Point, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)


ORTHOGONAL = [
    Point(+1, 0),
    Point(-1, 0),
    Point(0, +1),
    Point(0, -1),
]


DIAGONAL = [
    Point(-1, -1),
    Point(-1, +1),
    Point(+1, -1),
    Point(+1, +1),
]


def inclusive_range(m1: int, m2: int) -> Generator[int, None, None]:
    """needs a range including both endpoints, possibly with unordered arguments"""
    yield from range(min(m1, m2), max(m1, m2) + 1)
