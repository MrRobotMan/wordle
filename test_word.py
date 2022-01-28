import string
import unittest

import word


class TestWordle(unittest.TestCase):
    def setUp(self) -> None:
        with open("words.txt", "r") as f:
            word_list = set(line.strip() for line in f)
        self.wordle = word.Word(word_list, 5)

    def test_class_creation(self) -> None:
        self.assertIn("LINER", self.wordle.available_words)
        self.assertEqual(len(self.wordle._available_letters), self.wordle._word_length)  # type: ignore
        self.assertSetEqual(
            set(string.ascii_uppercase), self.wordle._available_letters[0]  # type: ignore
        )
        self.assertEqual(len(self.wordle._known_letters), self.wordle._word_length)  # type: ignore
        self.assertSetEqual(set(), self.wordle._known_letters[0])  # type: ignore

    def test_found_letter(self) -> None:
        guess = "LINER"
        self.wordle.guess(
            [
                ("L", word.Color.BLACK),
                ("I", word.Color.BLACK),
                ("N", word.Color.BLACK),
                ("E", word.Color.YELLOW),
                ("R", word.Color.GREEN),
            ]
        )
        self.assertNotIn(guess, self.wordle.available_words)
        self.assertEqual("R", self.wordle._known_letters[4])  # type: ignore
        self.assertIn("E", self.wordle._available_letters[0])  # type: ignore
        self.assertIn("E", self.wordle._available_letters[1])  # type: ignore
        self.assertIn("E", self.wordle._available_letters[2])  # type: ignore
        self.assertNotIn("E", self.wordle._available_letters[3])  # type: ignore
        self.assertNotIn("E", self.wordle._available_letters[4])  # type: ignore


if __name__ == "__main__":
    unittest.main()
