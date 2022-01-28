import string
from typing import Optional, Sequence, Set, Tuple, Union

LETTERS = set(letter for letter in string.ascii_uppercase)


class Wordle:
    def __init__(self) -> None:
        with open("words.txt") as f:
            self._available_words = set(line.strip() for line in f)
        self._available_letters = tuple(LETTERS.copy() for _ in range(5))
        self._known_letters: Tuple[Union[Set[str], str], ...] = (
            set(),
            set(),
            set(),
            set(),
            set(),
        )

    def guess(
        self,
        guess: str,
        yellow: Sequence[str] = "",
        green: Sequence[str] = "",
    ) -> None:
        guess = guess.upper()
        for idx, letter in enumerate(guess):
            if letter in yellow:
                self._add_possible(letter)
            elif letter in green:
                self._add_known(letter, idx)
            else:
                self._unavailable(letter)
        self._process_words()

    def _add_possible(self, letter: str) -> None:
        pass

    def _add_known(self, letter: str, position: int) -> None:
        pass

    def _unavailable(self, letter: str) -> None:
        pass

    def _process_words(self) -> None:
        for word in self._available_words.copy():
            if not all(letter in self._available_letters for letter in word):
                self._available_words.remove(word)


def main() -> None:
    wordle = Wordle()


if __name__ == "__main__":
    main()
