#! /usr/bin/env python3

from __future__ import annotations

import itertools
import math
import sys
from pathlib import Path
from pprint import pprint  # noqa: F401

import networkx as nx
import numpy as np


def parse(fname: str) -> list[str]:
    """Read from data file. Returns problem specific formatted data."""
    with Path(fname).open() as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    return np.array([[int(c) for c in line] for line in lines])


def construct_graph(h) -> nx.DiGraph:
    my, mx = h.shape

    edges = set()

    for y in range(my):
        for x in range(mx):
            # continue going right
            for step in range(1, 3):
                n = ((y, x + 1), (0, step + 1))
                c = ((y, x), (0, step))
                if x + 1 < mx and x - step >= 0:
                    edges.add((c, n))

            # continue going down
            for step in range(1, 3):
                n = ((y + 1, x), (1, step + 1))
                c = ((y, x), (1, step))
                if y + 1 < my and y - step >= 0:
                    edges.add((c, n))

            # continue going left
            for step in range(1, 3):
                n = ((y, x - 1), (2, step + 1))
                c = ((y, x), (2, step))
                if x - 1 >= 0 and x + step < mx:
                    edges.add((c, n))

            # continue going up
            for step in range(1, 3):
                n = ((y - 1, x), (3, step + 1))
                c = ((y, x), (3, step))
                if y - 1 >= 0 and y + step < my:
                    edges.add((c, n))

            # turn right, from going up/down
            if x + 1 < mx:
                for length in range(1, 4):
                    n = ((y, x + 1), (0, 1))

                    c = ((y, x), (1, length))
                    edges.add((c, n))
                    c = ((y, x), (3, length))
                    edges.add((c, n))

            # turn down, from going right/left
            if y + 1 < my:
                for length in range(1, 4):
                    n = ((y + 1, x), (1, 1))
                    edges.update([
                        (((y, x), (0, length)), n),
                        (((y, x), (2, length)), n),
                    ])

            # turn left, from going up/down
            if x - 1 >= 0:
                for length in range(1, 4):
                    n = ((y, x - 1), (2, 1))

                    c = ((y, x), (1, length))
                    edges.add((c, n))
                    c = ((y, x), (3, length))
                    edges.add((c, n))

            # turn up, from going right/left
            if y - 1 >= 0:
                for length in range(1, 4):
                    n = ((y - 1, x), (3, 1))
                    edges.update([
                        (((y, x), (0, length)), n),
                        (((y, x), (2, length)), n),
                    ])

    # g = nx.grid_2d_graph(*h.shape, create_using=nx.DiGraph)
    g = nx.DiGraph()

    # might overcount some edges. does this matter?
    for n1, n2 in edges:
        g.add_node(n1)
        g.add_node(n2)
    g.add_edges_from(edges)

    return g


def search(g, h) -> int:
    s_candidates = [
        ((0, 1), (0, 1)),
        ((1, 0), (1, 1)),
    ]

    # ending node coordinates
    y, x = h.shape
    e = (y - 1, x - 1)

    min_loss = math.inf

    for s in s_candidates:
        for l in itertools.product((0, 1), range(1, 4)):
            t = (e, l)
            path = nx.dijkstra_path(g, s, t, weight=lambda n1, n2, e: h[n1[0]])

            loss = sum(h[n[0]] for n in path)
            print(s, t, loss)
            min_loss = min(min_loss, loss)

    return min_loss


def part1(data) -> int:
    # this is not particularly fast, probably because i'm constructing the graph and calling
    # networkx in a dumb way. How am i supposed to encode the concept of a maximum length for
    # a path in one particular direction?
    g = construct_graph(data)
    return search(g, data)


def part2(data) -> int:
    print(data)
    return 0


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(part1(data))
    # print(part2(data))
