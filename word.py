import enum
import string
from typing import List, Sequence, Set, Tuple, Union

LETTERS = set(letter for letter in string.ascii_uppercase)


class Color(enum.Enum):
    """Enum for the letter colors

    black: not in the word
    yellow: in the word in the wrong position
    green: in the correct position
    """

    BLACK = enum.auto()
    YELLOW = enum.auto()
    GREEN = enum.auto()


class Word:
    def __init__(self, word_list: Set[str], word_length: int = 5) -> None:
        self._word_length = word_length
        self._available_words = word_list
        self._available_letters = tuple(set(LETTERS) for _ in range(self._word_length))
        self._known_letters: List[Union[Set[str], str]] = [
            set() for _ in range(word_length)
        ]

    def guess(
        self,
        guess: Sequence[Tuple[str, Color]],
    ) -> None:
        for idx, (letter, color) in enumerate(guess):
            if color is Color.YELLOW:
                self._add_possible(letter, idx)
            elif color is Color.GREEN:
                self._add_known(letter, idx)
            else:
                self._unavailable(letter)
        self._process_words()

    @property
    def available_words(self) -> Set[str]:
        return self._available_words

    def _add_possible(self, letter: str, idx: int) -> None:
        """Add the possible letter to all indices except the one it was in"""
        pass

    def _add_known(self, letter: str, position: int) -> None:
        self._known_letters[position] = letter

    def _unavailable(self, letter: str) -> None:
        pass

    def _process_words(self) -> None:
        for word in self._available_words.copy():
            if not all(letter in self._available_letters for letter in word):
                self._available_words.remove(word)
