#! /usr/bin/env python3

from __future__ import annotations

import math
import sys
from pathlib import Path
from pprint import pprint  # noqa: F401

import networkx as nx


def parse(fname: str) -> list[str]:
    """Read from data file. Returns problem specific formatted data."""
    with Path(fname).open() as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    g = nx.Graph()

    for line in lines:
        node, childs = line.split(": ")
        children = [c for c in childs.split(" ")]
        g.add_node(node)
        g.add_nodes_from(children)
        g.add_edges_from([(node, child) for child in children])

    return g


def part1(data: nx.Graph) -> int:
    print(data)

    # determined via graphviz:
    # neato -Tpng -ograph.png graph-input.txt
    data.remove_edges_from([
        ("ncg", "gsk"),
        ("mrd", "rjs"),
        ("gmr", "ntx"),
    ])

    cc = list(nx.connected_components(data))

    return math.prod(
        len(comp)
        for comp in cc
    )


def part2(data) -> int:
    print(data)
    return 0


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(part1(data))
    # print(part2(data))
