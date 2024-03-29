#! /usr/bin/env python3

from __future__ import annotations

import sys
import typing
from pathlib import Path
from pprint import pprint  # noqa: F401

import networkx as nx
import numpy as np
import numpy.typing as npt

Point = tuple[int, int]


def parse(fname: str, p2: bool = False) -> npt.NDArray[np.unicode_]:
    """Read from data file. Returns problem specific formatted data."""
    with Path(fname).open() as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    arr = np.array([[c for c in line] for line in lines])

    if p2:
        # correct the input array
        # is there a nice numpy way to do this?
        hy, hx = arr.shape
        for y in range(hy):
            for x in range(hx):
                if arr[(y, x)] in "<>v^":
                    arr[(y, x)] = "."

    return arr


def manhattan(p1: Point, p2: Point) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def debug(data, path) -> None:
    h = data.copy()
    for p in path:
        h[p] = "O"

    for y in range(h.shape[0]):
        print("".join(h[y]))


def part1(data) -> int:
    print(data.shape)

    ry = range(data.shape[0])
    rx = range(data.shape[1])

    # always annoying with tuple(np.argwhere); `start` *is* a tuple[int, int]
    start = tuple(np.argwhere(data == ".")[0])
    assert start[0] == 0

    goal = tuple(np.argwhere(data == ".")[-1])
    assert goal[0] == data.shape[0] - 1

    def neighbors(p):
        slide_map = {
            "<": (0, -1),
            ">": (0, 1),
            "v": (1, 0),
            "^": (-1, 0),
        }
        match data[p]:
            case ("<" | ">" | "v" | "^") as slide:
                s = slide_map[slide]
                ny, nx = (p[0] + s[0], p[1] + s[1])
                if ny in ry and nx in rx and data[(ny, nx)] in ".<>v^":
                    yield (ny, nx)
            case ".":
                for s in [
                    (1, 0),
                    (0, 1),
                    (-1, 0),
                    (0, -1),
                ]:
                    ny, nx = (p[0] + s[0], p[1] + s[1])
                    if ny in ry and nx in rx and data[(ny, nx)] in ".<>v^":
                        yield (ny, nx)

    # D: D: D:
    # do something absolutely dumb to allow a quick DFS solution to work.
    # default 1k
    sys.setrecursionlimit(141 * 141)

    def dfs(
        node: Point, path: list[Point], depth: int = 0,
    ) -> typing.Generator[list[Point], None, None]:
        # print(f"{depth=}")
        if node == goal:
            yield [*path, node]

        for next_p in neighbors(node):
            if next_p not in path:
                yield from dfs(next_p, [*path, node], depth+1)

    return max(len(path) for path in dfs(start, [])) - 1


def neighbors(p: Point, g: nx.DiGraph) -> typing.Generator[Point, None, None]:
    for y, x in [
        (-1, 0),
        (0, -1),
        (1, 0),
        (0, 1),
    ]:
        ny, nx = (p[0] + y, p[1] + x)
        if (ny, nx) in g.nodes:
            yield (ny, nx)


def dfs(
    start: Point, g: nx.DiGraph, path: list[Point],
) -> typing.Generator[tuple[int, Point], None, None]:
    adj = dict(g.adjacency())
    for n in neighbors(start, g):
        if n != start and n not in path and len(adj[n]) != 2:
            yield len(path), n
        elif n != start and n not in path:
            yield from dfs(n, g, [*path, n])


def condense(g: nx.DiGraph) -> nx.DiGraph:
    adj = dict(g.adjacency())

    edges = []

    for u, _ in filter(lambda e: len(e[1]) != 2, adj.items()):
        for path_len, v in dfs(u, g, []):
            if v != u:
                edges.append((u, v, {"weight": path_len}))

    newg = nx.DiGraph()
    newg.add_edges_from(edges)
    return newg


def part2(data) -> int:

    g = nx.grid_2d_graph(*data.shape, create_using=nx.DiGraph)
    g.remove_edges_from([
        (a, b)
        for a, b in g.edges
        if "#" in (data[a], data[b])
    ])
    g.remove_nodes_from([
        n
        for n in g.nodes
        if data[n] == "#"
    ])

    # takes a while to condense the graph, because i'm doing it in a fairly naive way.
    g = condense(g)

    start = next(filter(lambda n: n[0] == 0, g.nodes))
    goal = max(g.nodes, key=lambda n: n[0])

    # naively iterating through all the simple paths that exist in the graph. takes a min or two.
    return max(
        sum(1 + g.edges[(u, v)]["weight"] for u, v in zip(path, path[1:]))
        for path in nx.all_simple_paths(g, start, goal)
    )


if __name__ == "__main__":
    data = parse(sys.argv[1])
    # print(part1(data))

    data = parse(sys.argv[1], True)
    print(part2(data))
