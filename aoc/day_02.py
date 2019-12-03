from __future__ import annotations
from typing import Union


class IntcodeComputer:
    """Intcode computer that runs the provided program.

    Args:
        program (str): The intcode program. Has the form of a string
            of comma-separated integers.
    """

    def __init__(self, program: str = "") -> None:
        self.program = program

        self._op_codes = {
            1: self._op_sum,
            2: self._op_product,
        }
        self._reset_memory()

    def execute(self) -> IntcodeComputer:
        """Runs the computer's program from its initial state."""
        self._reset_memory()

        pointer = 0
        opcode = self.memory[pointer]

        while opcode != 99:
            try:
                # run instruction and get pointer move size
                move = self._op_codes[opcode](pointer) + 1
            except KeyError as err:
                print(f"Opcode {opcode} not found! Instruction is invalid.")
                raise err

            pointer += move

            try:
                opcode = self.memory[pointer]
            except IndexError as err:
                print("Program has no halt opcode (99) at its end!")
                raise err

        return self

    def change_inputs(
        self, noun: Union[int, str], verb: Union[int, str]
    ) -> IntcodeComputer:
        """Changes the program's inputs permanently.

        The inputs are the integers located in addresses 1 and 2 (noun and verb,
        respectively).

        Args:
            noun, verb (int): New inputs that will update the program.
        """
        program = [x for x in self.program.split(",")]
        program[1:3] = [str(noun), str(verb)]
        self.program = ",".join(program)

        return self

    def _reset_memory(self) -> None:
        """Sets computer's memory back to its initial state."""
        self.memory = [int(x) for x in self.program.split(",")]

    def _op_sum(self, address: int) -> int:
        """Sum opcode.

        Sums the integers located in the addresses indicated by the
        first two parameters, then save the results in the address
        indicated by the third parameter.

        Args:
            address (int): Address of the opcode. Position of the parameters
                will be relative to this address.

        Returns:
            (int) Number of parameters used by opcode.
        """
        n_params = 3
        self._validate_instruction(address, n_params)

        arg_1, arg_2, out = self.memory[address + 1 : address + n_params + 1]
        self.memory[out] = self.memory[arg_1] + self.memory[arg_2]

        return n_params

    def _op_product(self, address: int) -> int:
        """Product opcode.

        Calculates the product of the integers located in the addresses
        indicated by the first two parameters, then save the results in
        the address indicated by the third parameter.

        Args:
            address (int): Address of the opcode. Position of the parameters
                will be relative to this address.

        Returns:
            (int) Number of parameters used by opcode.
        """
        n_params = 3
        self._validate_instruction(address, n_params)

        arg_1, arg_2, out = self.memory[address + 1 : address + n_params + 1]
        self.memory[out] = self.memory[arg_1] * self.memory[arg_2]

        return n_params

    def _validate_instruction(self, address: int, n_params: int) -> None:
        """Validates a given instruction based on the opcode's address.

        A valid instruction must have:
            1. The necessary amount of parameters, according to the opcode.
            2. The parameters must point to existing addresses in the computer's
                memory.

        Args:
            address (int): Instruction's opcode address
            n_params (int): Number of expected parameters following the opcode.
        """
        mem_size = len(self.memory)

        if address + n_params >= mem_size:
            raise IndexError(
                f"Operator in address {address} does not have "
                f"{n_params} integers after it to serve as its parameters."
            )

        invalid_params = [
            str(param)
            for param in self.memory[address + 1 : address + n_params + 1]
            if param >= mem_size
        ]
        if invalid_params:
            raise IndexError(
                f"Memory does not contain addresses {', '.join(invalid_params)}"
            )


if __name__ == "__main__":
    with open("data/day_02_intcode_program.txt", "r") as f:
        computer = IntcodeComputer(f.read())

        print("Challenge 1:")
        computer.change_inputs(noun=12, verb=2).execute()
        print(computer.memory[0])

        print("Challenge 2:")
        for noun, verb in ((x, y) for x in range(0, 100) for y in range(0, 100)):
            computer.change_inputs(noun, verb).execute()
            if computer.memory[0] == 19690720:
                print(noun * 100 + verb)
                break
