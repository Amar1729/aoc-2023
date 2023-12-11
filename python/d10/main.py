#! /usr/bin/env python3

# Attempted to "learn" networkx for this one.
# You can see how poorly it went.

from __future__ import annotations

import sys
from pathlib import Path
from pprint import pprint  # noqa: F401

import networkx as nx
import numpy as np


def yield_neighbors(c: str, x, y):
    match c:
        case "S":
            yield (x + 1, y)
            yield (x - 1, y)
            yield (x, y + 1)
            yield (x, y - 1)
        case "|":
            yield (x, y - 1)
            yield (x, y + 1)
        case "-":
            yield (x + 1, y)
            yield (x - 1, y)
        case "L":
            yield (x + 1, y)
            yield (x, y - 1)
        case "J":
            yield (x - 1, y)
            yield (x, y - 1)
        case "7":
            yield (x - 1, y)
            yield (x, y + 1)
        case "F":
            yield (x + 1, y)
            yield (x, y + 1)


def points_are_connected(c1: str, p1, c2: str, p2) -> bool:
    p1 = p1[::-1]
    p2 = p2[::-1]
    return p2 in yield_neighbors(c1, *p1) and p1 in yield_neighbors(c2, *p2)


def parse(fname: str) -> tuple[tuple[int, int], nx.DiGraph]:
    """Read from data file. Returns problem specific formatted data."""
    with Path(fname).open() as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    H = np.array([list(row) for row in lines])
    start = tuple(*np.argwhere(H == "S"))

    G = nx.grid_2d_graph(*H.shape, create_using=nx.DiGraph)
    G.remove_edges_from([
        (a, b)
        for a, b in G.edges
        if not points_are_connected(H[a], a, H[b], b)
    ])

    # remove nodes that aren't properly connected
    # doesn't seem to do anything
    d = dict(G.adjacency())
    good_nodes = set([
        n for n, others in d.items()
        if len(others.keys()) >= 2 and all(n in d[k] for k in others)
    ])
    G.remove_nodes_from(set(G.nodes) - good_nodes)

    return start, G


def part1(data) -> int:
    start, g = data

    # ???
    cycles = [set(p) for p in nx.simple_cycles(g) if start in p and len(p) > 2]
    assert len(cycles) == 2, len(cycles)

    return len(cycles[0]) // 2


def part2(data) -> int:
    print(data)
    return 0


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(part1(data))
    # print(part2(data))
