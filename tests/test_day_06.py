from aoc.day_06 import OrbitMap


def test_count():
    orbits = (
        "COM)B\n"
        "B)C\n"
        "C)D\n"
        "D)E\n"
        "E)F\n"
        "B)G\n"
        "G)H\n"
        "D)I\n"
        "E)J\n"
        "J)K\n"
        "K)L"
    )
    orbit_map = OrbitMap(orbits)

    assert orbit_map.count_orbits() == 42


def test_path():
    orbits = (
        "COM)B\n"
        "B)C\n"
        "C)D\n"
        "D)E\n"
        "E)F\n"
        "B)G\n"
        "G)H\n"
        "D)I\n"
        "E)J\n"
        "J)K\n"
        "K)L\n"
        "K)YOU\n"
        "I)SAN"
    )
    orbit_map = OrbitMap(orbits)

    assert orbit_map.shortest_path("YOU", "SAN") == 4
