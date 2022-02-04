import unittest

import app
import word


class TestWordle(unittest.TestCase):
    word_list = app.get_words(app.WORDS_FILE)

    def setUp(self) -> None:
        self.wordle = word.Word(self.word_list, 5)

    def test_class_creation(self) -> None:
        self.assertIn("LINER", self.wordle.available_words)

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
        self.assertListEqual([], self.wordle._available_letters["L"])  # type: ignore
        self.assertIn(4, self.wordle._available_letters["R"])  # type: ignore
        self.assertListEqual([0, 1, 2], self.wordle._available_letters["E"])  # type: ignore
        self.assertEqual("____R", self.wordle.known_letters)

    def test_double_green_letter(self) -> None:
        self.wordle.guess(
            [
                ("R", word.Color.BLACK),
                ("O", word.Color.GREEN),
                ("B", word.Color.BLACK),
                ("O", word.Color.GREEN),
                ("T", word.Color.BLACK),
            ]
        )
        self.assertIn(1, self.wordle._available_letters["O"])  # type: ignore
        self.assertIn(3, self.wordle._available_letters["O"])  # type: ignore
        self.assertEqual("_O_O_", self.wordle.known_letters)

    def test_green_black_letter(self) -> None:
        self.wordle.guess(
            [
                ("L", word.Color.GREEN),
                ("I", word.Color.GREEN),
                ("M", word.Color.BLACK),
                ("I", word.Color.BLACK),
                ("T", word.Color.GREEN),
            ]
        )
        self.assertEqual("LI__T", self.wordle.known_letters)
        self.assertEqual(1, len(self.wordle.available_words))

    def test_change_black_to_green_or_yellow(self) -> None:
        """Tests that an exception is raised if a letter changes from black to green or yellow."""
        self.wordle.guess(
            [
                ("R", word.Color.BLACK),
                ("O", word.Color.GREEN),
                ("B", word.Color.BLACK),
                ("O", word.Color.GREEN),
                ("T", word.Color.BLACK),
            ]
        )
        with self.assertRaises(word.BlackLetterError) as green:
            self.wordle.guess(
                [
                    ("A", word.Color.BLACK),
                    ("S", word.Color.BLACK),
                    ("C", word.Color.BLACK),
                    ("O", word.Color.GREEN),
                    ("T", word.Color.GREEN),
                ]
            )
        self.assertEqual(
            "'T' can not be changed from BLACK to GREEN", str(green.exception)
        )
        self.assertListEqual([], self.wordle._available_letters["T"])  # type: ignore
        with self.assertRaises(word.BlackLetterError) as yellow:
            self.wordle.guess(
                [
                    ("R", word.Color.YELLOW),
                    ("A", word.Color.BLACK),
                    ("B", word.Color.BLACK),
                    ("I", word.Color.BLACK),
                    ("D", word.Color.BLACK),
                ]
            )
        self.assertEqual(
            "'R' can not be changed from BLACK to YELLOW", str(yellow.exception)
        )

    def test_yellow_after_green(self) -> None:
        self.wordle.guess(
            [
                ("R", word.Color.GREEN),
                ("A", word.Color.BLACK),
                ("B", word.Color.YELLOW),
                ("I", word.Color.BLACK),
                ("D", word.Color.BLACK),
            ]
        )
        self.assertListEqual([1, 3, 4], self.wordle._available_letters["B"])  # type: ignore


if __name__ == "__main__":
    unittest.main()
