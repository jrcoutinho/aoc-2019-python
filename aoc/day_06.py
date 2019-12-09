from typing import List

from functools import reduce


class OrbitMap:
    """Aids navigation using orbit maps.

    Args:
        orbits (str): String describing the orbitting relationships, in the form
            of "A)B", meaning 'B' orbits 'A'. Relationships are separated by line.
    """
    def __init__(self, orbits: str) -> None:
        self.map = self._parse_map(orbits)

    def count_orbits(self) -> int:
        """Counts the number of direct and indirect orbits.

        Returns:
            int: Number of orbits.
        """
        return sum(len(path) - 1 for path in self.map)

    def shortest_path(self, begin: str, end: str) -> int:
        """Finds the length of the shortest path between two objects.

        This distance is the number of orbital jumps between the object
        "begin" is orbitting to the object "end" is orbitting.

        Args:
            begin, end (str): Reference objects to calculate distance.

        Returns:
            int: Distance in orbital jumps.
        """
        endpoints = [begin, end]
        paths = [path for path in self.map if path[-1] in endpoints]

        if set(endpoints) != {path[-1] for path in paths}:
            raise ValueError(
                f"Both {begin} and {end} need to exist as objects in the orbit map!"
            )

        total_depth = sum(len(path) - 1 for path in paths)
        common_path = len(reduce(lambda x, y: set(x) & set(y), paths))

        return total_depth - 2 * common_path

    def _parse_map(self, orbits: str) -> List[List[str]]:
        """Parses orbit map from string to list of orbit chains."""
        pairs = [orbit.split(")") for orbit in orbits.split("\n")]

        paths = [["COM"]]
        while pairs:
            path_ends = [path[-1] for path in paths]
            to_add = [pair for pair in pairs if pair[0] in path_ends]

            paths.extend(
                [
                    path + [new[1]]
                    for path in paths
                    for new in to_add
                    if new[0] == path[-1]
                ]
            )

            pairs = [pair for pair in pairs if pair not in to_add]

        return paths


if __name__ == "__main__":
    with open("data/day_06_orbits.txt", "r") as f:
        orbits = f.read()
        orbit_map = OrbitMap(orbits)

        print("Challenge 1:")
        print(orbit_map.count_orbits())

        print("Challenge 2:")
        print(orbit_map.shortest_path("YOU", "SAN"))
