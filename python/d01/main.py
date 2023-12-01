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


# good god
def parse_number(s: str, forward: bool) -> int | None:
    if forward:
        while s:
            if (s[0] == "1") or s.startswith("one"):
                return 1
            if (s[0] == "2") | s.startswith("two"):
                return 2
            if (s[0] == "3") | s.startswith("three"):
                return 3
            if (s[0] == "4") | s.startswith("four"):
                return 4
            if (s[0] == "5") | s.startswith("five"):
                return 5
            if (s[0] == "6") | s.startswith("six"):
                return 6
            if (s[0] == "7") | s.startswith("seven"):
                return 7
            if (s[0] == "8") | s.startswith("eight"):
                return 8
            if (s[0] == "9") | s.startswith("nine"):
                return 9

            s = s[1:]

    else:
        while s:
            if (s[-1] == "1") or s.endswith("one"):
                return 1
            if (s[-1] == "2") | s.endswith("two"):
                return 2
            if (s[-1] == "3") | s.endswith("three"):
                return 3
            if (s[-1] == "4") | s.endswith("four"):
                return 4
            if (s[-1] == "5") | s.endswith("five"):
                return 5
            if (s[-1] == "6") | s.endswith("six"):
                return 6
            if (s[-1] == "7") | s.endswith("seven"):
                return 7
            if (s[-1] == "8") | s.endswith("eight"):
                return 8
            if (s[-1] == "9") | s.endswith("nine"):
                return 9

            s = s[:-1]

    return None


def part2(data) -> int:
    digits = [
        int(f"{parse_number(line, True)}{parse_number(line, False)}")
        for line in data
    ]

    return sum(digits)


if __name__ == "__main__":
    data = parse(sys.argv[1])

    # print(part1(data))
    print(part2(data))
