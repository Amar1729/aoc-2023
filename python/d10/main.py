#! /usr/bin/env python3

# Attempted to "learn" networkx for this one.
# You can see how poorly it went.

from __future__ import annotations

import itertools
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
    start: tuple[int, int] = tuple(*np.argwhere(H == "S"))

    G = nx.grid_2d_graph(*H.shape, create_using=nx.DiGraph)
    G.remove_edges_from([(a, b) for a, b in G.edges if not points_are_connected(H[a], a, H[b], b)])

    # remove nodes that aren't properly connected
    # doesn't seem to do anything
    d = dict(G.adjacency())
    good_nodes = set(
        [n for n, others in d.items() if len(others.keys()) >= 2 and all(n in d[k] for k in others)]
    )
    G.remove_nodes_from(set(G.nodes) - good_nodes)

    for node in G.nodes:
        G.add_node(node, label=H[node])

    return start, G


def part1(data) -> int:
    start, g = data

    # ???
    cycles = [set(p) for p in nx.simple_cycles(g) if start in p and len(p) > 2]
    assert len(cycles) == 2, len(cycles)

    return len(cycles[0]) // 2


def pretty_print(path, points, outside=None, fname=None):
    h = None
    if fname:
        with Path(fname).open() as f:
            content = f.read()
        h = np.array([list(row) for row in content.splitlines()])

    max_y = max(p[0] for p in itertools.chain(path, points))
    max_x = max(p[1] for p in itertools.chain(path, points))

    mapp = {
        "F": "┌",
        "L": "└",
        "-": "─",
        "7": "┐",
        "|": "│",
        "J": "┘",
        "S": "S",
    }

    for y in range(max_y + 1):
        row = ["X"] * (max_x + 1)
        for x in range(max_x + 1):
            if (y, x) in path:
                row[x] = "#"
                if h is not None:
                    row[x] = mapp[h[(y, x)]]
            if (y, x) in points:
                row[x] = "I"
            if (y, x) in outside:
                row[x] = " "
        print("".join(row))


# who needs a 4090 when you can code up ray-tracing in python?
def part2(data) -> int:
    """
    Use a ray-tracing approach to find all points inside.

    Left-to-right, a point is inside our path if we've encountered an even number of vertical
    segments so far. However, our tracing rays move parallel to our edges in some cases, so be
    sure to track the corners (FLJ7) as well.
    """
    start, g = data

    # there's some minor optimization over the next few lines:
    # `cycle` is saved, even though i immediately turn it into a dict
    # y_range and x_range together iterate over cycle points 4 times, so calculating those
    # and `h` could probably all be done in one loop. i felt like keeping it more readable.

    cycle = set(next(filter(lambda p: start in p and len(p) > 2, nx.simple_cycles(g))))
    h = {n: g.nodes[n]["label"] for n in cycle}

    y_range = range(min(p[0] for p in cycle), max(p[0] for p in cycle))
    x_range = range(min(p[1] for p in cycle), max(p[1] for p in cycle))

    contained_tiles = 0
    for row_idx in y_range:
        parity = 0
        prev_corner = ""
        for col_idx in x_range:
            p = (row_idx, col_idx)

            match h.get(p, ""), prev_corner:
                case "", _:
                    if parity == 1:
                        contained_tiles += 1
                case ("|", _) | ("J", "F") | ("7", "L"):
                    # if the current character is a J or 7, since we're scanning
                    # Left-to-right, we must have already encountered an F or L.
                    # Notice that a FJ or L7 is equivalent to a vertical line (but
                    # F7 and LJ is not), so change parity if we encounter those
                    # combinations.
                    parity ^= 1
                case ("F" | "L") as t, _:
                    prev_corner = t

    return contained_tiles


if __name__ == "__main__":
    data = parse(sys.argv[1])

    # print(part1(data))
    print(part2(data))
