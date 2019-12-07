from aoc.day_04 import CodeBreaker


def test_valid():
    breaker = CodeBreaker(6)

    valid = breaker.valid_passwords()
    assert "111111" in valid
    assert "223450" not in valid
    assert "123789" not in valid

    valid = breaker.valid_passwords(strict=True)
    assert "112233" in valid
    assert "123444" not in valid
    assert "111122" in valid
