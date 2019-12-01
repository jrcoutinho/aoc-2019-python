from typing import List


class RocketLaunch:
    """Aids the launch of Santa's rocket by providing fuel requirements.

    Args:
        modules (List[int]): List containing the masses of all modules to be launched.
    """

    def __init__(self, modules: List[int] = []):
        self.modules = modules

    def fuel_requirements(self, ignore_fuel_mass: bool = False) -> int:
        """Calculates the total fuel required, given a list of module masses.

        Args:
            ignore_fuel_mass (bool): If true, the fuel's mass does not incur
                the necessity of additional fuel.

        Returns:
            int: Total fuel requirements.
        """
        fuel_req = self._get_module_fuel if ignore_fuel_mass else self._get_fuel
        return sum(fuel_req(mass) for mass in self.modules)

    def _get_module_fuel(self, mass: int) -> int:
        """Calculates the required fuel to launch a module given its mass.

        Args:
            mass (int): The module's mass.

        Returns:
            int: Required fuel.
        """
        return mass // 3 - 2

    def _get_fuel(self, mass: int, ignore_fuel_mass: bool = False) -> int:
        """Similar to `_get_module_fuel`, but takes fuel mass into consideration."""
        fuel = mass // 3 - 2

        if fuel > 0:
            return fuel + self._get_fuel(fuel)
        else:
            return 0


if __name__ == "__main__":
    with open("data/day_01_modules.txt", "r") as f:
        modules = [int(mass) for mass in f.read().split("\n") if mass != ""]
        launch = RocketLaunch(modules)

        print("Challenge 1:")
        print(launch.fuel_requirements(ignore_fuel_mass=True))

        print("\n")
        print("Challenge 2:")
        print(launch.fuel_requirements())
