#! /usr/bin/env python3

from __future__ import annotations

import dataclasses
import math
import sys
import typing
from pathlib import Path
from pprint import pprint  # noqa: F401

import pytest


# ... Gross.
class CubeSplitKwargs(typing.TypedDict):
    attr: typing.NotRequired[str]
    op: typing.NotRequired[str]
    bound: typing.NotRequired[int]
    rule: typing.NotRequired[Rule]


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


@dataclasses.dataclass
class Workflow:
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


@pytest.mark.parametrize(
    ("flow_name", "count"),
    [
        # mostly worked out by hand; some values taken by just calculation and assuming
        # correctness.
        ("crn", (4000 - 2662) * 4000**3),
        ("gd", 0),
        ("hdj", ((4000 - 838) * 4000**3) + (838 * 1716 * 4000**2)),
        ("lnx", 4000**4),
        ("pv", 1716 * 4000**3),
        ("qkq", (1415 * 4000**3) + (4000 - 2662) * 4000**3),
        ("qqz", 137288968640000),
        ("qs", 4000**4),
        ("rfg", 2440 * (4000 - 536) * 4000**2),
        (
            "px",
            (2440 * 2090 * (4000 - 2006 + 1) * (4000 - 537 + 1))
            + (4000 * (4000 - 2091 + 1) * (4000 - 2006 + 1) * 4000)
            + (((4000 - 2663 + 1) + 1415) * 2005 * 4000**2),
        ),
        ("in", 167409079868000),
    ],
)
def test_cube(flow_name: str, count: int) -> None:
    _flows, _ = parse("sample.txt")
    flows = {w.name: w for w in _flows}
    assert count == apply_flows(flow_name, flows)  # noqa: S101


@dataclasses.dataclass
class Cube:
    """Set of x.m.a.s. points that can be easily split down.

    Look, i know this isn't a *cube*, it's more technically a 4-orthotope, or hyperrectangle
    (similar to a hypercube, but with faces that aren't necessarily congruent). That's a bit
    wordy for a class name though...
    """
    def __init__(self, init: bool=True):
        if init:
            self.x = set(range(1, 4001))
            self.m = set(range(1, 4001))
            self.a = set(range(1, 4001))
            self.s = set(range(1, 4001))
        else:
            self.x = set()
            self.m = set()
            self.a = set()
            self.s = set()

    def __repr__(self) -> str:
        st = "Cube("
        for k in "xmas":
            s = getattr(self, k)
            st += f"{k}=[{min(s)}, {max(s)}], "
        return st[:-3] + ")"

    def copy(self, not_with_label: str) -> Cube:
        cube = Cube(False)
        for k in "xmas":
            if k != not_with_label:
                setattr(cube, k, getattr(self, k))
        return cube

    def count(self) -> int:
        return math.prod(len(getattr(self, k)) for k in "xmas")

    def blank(self) -> None:
        # blank out a cube (if a rule is a reject rule and wants to blank us)
        for k in "xmas":
            setattr(self, k, set())

    def split(self, **kwargs: typing.Unpack[CubeSplitKwargs]) -> tuple[Cube, Cube]:
        """Returns the cube of accepted points and the cube of rejected points.

        Here, "accepted" and "rejected" means for a particular rule (what's causing the split)
        and not specifically the A/R targets used in the workflow.
        """

        rule = kwargs.get("rule", None)
        if rule:
            attr = rule.lop
            op = rule.op
            bound = rule.rop
        else:
            # i'm not sure how to type-guard a TypedDict?
            try:
                attr = kwargs["attr"]
                op = kwargs["op"]
                bound = kwargs["bound"]
            except KeyError:
                msg = "`rule` or all of `attr`, `op`, `bound` are required."
                raise TypeError(msg) from KeyError

        if op == "<":
            ns = set(range(1, bound))
        elif op == ">":
            ns = set(range(bound + 1, 4001))
        else:
            msg = "`op` must be <>."
            raise ValueError(msg)

        s = getattr(self, attr)

        accepted_points = s & ns
        acc = self.copy(attr)
        setattr(acc, attr, accepted_points)

        rejected_points = s - accepted_points
        rej = self.copy(attr)
        setattr(rej, attr, rejected_points)

        return (acc, rej)


def apply_flows(flow_name: str, flows: dict[str, Workflow], cube: Cube | None = None) -> int:
    if cube is None:
        cube = Cube()

    s = 0

    # iterate over each Rule in our Workflow.
    # as we do, we successively split our cube:
    # A rules take some of the cube, and add to our total
    # R rules takes some of the cube, and dont add
    # other targets recurse, to find the proper count of those flows.
    for rule in flows[flow_name].rules:
        match rule.target, rule.lop:
            case "A", "":
                assert cube is not None  # noqa: S101
                s += cube.count()
            case "R", "":
                pass
            case "A", _:
                assert cube is not None  # noqa: S101
                acc, cube = cube.split(rule=rule)
                s += acc.count()
            case "R", _:
                assert cube is not None  # noqa: S101
                _, cube = cube.split(rule=rule)
            case _ as t, "":
                # end of the line: add any results from this target, given our current cube.
                s += apply_flows(t, flows, cube)
            case _ as t, _:
                assert cube is not None  # noqa: S101
                acc, cube = cube.split(rule=rule)
                s += apply_flows(t, flows, acc)
            case _:
                raise ValueError(rule)

    return s


def part2(data: tuple[list[Workflow], list[Part]]) -> int:
    flows = {w.name: w for w in data[0]}
    return apply_flows("in", flows)


if __name__ == "__main__":
    data = parse(sys.argv[1])

    # print(part1(data))
    print(part2(data))
