#! /usr/bin/env python3

from __future__ import annotations

import sys
import typing
from pathlib import Path
from pprint import pprint  # noqa: F401


class Part(typing.NamedTuple):
    x: int
    m: int
    a: int
    s: int


class Rule(typing.NamedTuple):
    target: str
    lop: str
    rop: int
    op: str


class Workflow(typing.NamedTuple):
    name: str
    rules: list[Rule]

    def run(self, part: Part) -> str | bool:
        for rule in self.rules:
            if rule.lop and rule.rop:
                lop = getattr(part, rule.lop)
                if eval(f"{lop} {rule.op} {rule.rop}"):
                    if rule.target == "A":
                        return True
                    if rule.target == "R":
                        return False
                    return rule.target
            elif rule.target == "A":
                return True
            elif rule.target == "R":
                return False
            else:
                return rule.target

        raise ValueError


def parse(fname: str) -> tuple[list[Workflow], list[Part]]:
    """Read from data file. Returns problem specific formatted data."""
    with Path(fname).open() as f:
        content = f.read().split("\n\n")

    rules = [line.strip() for line in content[0].splitlines()]
    parts = [line.strip() for line in content[1].splitlines()]

    return list(map(parse_workflow, rules)), list(map(parse_part, parts))


def parse_workflow(line: str) -> Workflow:
    c = line.index("{")  # }
    name = line[:c]
    rest = line[c+1:-1].split(",")

    rules = []

    for rule in rest:
        if any(c in rule for c in "<>:"):
            expr, target = rule.split(":")
            op = "<" if "<" in expr else ">"
            assert op in expr
            lop, _rop = expr.split(op)
            rop = int(_rop)

            rules.append(Rule(target, lop, rop, op))
        else:
            rules.append(Rule(rule, "", 0, ""))

    return Workflow(name, rules)


def parse_part(line: str) -> Part:
    four = line[1:-1].split(",")
    nums = [int(s.split("=")[1]) for s in four]

    return Part(*nums)


def part1(data: tuple[list[Workflow], list[Part]]) -> int:
    flows = {w.name: w for w in data[0]}
    parts = data[1]

    accepted = []
    for part in parts:
        rule: str | bool = "in"
        while isinstance(rule, str):
            rule = flows[rule].run(part)

        if rule:
            accepted.append(part)

    return sum(p.x + p.m + p.a + p.s for p in accepted)


def part2(data) -> int:
    print(data)
    return 0


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(part1(data))
    # print(part2(data))
