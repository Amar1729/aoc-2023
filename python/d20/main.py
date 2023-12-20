#! /usr/bin/env python3

from __future__ import annotations

import collections
import dataclasses
import math
import sys
from pathlib import Path
from pprint import pprint  # noqa: F401


@dataclasses.dataclass
class Module:
    # define here to take advantage of dataclass automatic repr
    mod_name: str
    mod_type: str
    receivers: list[str]
    state: bool
    memory: dict[str, bool]

    # flip-flop: %
    # conjunction: &
    def __init__(self, s: str):
        self.mod_name, receivers = s.split(" -> ")

        self.mod_type = ""
        if self.mod_name[0] in ("&", "%"):
            self.mod_type = self.mod_name[0]
            self.mod_name = self.mod_name[1:]

        self.receivers = receivers.split(", ")

        # for flip-flop
        self.state = False

        # memory is the current state.
        self.memory = {}

    def set_memory(self, modules: list[str]) -> None:
        """Set the input modules for a conjunction module."""
        for m in modules:
            self.memory[m] = False

    def send(self, pulse: bool, input_mod: str | None = None) -> bool | None:
        # type of pulse to send (if any).
        # destination is managed outside this function.

        if self.mod_type == "%":
            # flip-flop
            if pulse:
                return None

            self.state = not self.state
            return self.state

        if self.mod_type == "&":
            assert input_mod is not None
            self.memory[input_mod] = pulse
            return not all(self.memory.values())

        if self.mod_name == "broadcaster":
            return pulse

        if self.mod_name == "output":
            # nothing; for testing only.
            return None

        raise ValueError


def parse(fname: str) -> dict[str, Module]:
    """Read from data file. Returns problem specific formatted data."""
    with Path(fname).open() as f:
        modules = [Module(line.strip()) for line in f.read().splitlines() if line.strip()]

    modules_d = {m.mod_name: m for m in modules}

    if fname == "sample2.txt":
        # ???
        # completely fake
        modules_d["output"] = Module("output -> output")

    # parse out the inputs to each conjunction module as well.

    input_counter = collections.defaultdict(list)

    for m_name, m in modules_d.items():
        for dst in m.receivers:
            if dst not in modules_d:
                # is this ... allowed?
                # it's the "rx" module, a thing for p2.
                continue
            if modules_d[dst].mod_type == "&":
                input_counter[dst].append(m_name)

    for dst, input_mod_names in input_counter.items():
        modules_d[dst].set_memory(input_mod_names)

    return modules_d


# side note: i really don't like this type signature.
# i'm not sure how to get it to look better, although i thought type guards could help...
def push_button(modules: dict[str, Module], part2: bool = False) -> tuple[int, int] | str:
    """Modifies the input modules. Returns number of high/low pulses sent."""

    signal = modules["broadcaster"].send(False)

    # queue of signals to send, and to whom
    q: list[tuple[str, str, bool | None]] = [
        ("broadcaster", rec, signal)
        for rec in modules["broadcaster"].receivers
        if signal is not None
    ]

    highs = lows = 0
    # of high school football

    # PART 2:
    # we are looking for particular receivers, whenever they get set.
    # specifically, we are looking for any of the ones that feed into the "mf"
    # module, which is the only module that feeds into the "rx" module.
    found = ""

    while q:
        src, rec, signal = q.pop(0)
        # what about none?
        # s_signal = "-high" if signal else "-low"
        # if signal is None:
        #     s_signal = "<none>"
        # print(f"{src} {s_signal} -> {rec}")

        if signal is True:
            highs += 1
        if signal is False:
            lows += 1

        if signal is not None:
            # rx module is EFFED? will that be for p2?
            if rec not in modules:
                continue
            if rec == "mf" and signal is True:
                found = src
            # keep in mind that sending a signal may mutate a module.
            # make sure to send the source so conj mods can do their thing?
            output = modules[rec].send(signal, src)
            if output is not None:
                q.extend([
                    (rec, m_rec, output)
                    for m_rec in modules[rec].receivers
                ])

    if isinstance(part2, str):
        return found

    # add 1 to lows for the initial button->broadcaster press.
    return highs, lows + 1


def part1(data: dict[str, Module]) -> int:
    th = tl = 0
    for b in range(1000):
        r = push_button(data)
        assert isinstance(r, tuple)
        h, l = r
        print(f"\nPUSH BUTTON: {b} {h} {l}\n")
        th += h
        tl += l

    return th * tl


def part2(data: dict[str, Module]) -> int:
    b = 0
    prevs: dict[str, int] = {}
    while len(prevs) < 4:
        rec = push_button(data, True)
        assert isinstance(rec, str)
        b += 1
        # print(f"PUSH BUTTON: {b}")

        if rec and rec not in prevs:
            prevs[rec] = b

    # woop woop
    return math.lcm(*prevs.values())


if __name__ == "__main__":
    data = parse(sys.argv[1])

    # print(part1(data))
    print(part2(data))
