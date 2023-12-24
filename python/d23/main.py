#! /usr/bin/env python3

from __future__ import annotations

# commonly-used built-in imports. not all of these are necessarily used each day.
import collections
import functools
import heapq
import itertools
import re
import sys
import typing
from pathlib import Path
from pprint import pprint  # noqa: F401

import numpy as np

# see parent directory
# from aoc_tools import *


def parse(fname: str) -> list[str]:
    """Read from data file. Returns problem specific formatted data."""
    with Path(fname).open() as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    return np.array([[c for c in line] for line in lines])


def manhattan(p1, p2) -> int:
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

    def dfs(node: tuple[int, int], path: list[tuple[int, int]], depth=0):  # generator?
        # print(f"{depth=}")
        if node == goal:
            yield [*path, node]

        for next_p in neighbors(node):
            if next_p not in path:
                yield from dfs(next_p, [*path, node], depth+1)

    # paths = dfs(start, [])
    # print("DFS")
    # for path in paths:
    #     print("----" * 10)
    #     print(len(path))
    #     debug(data, path)
    #     print("----" * 10)

    return max(len(path) for path in dfs(start, [])) - 1

    q = [(-manhattan(start, goal), start)]

    # keep track of visited nodes and the paths to reach them
    visited = {start: [start]}

    # keep track of just visited nodes
    # since we're doing BFS we don't have to keep track of path?
    # visited = set([start])

    print(f"{start=} {goal=}")

    while q:
        distance, curr = heapq.heappop(q)
        distance *= -1

        print(f"Popped: {distance=} {curr=}")

        if curr == goal:
            # found goal! (and i think this is guaranteed to be longest path?)
            break

        for next_p in neighbors(curr):
            print(f"Visiting neighbor: {next_p=} {data[next_p]} {next_p in visited}")
            if next_p in visited:
                # update info if necessary
                if len(visited[curr]) + 1 > len(visited[next_p]):
                    visited[next_p] = visited[curr] + [next_p]
                    # heapq.heappush(q, (-manhattan(next_p, goal), next_p))
            else:
                # visit neighbors of next_p, searching for goal
                heapq.heappush(q, (-manhattan(next_p, goal), next_p))
                visited[next_p] = visited[curr] + [next_p]

    # pprint(visited[goal])
    debug(data, visited[goal])
    return len(visited[goal])


def part2(data) -> int:
    print(data)
    return 0


if __name__ == "__main__":
    data = parse(sys.argv[1])

    print(part1(data))
    # print(part2(data))
