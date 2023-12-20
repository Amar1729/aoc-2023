#! /usr/bin/env python3

from __future__ import annotations

import dataclasses
import math
import sys
import typing
from pathlib import Path
from pprint import pprint  # noqa: F401

import pytest


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


@dataclasses.dataclass
class Layer:
    x: set[int]
    m: set[int]
    a: set[int]
    s: set[int]

    def __init__(self, blank: bool = False):
        if blank:
            for k in "xmas":
                setattr(self, k, set(range(0)))
        else:
            for k in "xmas":
                setattr(self, k, set(range(1, 4001)))

    def filter_rule(self, rule: Rule) -> None:
        s = getattr(self, rule.lop)

        match rule.target, rule.op:
            case "A", "<":
                s &= set(range(1, rule.rop))
            case "A", ">":
                s &= set(range(rule.rop + 1, 4001))
            case "R", "<":
                s = set(range(rule.rop, 4001))
            case "R", ">":
                s = set(range(1, rule.rop + 1))

            # same as A?
            case _, "<":
                s &= set(range(1, rule.rop))
            case _, ">":
                s &= set(range(rule.rop + 1, 4001))

        setattr(self, rule.lop, s)

    def filter_(self, other: Layer, lop: str | None = None) -> None:
        if lop:
            s = getattr(self, lop)
            s -= getattr(other, lop)
            setattr(self, lop, s)
            return

        for k in "xmas":
            s = getattr(self, k)
            s -= getattr(other, k)
            setattr(self, k, s)

    def combined(self, other: Layer) -> Layer | None:
        # how slow is this?
        if all(getattr(self, k).issuperset(getattr(other, k)) for k in "xmas"):
            return self

        if all(getattr(other, k).issuperset(getattr(self, k)) for k in "xmas"):
            return other

        s = 0
        bkey = None
        for k in "xmas":
            if getattr(self, k) == getattr(other, k):
                s += 1
            else:
                bkey = k
        if s == 3 and bkey is not None:
            ns = getattr(self, bkey) | getattr(other, bkey)
            setattr(self, bkey, ns)
            return self

        return None

    def __repr__(self) -> str:
        j = []
        for k in "xmas":
            s = getattr(self, k)
            bounds = []
            if s:
                sn = sx = None
                for c in range(1, 4001):
                    if c in s:
                        if sn is None:
                            sn = c
                        sx = c
                    else:
                        if sn is not None:
                            bounds.append((sn, sx))
                            sn = None
                            sx = None

                if sn is not None:
                    bounds.append((sn, sx))

                b = "|".join([f"{n},{m}" for n, m in bounds])
                j.append(f"{k} = [{b}]")
            else:
                j.append(f"{k}=[]")
        return "Layer: " + ", ".join(j)


def constrain2(flow: Workflow, flows: dict[str, Workflow]) -> list[Layer]:
    layers: list[Layer] = []

    for rule in flow.rules[::-1]:
        match rule.target, rule.lop:
            case "A", "":
                layers.append(Layer())
            case "R", "":
                pass
            case "A", _:
                new_layer = Layer()
                new_layer.filter_rule(rule)
                for layer in layers:
                    layer.filter_(new_layer, rule.lop)
                layers.append(new_layer)
            case "R", _:
                for layer in layers:
                    layer.filter_rule(rule)
            case target, "":
                layers.extend(constrain2(flows[target], flows))
            case target, _:
                other_layers = constrain2(flows[target], flows)
                if not other_layers:
                    print(flow.name)
                    print(f"not other layers: {rule.lop} {rule.op} {rule.rop}")
                    pprint(layers)
                    fake_layer = Layer(blank=True)
                    fake_layer.filter_rule(Rule("R", rule.lop, rule.rop, rule.op))
                    # ???
                    fake_layer.filter_rule(
                        Rule(
                            "R",
                            rule.lop,
                            rule.rop - 1,
                            "<" if rule.op == ">" else ">",
                        ),
                    )
                    print(f"fake layer: {fake_layer}")
                    for layer in layers:
                        layer.filter_(fake_layer)
                    print()
                    pprint(layers)
                    print()
                for other_layer in other_layers:
                    other_layer.filter_rule(rule)
                    for layer in layers:
                        layer.filter_(other_layer, rule.lop)
                layers.extend(other_layers)

    if not layers:
        return []

    combined = [layers.pop(0)]
    for s in layers:
        p = combined[-1].combined(s)
        if p is not None:
            combined[-1] = p
        else:
            combined.append(s)

    print(f"Layers for: {flow.name}")
    pprint(combined)
    print()

    return combined


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
        ("crn", (4000 - 2662) * 4000**3),
        ("gd", 0),
        ("hdj", ((4000 - 838) * 4000**3) + (838 * 1716 * 4000**2)),
        ("lnx", 4000**4),
        ("pv", 1716 * 4000**3),
        ("qkq", (1415 * 4000**3) + (4000 - 2662) * 4000**3),
        # check this math later
        # [Layer: x = [(1,4000)], m = [(1,838)], a = [(1,1716)], s = [(1,2770)],
        # Layer: x = [(1,4000)], m = [(839,1800)], a = [(1,4000)], s = [(1,2770)],
        # Layer: x = [(1,4000)], m = [(1,4000)], a = [(1,4000)], s = [(2771,4000)]]
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
def test_count(flow_name: str, count: int) -> None:
    _flows, _ = parse("sample.txt")
    flows = {w.name: w for w in _flows}
    assert count == calc(flow_name, flows)


def calc(target: str, flows: dict[str, Workflow]) -> int:
    return sum(
        math.prod(len(getattr(layer, k)) for k in "xmas")
        for layer in constrain2(flows[target], flows)
    )


def part2(data: tuple[list[Workflow], list[Part]]) -> int:
    flows = {w.name: w for w in data[0]}
    return calc("in", flows)


if __name__ == "__main__":
    data = parse(sys.argv[1])

    # print(part1(data))
    print(part2(data))
