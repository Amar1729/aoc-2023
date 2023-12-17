#! /usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path
from pprint import pprint  # noqa: F401

import networkx as nx
import numpy as np
import numpy.typing as npt


def parse(fname: str) -> npt.NDArray[np.uint8]:
    """Read from data file. Returns problem specific formatted data."""
    with Path(fname).open() as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    return np.array([[int(c) for c in line] for line in lines]).astype(np.uint8)


def construct_graph(h, p2: bool=False) -> nx.DiGraph:
    my, mx = h.shape

    edges = set()

    max_path = 10 if p2 else 3
    min_path = 4 if p2 else 0

    for y in range(my):
        for x in range(mx):
            for step in range(1, max_path):
                # continue going right
                n = ((y, x + 1), (0, step + 1))
                c = ((y, x), (0, step))
                if x + 1 < mx and x - step >= 0:
                    edges.add((c, n))

                # continue going down
                n = ((y + 1, x), (1, step + 1))
                c = ((y, x), (1, step))
                if y + 1 < my and y - step >= 0:
                    edges.add((c, n))

                # continue going left
                n = ((y, x - 1), (2, step + 1))
                c = ((y, x), (2, step))
                if x - 1 >= 0 and x + step < mx:
                    edges.add((c, n))

                # continue going up
                n = ((y - 1, x), (3, step + 1))
                c = ((y, x), (3, step))
                if y - 1 >= 0 and y + step < my:
                    edges.add((c, n))

            for length in range(min_path, max_path + 1):
                # turn right, from going up/down
                if x + 1 < mx and y - length >= 0:
                    n = ((y, x + 1), (0, 1))
                    c = ((y, x), (1, length))
                    edges.add((c, n))
                if x + 1 < mx and y + length < my:
                    n = ((y, x + 1), (0, 1))
                    c = ((y, x), (3, length))
                    edges.add((c, n))

                # turn down, from going right/left
                if y + 1 < my and x - length >= 0:
                    n = ((y + 1, x), (1, 1))
                    c = ((y, x), (0, length))
                    edges.add((c, n))
                if y + 1 < my and x + length < mx:
                    n = ((y + 1, x), (1, 1))
                    c = ((y, x), (2, length))
                    edges.add((c, n))

                # turn left, from going up/down
                if x - 1 >= 0 and y - length >= 0:
                    n = ((y, x - 1), (2, 1))
                    c = ((y, x), (1, length))
                    edges.add((c, n))
                if x - 1 >= 0 and y + length < my:
                    n = ((y, x - 1), (2, 1))
                    c = ((y, x), (3, length))
                    edges.add((c, n))

                # turn up, from going right/left
                if y - 1 >= 0 and x - length >= 0:
                    n = ((y - 1, x), (3, 1))
                    c = ((y, x), (0, length))
                    edges.add((c, n))
                if y - 1 >= 0 and x + length < mx:
                    n = ((y - 1, x), (3, 1))
                    c = ((y, x), (2, length))
                    edges.add((c, n))

    g = nx.DiGraph()

    for n1, n2 in edges:
        g.add_node(n1)
        g.add_node(n2)
    g.add_edges_from(edges)

    # special case: add start and end nodes.
    g.add_edge(((0, 0), (-1, -1)), ((0, 1), (0, 1)))
    g.add_edge(((0, 0), (-1, -1)), ((1, 0), (1, 1)))
    h[(0, 0)] = 0

    e = (my - 1, mx - 1)
    new_edges = [
        (node, (e, (-1, -1)))
        for node in filter(lambda n_l: n_l[0] == e and n_l[1][1] >= min_path, g.nodes)
    ]
    g.add_edges_from(new_edges)

    return g


def debug(h, path) -> None:
    hc = h.astype("U")
    red = "\033[31m"  # ]
    noc = "\033[0m"  # ]

    for n, (d, _) in path:
        match d:
            case 0:
                hc[n] = red + ">" + noc
            case 1:
                hc[n] = red + "v" + noc
            case 2:
                hc[n] = red + "<" + noc
            case 3:
                hc[n] = red + "^" + noc

    for line in hc:
        print("".join(line))


def search(g, h) -> int:
    # ending node coordinates
    y, x = h.shape
    e = (y - 1, x - 1)

    start = ((0, 0), (-1, -1))
    end = (e, (-1, -1))

    print(start, end)
    path = nx.dijkstra_path(g, start, end, weight=lambda n1, n2, e: h[n1[0]])
    return sum(h[n[0]] for n in path) - h[path[-1][0]]


def part1(data) -> int:
    g = construct_graph(data)
    return search(g, data)


def part2(data) -> int:
    g = construct_graph(data, p2=True)
    return search(g, data)


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(part1(data))
    print(part2(data))
