import unittest
from unittest.mock import Mock, patch

import app
from word import Color


class TestApp(unittest.TestCase):
    """Test class fro the main app."""

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


if __name__ == "__main__":
    unittest.main()
