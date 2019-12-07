from typing import Optional, Tuple, List, Iterator

from itertools import chain


class CodeBreaker:
    """Helps generation of valid password given constraints.

    Args:
        length (int): The password length.
        valid_range (Tuple[str, str], optional): The range of possible passwords.
            If None, will check all from all possible passwords of length `length`.
    """
    def __init__(
        self, length: int, valid_range: Optional[Tuple[str, str]] = None,
    ) -> None:
        self.length = length
        self.valid_range = valid_range if valid_range else ("0" * length, "9" * length)

    def valid_passwords(self, strict: bool = False) -> List[str]:
        """Generates list of valid passwords, according to constraints.

        Args:
            strict (bool, optional): Set to True for more restrictive constraints.
                In this case`Defaults to False.

        Returns:
            List[str]: List of valid passwords.
        """
        if strict:
            return [
                pw for pw in self._generate_candidates()
                if self._is_non_dec(pw) and self._has_adj_strict(pw)
            ]
        else:
            return [
                pw for pw in self._generate_candidates()
                if self._is_non_dec(pw) and self._has_adj(pw)
            ]

    def _generate_candidates(self) -> Iterator:
        """Generates password candidates inside defined range."""
        adj_range = (
            max(int(self.valid_range[0]), int("1" * self.length)),
            int(self.valid_range[1]) + 1,
        )
        candidates = (str(x) for x in range(*adj_range))

        if int(self.valid_range[0]) == 0:
            # minor manual optimization
            return chain(["0" * self.length], candidates)
        else:
            return candidates

    def _is_non_dec(self, pw: str) -> bool:
        """Check if password is non-decreasing."""
        return pw == "".join(sorted(pw))

    def _has_adj(self, pw: str) -> bool:
        """Check if identical digits are adjacent to each other."""
        return any(pw[i] == pw[i + 1] for i in range(self.length - 1))

    def _has_adj_strict(self, pw: str) -> bool:
        """Check if at most two identical digits are adjacent to each other."""
        return any(
            pw[i] == pw[i + 1]
            and (i == self.length - 2 or pw[i] != pw[i + 2])
            and (i == 0 or pw[i] != pw[i - 1])
            for i in range(self.length - 1)
        )


if __name__ == "__main__":
    breaker = CodeBreaker(length=6, valid_range=("278384", "824795"))

    print("Challenge 1:")
    print(len(breaker.valid_passwords()))

    print("Challenge 2:")
    print(len(breaker.valid_passwords(strict=True)))
