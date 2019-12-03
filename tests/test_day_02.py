from aoc.day_02 import IntcodeComputer
import pytest


def _run_test(program, expected):
    computer = IntcodeComputer(program).execute()
    assert ",".join(str(x) for x in computer.memory) == expected


def test_ex01():
    program = "1,9,10,3,2,3,11,0,99,30,40,50"
    expected = "3500,9,10,70,2,3,11,0,99,30,40,50"
    _run_test(program, expected)


def test_ex02():
    program = "1,0,0,0,99"
    expected = "2,0,0,0,99"
    _run_test(program, expected)


def test_ex03():
    program = "2,3,0,3,99"
    expected = "2,3,0,6,99"
    _run_test(program, expected)


def test_ex04():
    program = "2,4,4,5,99,0"
    expected = "2,4,4,5,99,9801"
    _run_test(program, expected)


def test_ex05():
    program = "1,1,1,4,99,5,6,0,99"
    expected = "30,1,1,4,2,5,6,0,99"
    _run_test(program, expected)


def test_invalid_instruction():
    program = "1,0,0"
    with pytest.raises(IndexError):
        IntcodeComputer(program).execute()


def test_invalid_addresses():
    program = "1,10,20,30"
    with pytest.raises(IndexError):
        IntcodeComputer(program).execute()


def test_no_halt():
    program = "1,0,0,1"
    with pytest.raises(IndexError):
        IntcodeComputer(program).execute()
