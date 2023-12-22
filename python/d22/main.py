#! /usr/bin/env python3

from __future__ import annotations

import itertools
import sys
from pathlib import Path
from pprint import pprint  # noqa: F401

Point = tuple[tuple[int, int, int], str]


def parse(fname: str) -> list[set[Point]]:
    """Read from data file. Returns problem specific formatted data."""
    with Path(fname).open() as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    # sort bricks by minimum z coord
    # TODO: i want to zip this somehow with string.ascii_uppercase to have nice labels...
    return sorted(
        list(itertools.starmap(parse_brick, enumerate(lines))),
        key=lambda ps: min(p[0][2] for p in ps),
    )


def parse_brick(idx: int, line: str) -> set[Point]:
    start, end = line.split("~")

    sx, sy, sz = map(int, start.split(","))
    ex, ey, ez = map(int, end.split(","))

    return set(
        [
            ((x, y, z), str(idx))
            for x in range(sx, ex + 1)
            for y in range(sy, ey + 1)
            for z in range(sz, ez + 1)
        ],
    )


def shift_brick(brick: set[Point]) -> set[Point]:
    return set(
        map(
            lambda p: (
                (
                    p[0][0],
                    p[0][1],
                    p[0][2] - 1,
                ),
                p[1],
            ),
            brick,
        ),
    )


def part1(data, p2: bool) -> int | dict[str, list[str]]:
    # anything that settles onto the ground gets added here, for easier cmp
    settled: dict[tuple[int, int, int], str] = {}

    def find_bricks_below(brick: set[tuple[int, int, int]]) -> set[str]:
        points_below = {
            (bp[0], bp[1], bp[2] - 1)
            for bp in brick
            if (bp[0], bp[1], bp[2] - 1) in settled
        }

        # print(f"For {label}, found: {points_below=}")
        if not any(p[2] == 1 for p in brick):
            assert len(points_below) > 0, (label, brick)

        return set([
            settled[p]
            for p in points_below
            # don't count ourselves, if a vertical brick.
            if settled[p] != label
        ])

    while data:
        brick = data.pop(0)

        orig_brick = brick.copy()

        while True:
            if any(p[0][2] == 1 for p in brick):
                # if any(p[2] == 1 for p in brick):
                # TODO: actually track the brick somehow?
                # not sure how yet.
                # maybe numpy array with labels,
                # or maybe settled should be a dict?
                # settled |= set(p for p in brick)
                settled.update({p[0]: p[1] for p in brick})
                break

            # new_brick = set(map(lambda p: (p[0], p[1], p[2] - 1), brick))
            new_brick = shift_brick(brick)

            # if any(p in settled for p in new_brick) or any(p[2] == 1 for p in new_brick):
            if any(p[0] in settled for p in new_brick):
                # add the old brick (we've shifted down too far)
                for point, label in brick:
                    assert point not in settled, (label, point)
                    settled[point] = label
                break
            if any(p[0][2] == 1 for p in new_brick):
                # add the new brick (we've hit ground)
                # settled |= set(p for p in brick)
                # settled.update({p[0]: p[1] for p in new_brick})
                for point, label in new_brick:
                    assert point not in settled, (label, point)
                    settled[point] = label
                break

            brick = new_brick

        # print(f"Settled brick: {orig_brick}")
        # print(f"At coords:     {brick}")
        # print()

    # check which bricks have bricks above them:
    # for efficiency, i could probably create a tree-like DS.
    # however i don't think it'll be necessary for this problem?

    disintegrate_check: dict[str, bool] = {}

    support_graph: dict[str, list[str]] = {}

    it = sorted(
        set(settled.items()),
        key=lambda i: i[0][2],
    )

    # for label in sorted(set(settled.values())):
    for _, label in it:
        brick = {p for p in settled if settled[p] == label}
        # print(f"Brick {label}: {brick}")

        # assume any brick is a leaf (can be disintegrated).
        # will be set to False later if this is not true.
        disintegrate_check[label] = True

        bricks_below = find_bricks_below(brick)

        if not any(p[2] == 1 for p in brick):
            assert len(bricks_below) > 0

        # print(f"bricks below brick {label}:", bricks_below)

        # kind of gross tbh
        support_graph[label] = list(bricks_below)

        if len(bricks_below) == 1:
            # the below brick has at least one brick (this one)
            # that only has it as a support. can't disintegrate.
            disintegrate_check[bricks_below.pop()] = False
        else:
            for below in bricks_below:
                # don't overwrite any possible False values already in here.
                if below not in disintegrate_check:
                    disintegrate_check[below] = True

    if p2:
        return support_graph

    return sum(disintegrate_check.values())


def part2(data) -> int:
    # i really need to figure out how to nicely type-narrow with boolean arguments ...?
    supporting_graph = part1(data, True)
    assert isinstance(supporting_graph, dict)

    would_fall = 0

    # gross. put together an easier way to iterate through "bricks above <label>"
    supported: dict[str, set[str]] = {}
    for label, deps in supporting_graph.items():
        if label not in supported:
            supported[label] = set()
        for dep in deps:
            if dep not in supported:
                supported[dep] = set()

            supported[dep].add(label)

    # walk through dep graph. mark a node as visited (in would_dis set), then check its
    # dependents. If everything a brick rests on is in would_dis, it will also disintegrate.
    for label, above in supported.items():
        would_dis = set([label])
        q = list(above.copy())
        while q:
            curr = q.pop(0)
            if all(brick in would_dis for brick in supporting_graph[curr]):
                q.extend(supported[curr])
                would_dis.update([curr])

        would_fall += len(would_dis) - 1

    return would_fall


if __name__ == "__main__":
    data = parse(sys.argv[1])

    # print(part1(data))
    print(part2(data))
