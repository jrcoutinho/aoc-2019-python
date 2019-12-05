from __future__ import annotations

from typing import List
from functools import reduce


class WireIntersections:
    """Supports identification of path intersections for a list of wires.

    Args:
        wires (List[List[str]]): List of wire paths. Each path is a list of
            instructions in the form of <direction><number of steps>,
            where direction is one of right ('R'), left ('L'), up ('U')
            or down ('D'). Example: ['R4', 'U3', 'D10'].
    """

    def __init__(self, wires: List[List[str]]) -> None:
        self._draw_paths(wires)

    def find_closest(self) -> int:
        """Calculates the smallest distance from the origin to an intersection."""
        intersections = reduce(lambda x, y: set(x) & set(y), self.coords)
        return min(self._manhattan(i) for i in intersections)

    def find_shortest(self) -> int:
        """Calculates the shortest path to an intersection."""
        intersections = reduce(lambda x, y: set(x) & set(y), self.coords)
        return min(
            sum(wire_path.index(i) + 1 for wire_path in self.coords)
            for i in intersections
        )

    def _draw_paths(self, wires: List[List[str]]) -> None:
        """Draws the wire paths as an ordered list of grid coordinates."""
        pos = complex  # position vector alias
        dirs = {
            "R": pos(0, 1),
            "L": pos(0, -1),
            "U": pos(1, 0),
            "D": pos(-1, 0),
        }

        # generates list of coordinates where wires passed through
        coords = []
        for wire in wires:
            wire_path = []
            current = pos(0, 0)
            for d, *steps in wire:
                steps = int("".join(steps))
                wire_path.extend([current + dirs[d] * i for i in range(1, steps + 1)])
                current = wire_path[-1]
            coords.append(wire_path)

        self.coords = coords

    @staticmethod
    def _manhattan(position: complex) -> int:
        """Calculates the manhattan distance of a 2D coordinate vector."""
        return int(abs(position.real) + abs(position.imag))


if __name__ == "__main__":
    with open("data/day_03_wires.txt", "r") as f:
        wires = [wire.split(",") for wire in f.read().split("\n")]
        wire_intersections = WireIntersections(wires)

        print("Challenge 1:")
        print(wire_intersections.find_closest())

        print("Challenge 2:")
        print(wire_intersections.find_shortest())
