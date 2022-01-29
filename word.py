import enum
import string
from typing import Any, List, Sequence, Set, Tuple

LETTERS = set(letter for letter in string.ascii_uppercase)


class BlackLetterError(Exception):
    """Exception to be called when trying to change a black letter to yellow or green"""

    def __init__(self, letter: str, color: str, *args: Any, **kwargs: Any) -> None:
        self.letter = letter
        self.color = color.upper()
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        return f"'{self.letter}' can not be changed from BLACK to {self.color}"


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
        self._available_letters = {
            letter: [idx for idx in range(self._word_length)] for letter in LETTERS
        }
        self._known_letters = ["" for _ in range(self._word_length)]

    def guess(
        self,
        guess: Sequence[Tuple[str, Color]],
    ) -> None:
        for idx, (letter, color) in enumerate(guess):
            if color is Color.YELLOW:
                self._add_possible_letter(letter, idx)
            elif color is Color.GREEN:
                self._add_known_letter(letter, idx)
            else:
                self._unavailable_letter(letter)
        self._process_words()

    @property
    def available_words(self) -> Set[str]:
        return self._available_words

    @property
    def known_letters(self) -> str:
        """Returns a string of the known letters.

        i.e. if O is known to be in the 2nd and 4th positions (like ROBOT)
        returns _O_O_
        """
        known: List[str] = []
        for letter in self._known_letters:
            if letter:
                known.append(letter)
            else:
                known.append("_")
        return "".join(known)

    def _remove_position(self, letter_list: List[int], position: int):
        """Removes the possible position for a letter"""
        if position in letter_list:
            letter_list.remove(position)

    def _add_possible_letter(self, letter: str, position: int) -> None:
        """Remove the available index in the position of the yellow letter"""
        letter_list = self._available_letters[letter]
        if not letter_list:
            raise BlackLetterError(letter, "YELLOW")
        self._remove_position(letter_list, position)
        for idx, let in enumerate(self._known_letters):
            if let:
                self._remove_position(letter_list, idx)

    def _add_known_letter(self, letter: str, position: int) -> None:
        """Sets the known letters' position and the available letters list to those positions"""
        if not self._available_letters[letter]:
            raise BlackLetterError(letter, "GREEN")
        self._known_letters[position] = letter
        self._available_letters[letter] = [
            pos for pos, let in enumerate(self._known_letters) if let == letter
        ]
        for unknown, unknown_postions in self._available_letters.items():
            if unknown == letter:
                continue
            self._remove_position(unknown_postions, position)

    def _unavailable_letter(self, letter: str) -> None:
        """Removes all positions from the available letters"""
        self._available_letters[letter] = []

    def _process_words(self) -> None:
        unavailable = [let for let, pos in self._available_letters.items() if not pos]
        for word in self._available_words.copy():
            if any(letter in unavailable for letter in word):
                self._available_words.remove(word)
