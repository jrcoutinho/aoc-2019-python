from __future__ import annotations
from typing import Union, Tuple


class IntcodeComputer:
    """Intcode computer that runs the provided program.

    Args:
        program (str): The intcode program. Has the form of a string
            of comma-separated integers.
    """

    def __init__(self, program: str = "") -> None:
        self.program = program

        self._opcodes = {
            1: self._op_sum,
            2: self._op_product,
            3: self._op_input,
            4: self._op_output,
            5: self._op_jump_true,
            6: self._op_jump_false,
            7: self._op_less_than,
            8: self._op_equals,
        }
        self._reset_memory()

    def execute(self) -> IntcodeComputer:
        """Runs the computer's program from its initial state."""
        self._reset_memory()

        pointer = 0
        modes, opcode = self._parse_op(pointer)

        while opcode != 99:
            try:
                # run instruction and get pointer move size
                move = self._opcodes[opcode](pointer, modes) + 1
            except KeyError as err:
                print(f"Opcode {opcode} not found! Instruction is invalid.")
                raise err

            pointer += move

            try:
                modes, opcode = self._parse_op(pointer)
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

    def _parse_op(self, address: int) -> Tuple[str, int]:
        """Parses operation to find the modes and opcode.

        Args:
            address (int): Memory address where operator information is located.

        Returns:
            Tuple[str, int]: Tuple containing the mode string and opcode integer.
        """
        op = str(self.memory[address])
        return op[:-2], int(op[-2:])

    def _op_sum(self, address: int, modes: str) -> int:
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

        *args, out = self.memory[address + 1 : address + n_params + 1]
        args = [
            self.memory[arg] if mode == "0" else arg
            for arg, mode in zip(args, modes.zfill(n_params - 1)[::-1])
        ]
        self.memory[out] = args[0] + args[1]

        return n_params

    def _op_product(self, address: int, modes: str) -> int:
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

        *args, out = self.memory[address + 1 : address + n_params + 1]
        args = [
            self.memory[arg] if mode == "0" else arg
            for arg, mode in zip(args, modes.zfill(n_params - 1)[::-1])
        ]
        self.memory[out] = args[0] * args[1]

        return n_params

    def _op_input(self, address: int, modes: str) -> int:
        n_params = 1
        self._validate_instruction(address, n_params)

        try:
            input_value = int(input())
        except ValueError:
            raise ValueError("Input must be an integer.")
        out = self.memory[address + 1]
        self.memory[out] = input_value

        return n_params

    def _op_output(self, address: int, modes: str) -> int:
        n_params = 1
        modes = modes.zfill(n_params)
        self._validate_instruction(address, n_params)

        out = self.memory[address + 1] if modes[0] == "0" else address + 1
        print(self.memory[out])

        return n_params

    def _op_jump_true(self, address: int, modes: str) -> int:
        n_params = 2
        self._validate_instruction(address, n_params)

        args = self.memory[address + 1 : address + n_params + 1]
        args = [
            self.memory[arg] if mode == "0" else arg
            for arg, mode in zip(args, modes.zfill(n_params)[::-1])
        ]

        return (args[1] - address - 1) if args[0] else n_params

    def _op_jump_false(self, address: int, modes: str) -> int:
        n_params = 2
        self._validate_instruction(address, n_params)

        args = self.memory[address + 1 : address + n_params + 1]
        args = [
            self.memory[arg] if mode == "0" else arg
            for arg, mode in zip(args, modes.zfill(n_params)[::-1])
        ]

        return (args[1] - address - 1) if not args[0] else n_params

    def _op_less_than(self, address: int, modes: str) -> int:
        n_params = 3
        self._validate_instruction(address, n_params)

        *args, out = self.memory[address + 1 : address + n_params + 1]
        args = [
            self.memory[arg] if mode == "0" else arg
            for arg, mode in zip(args, modes.zfill(n_params - 1)[::-1])
        ]
        self.memory[out] = 1 if args[0] < args[1] else 0

        return n_params

    def _op_equals(self, address: int, modes: str) -> int:
        n_params = 3
        self._validate_instruction(address, n_params)

        *args, out = self.memory[address + 1 : address + n_params + 1]
        args = [
            self.memory[arg] if mode == "0" else arg
            for arg, mode in zip(args, modes.zfill(n_params - 1)[::-1])
        ]
        self.memory[out] = 1 if args[0] == args[1] else 0

        return n_params

    def _validate_instruction(self, address: int, n_params: int) -> None:
        """Validates a given instruction based on the opcode's address.

        A valid instruction must have the necessary amount of parameters,
        according to the opcode.

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


if __name__ == "__main__":
    # day 02
    print("Day 02")
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

    print("\nDay 05")
    # day 05
    with open("data/day_05_intcode_program.txt", "r") as f:
        computer = IntcodeComputer(f.read())

        print("Challenge 1:")
        input = lambda: "1"  # monkey patched input function
        computer.execute()

        print("Challenge 2:")
        input = lambda: "5"  # monkey patched input function
        computer.execute()
