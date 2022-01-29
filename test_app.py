import unittest
from unittest.mock import Mock, patch

import app
from word import Color, Word


class TestApp(unittest.TestCase):
    """Test class fro the main app."""

    with open("words.txt", "r") as f:
        word_list = set(line.strip() for line in f)
    wordle = Word(word_list, 5)

    @patch(
        "builtins.input", side_effect=["liner", "1", "", "b", "Y", "4", "g", "green"]
    )
    def test_get_guess(self, mock_input: Mock) -> None:
        """Tests the error handling of the get_guess function.

        First "LINER" is entered.
        On the color prompts:
            1 is entered for L
            nothing is entered for I (just hit enter)
            b is entered for I
            Y is entered for N
            4 is improperly entered for E
            g is entered for E
            green is entered for R
        """
        guess = app.get_guess()
        self.assertListEqual(
            [
                ("L", Color.BLACK),
                ("I", Color.BLACK),
                ("N", Color.YELLOW),
                ("E", Color.GREEN),
                ("R", Color.GREEN),
            ],
            guess,
        )

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["", "h", "Y"])
    def test_view_available_words(self, mock_input: Mock, mock_output: Mock) -> None:
        self.wordle.guess(
            [
                ("R", Color.GREEN),
                ("A", Color.BLACK),
                ("B", Color.BLACK),
                ("I", Color.BLACK),
                ("T", Color.GREEN),
            ]
        )
        app.view_available_words(self.wordle)
        mock_input.assert_any_call(
            "There are 3 possible words remaining. Would you like to view them? [y/N]: "
        )
        self.assertEqual(3, mock_input.call_count)
        mock_output.assert_called_once_with({"ROOST", "RECUT", "RESET"})


if __name__ == "__main__":
    unittest.main()
