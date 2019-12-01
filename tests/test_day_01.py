from aoc.day_01 import RocketLaunch


def test_ex_01():
    launch = RocketLaunch()
    assert launch._get_module_fuel(12) == 2
    assert launch._get_fuel(12) == 2


def test_ex_02():
    launch = RocketLaunch()
    assert launch._get_module_fuel(14) == 2
    assert launch._get_fuel(14) == 2


def test_ex_03():
    launch = RocketLaunch()
    assert launch._get_module_fuel(1969) == 654
    assert launch._get_fuel(1969) == 966


def test_ex_04():
    launch = RocketLaunch()
    assert launch._get_module_fuel(100756) == 33583
    assert launch._get_fuel(100756) == 50346


def test_total():
    modules = [12, 14, 1969, 100756]
    launch = RocketLaunch(modules)

    expected_total = 2 + 2 + 654 + 33583
    assert launch.fuel_requirements(ignore_fuel_mass=True) == expected_total

    expected_total = 2 + 2 + 966 + 50346
    assert launch.fuel_requirements() == expected_total
