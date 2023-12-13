#! /usr/bin/env python3

from __future__ import annotations

import functools
import sys
from pathlib import Path
from pprint import pprint  # noqa: F401

import pytest


def parse_line(s: str) -> tuple[str, tuple[int, ...]]:
    s, nums = s.split(" ")
    return (s, tuple(map(int, nums.split(","))))


def parse(fname: str) -> list[tuple[str, tuple[int, ...]]]:
    """Read from data file. Returns problem specific formatted data."""
    with Path(fname).open() as f:
        return [parse_line(line.strip()) for line in f.read().splitlines() if line.strip()]


@functools.cache
def calc(unknown: str, values: tuple[int, ...]) -> int:
    # recursive.
    # build the solution backwards.
    if len(values) == 1:
        # base case
        c = 0
        for idx in range(len(unknown) - values[0] + 1):
            substring_is_valid = all(s in "#?" for s in unknown[idx:idx+values[0]])
            rest_of_string_ok = "#" not in unknown[:idx] + unknown[idx+values[0]:]
            if substring_is_valid and rest_of_string_ok:
                c += 1
        # print(f"Recieved {unknown} {values[0]=}; found {c}")
        return c

    # get a bound for the rest of the string based on rest of values.
    # then look at first value + soln(rest of string)

    # lower bound for rest of string:
    # each value needs one space on each side; not counting the end
    # of string, this is len(values[1:]).
    rest_of_line = sum(values[1:]) + len(values[1:])

    # ex:
    # len(s) == 10
    # values = [2, 3]
    # iterate from: 0:2 to 4:6
    # importantly, the first value will take one extra space from the str
    # so s gets split like:
    # 0:2 2:3 3:10
    # 1:3 3:4 4:10
    # ...
    # 4:6 6:7 7:10

    tot = 0
    right_bound = len(unknown) - rest_of_line
    # print(f"Initial {len(unknown)} {unknown=}")
    for idx in range(right_bound - values[0] + 1):
        s_left = unknown[idx:idx+values[0]]
        s_right = unknown[idx+values[0]+1:]

        # edge case: it's not valid to split and drop a '#'
        if unknown[idx + values[0]] == "#":
            # print("Dropping a '#'; skipping.")
            continue
        # edge case: not valid to leave "#" behind s_left
        if "#" in unknown[:idx]:
            continue

        # print(f"Splitting string to {idx} '{s_left}' | '{unknown[idx+values[0]]}' | '{s_right}' {values=}")
        v_1 = calc(s_left, (values[0],))
        if v_1 > 0:
            v_rest = calc(s_right, values[1:])
            # print(f"results: {v_1=} {v_rest=}")
            tot += v_rest

    return tot


def part1(data: list[tuple[str, tuple[int, ...]]]) -> int:
    return sum(calc(*line) for line in data)


def munge_line(line: tuple[str, tuple[int, ...]]) -> tuple[str, tuple[int, ...]]:
    return ("?".join([line[0]] * 5), line[1] * 5)


def part2(data: list[tuple[str, tuple[int, ...]]]) -> int:
    return sum(calc(*munge_line(line)) for line in data)


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        # my own tests
        ("??? 1", 3),
        ("??? 1,1", 1),
        ("?.???.......... 1,3", 1),
        # ("?????????? 2,3", 24),
        ("?????????? 1,1,6", 1),
        ("???? 1,2", 1),
        ("???#? 1", 1),

        ("???.### 1,1,3", 1),
        (".??..??...?##. 1,1,3", 4),
        ("?#?#?#?#?#?#?#? 1,3,1,6", 1),
        # .1.333.1.666666
        ("????.#...#... 4,1,1", 1),
        ("????.######..#####. 1,6,5", 4),

        ("?###???????? 3,2,1", 10),
        # so ^this is basically:
        ("??????? 2,1", 10),
        # 22.1...
        # 22..1..
        # 22...1.
        # 22....1
        # .22.1..
        # .22..1.
        # .22...1
        # ..22.1.
        # ..22..1
        # ...22.1
    ],
)
def test_p1(s: str, expected: int) -> None:
    assert expected == calc(*parse_line(s))  # noqa: S101


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("???.### 1,1,3", 1),
        (".??..??...?##. 1,1,3", 16384),
        ("?#?#?#?#?#?#?#? 1,3,1,6", 1),
        ("????.#...#... 4,1,1", 16),
        ("????.######..#####. 1,6,5", 2500),
        ("?###???????? 3,2,1", 506250),
    ],
)
def test_p2(s: str, expected: int) -> None:
    assert expected == calc(*munge_line(parse_line(s)))  # noqa: S101


if __name__ == "__main__":
    data = parse(sys.argv[1])

    # print(part1(data))
    print(part2(data))

    # fun to see how many times the cache has been BLASTED
    print(calc.cache_info())
