#! /usr/bin/env python3

from __future__ import annotations

import itertools
import sys
import typing
from pathlib import Path
from pprint import pprint  # noqa: F401

import numpy as np
import numpy.typing as npt


class Point(typing.NamedTuple):
    x: int
    y: int
    z: int


class Vec(typing.NamedTuple):
    p: Point
    v: Point

    def next_point(self) -> Point:
        return Point(
            self.p.x + self.v.x,
            self.p.y + self.v.y,
            self.p.z + self.v.z,
        )

    @staticmethod
    def from_line(line: str) -> Vec:
        ps, vs = line.split(" @ ")
        p = map(int, ps.split(", "))
        v = map(int, vs.split(", "))
        return Vec(Point(*p), Point(*v))

    def intersect(self, other: Vec) -> npt.NDArray[np.float64] | None:
        p2_self = self.next_point()
        p2_other = other.next_point()

        a = np.array([
            [
                self.p.y - p2_self.y,
                p2_self.x - self.p.x,
            ],
            [
                other.p.y - p2_other.y,
                p2_other.x - other.p.x,
            ],
        ])

        b = -np.array([
            self.p.x * p2_self.y - p2_self.x * self.p.y,
            other.p.x * p2_other.y - p2_other.x * other.p.y,
        ])

        try:
            return np.linalg.solve(a, b)
        except np.linalg.LinAlgError:
            return None

    def has_future(self, p: npt.NDArray[np.float64]) -> bool:
        for idx, attr in enumerate("xy"):
            pa = getattr(self.p, attr)
            va = getattr(self.v, attr)

            if va > 0 and p[idx] <= pa:
                return False
            if va < 0 and p[idx] >= pa:
                return False
            if va == 0 and not np.isclose(p[idx], 0.0):
                return False

        return True


def parse(fname: str) -> list[Vec]:
    """Read from data file. Returns problem specific formatted data."""
    with Path(fname).open() as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    return list(map(Vec.from_line, lines))


def part1(data: list[Vec]) -> int:
    tot = 0

    # mn = 7
    # mx = 27
    mn = 200_000_000_000_000
    mx = 400_000_000_000_000

    for v1, v2 in itertools.combinations(data, 2):

        p = v1.intersect(v2)

        if p is not None and v1.has_future(p) and v2.has_future(p):

            x = round(p[0])
            y = round(p[1])

            if mn <= x <= mx and mn <= y <= mx:
                tot += 1

    return tot


def part2(data) -> int:
    print(data)
    return 0


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(part1(data))
    # print(part2(data))
