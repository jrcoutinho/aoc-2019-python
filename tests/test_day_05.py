from aoc.day_02 import IntcodeComputer


def _run_test(program, expected):
    computer = IntcodeComputer(program).execute()
    assert ",".join(str(x) for x in computer.memory) == expected


def test_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda: "1")

    program = "3,0,99"
    expected = "1,0,99"
    _run_test(program, expected)


def test_output(capfd):
    program = "4,0,99"
    IntcodeComputer(program).execute()

    captured = capfd.readouterr()
    assert captured.out == "4\n"


def test_ex01():
    program = "1002,4,3,4,33"
    expected = "1002,4,3,4,99"
    _run_test(program, expected)


def _test_in_out(comp, in_val, out_val, monkeypatch, capfd):
    monkeypatch.setattr("builtins.input", lambda: in_val)
    comp.execute()
    captured = capfd.readouterr()
    assert captured.out == f"{out_val}\n"


def test_ex02(monkeypatch, capfd):
    program = "3,9,8,9,10,9,4,9,99,-1,8"
    comp = IntcodeComputer(program)

    _test_in_out(comp, 8, 1, monkeypatch, capfd)
    _test_in_out(comp, 1, 0, monkeypatch, capfd)


def test_ex03(monkeypatch, capfd):
    program = "3,9,7,9,10,9,4,9,99,-1,8"
    comp = IntcodeComputer(program)

    _test_in_out(comp, 7, 1, monkeypatch, capfd)
    _test_in_out(comp, 9, 0, monkeypatch, capfd)


def test_ex04(monkeypatch, capfd):
    program = "3,3,1108,-1,8,3,4,3,99"
    comp = IntcodeComputer(program)

    _test_in_out(comp, 8, 1, monkeypatch, capfd)
    _test_in_out(comp, 1, 0, monkeypatch, capfd)


def test_ex05(monkeypatch, capfd):
    program = "3,3,1107,-1,8,3,4,3,99"
    comp = IntcodeComputer(program)

    _test_in_out(comp, 7, 1, monkeypatch, capfd)
    _test_in_out(comp, 8, 0, monkeypatch, capfd)


def test_ex06(monkeypatch, capfd):
    program = "3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9"
    comp = IntcodeComputer(program)

    _test_in_out(comp, 0, 0, monkeypatch, capfd)
    _test_in_out(comp, 1, 1, monkeypatch, capfd)


def test_ex07(monkeypatch, capfd):
    program = "3,3,1105,-1,9,1101,0,0,12,4,12,99,1"
    comp = IntcodeComputer(program)

    _test_in_out(comp, 0, 0, monkeypatch, capfd)
    _test_in_out(comp, 1, 1, monkeypatch, capfd)


def test_ex08(monkeypatch, capfd):
    program = (
        "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,"
        "1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,"
        "999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
    )
    comp = IntcodeComputer(program)

    _test_in_out(comp, 7, 999, monkeypatch, capfd)
    _test_in_out(comp, 8, 1000, monkeypatch, capfd)
    _test_in_out(comp, 9, 1001, monkeypatch, capfd)
