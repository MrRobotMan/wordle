import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import colorama

import app
from word import Color, Word


@patch("builtins.print")
class TestApp(unittest.TestCase):
    """Test class fro the main app."""

    word_list = app.get_words(app.WORDS_FILE)

    def setUp(self) -> None:
        self.wordle = Word(self.word_list, 5)

    def test_get_words_list(self, mock_print: Mock) -> None:
        """Tests that the wordle list generates the correct number for words."""
        self.assertEqual(2315, len(app.get_words(app.WORDS_FILE)))

    def test_bad_words_list(self, mock_print: Mock) -> None:
        """Tests that no match generates no words"""
        self.assertSetEqual(set(), app.get_words(Path("requirements.txt")))

    @patch(
        "builtins.input",
        side_effect=["liners", "liner", "1", "", "b", "Y", "4", "g", "green"],
    )
    def test_get_guess(self, mock_input: Mock, mock_print: Mock) -> None:
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
                ("L", (Color.BLACK, colorama.Fore.WHITE)),
                ("I", (Color.BLACK, colorama.Fore.WHITE)),
                ("N", (Color.YELLOW, colorama.Fore.YELLOW)),
                ("E", (Color.GREEN, colorama.Fore.GREEN)),
                ("R", (Color.GREEN, colorama.Fore.GREEN)),
            ],
            guess,
        )

    @patch("app.view_available_words")
    @patch.object(Word, "guess")
    @patch(
        "app.get_guess",
        return_value=[
            ("L", (Color.BLACK, colorama.Fore.WHITE)),
            ("I", (Color.BLACK, colorama.Fore.WHITE)),
            ("N", (Color.YELLOW, colorama.Fore.YELLOW)),
            ("E", (Color.GREEN, colorama.Fore.GREEN)),
            ("R", (Color.GREEN, colorama.Fore.GREEN)),
        ],
    )
    def test_guess_loop(
        self,
        mock_get_guess: Mock,
        mock_guess: Mock,
        mock_view_available_words: Mock,
        mock_print: Mock,
    ) -> None:
        app.guess_loop("Enter a guess", self.wordle)
        mock_get_guess.assert_called_once()
        mock_guess.assert_called_once_with(
            [
                ("L", Color.BLACK),
                ("I", Color.BLACK),
                ("N", Color.YELLOW),
                ("E", Color.GREEN),
                ("R", Color.GREEN),
            ]
        )
        mock_view_available_words.assert_called_once()

    @patch("builtins.input", side_effect=["", "h", "Y"])
    def test_view_available_words(self, mock_input: Mock, mock_print: Mock) -> None:
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
        mock_print.assert_called_once_with({"ROOST", "RECUT", "RESET"})

    @patch("builtins.input", side_effect=["liner", "1", "1", "1", "1", "1", "n"] * 6)
    def test_main_too_many_guesses(self, mock_input: Mock, mock_print: Mock) -> None:
        app.main()
        self.assertIn("Too bad", mock_print.call_args.args[0])

    @patch(
        "builtins.input",
        side_effect=[
            "liner",
            "2",
            "1",
            "1",
            "2",
            "1",
            "n",
            "pleat",
            "3",
            "3",
            "3",
            "3",
            "3",
        ],
    )
    def test_main_success(self, mock_input: Mock, mock_print: Mock) -> None:
        app.main()
        mock_print.assert_called_with("Nailed it! Only took 2 guesses.")


if __name__ == "__main__":
    unittest.main()
