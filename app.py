from typing import List, Tuple

import word

COLOR_MAP = {
    "1": word.Color.BLACK,
    "b": word.Color.BLACK,
    "2": word.Color.YELLOW,
    "y": word.Color.YELLOW,
    "3": word.Color.GREEN,
    "g": word.Color.GREEN,
}
MAX_GUESSES = 6
WORD_LENGTH = 5


def view_available_words(word: word.Word) -> None:
    """Shows the user how many words in the list still remain
    and prompts them if they want to view the list.
    """
    words = word.available_words
    view = input(
        f"There are {len(words)} possible words remaining. Would you like to view them? [y/N]: "
    ).lower()
    while view not in ("y", "n"):
        view = input("Please enter only 'Y' or 'N': ").lower()
    if view == "y":
        print(words)


def get_guess(input_text: str = "Enter your guess: ") -> List[Tuple[str, word.Color]]:
    guess = input(input_text).upper()
    print("Enter '1' or 'b' for black, '2' or 'y' for yellow, '3' or 'g' for green.")
    guessed: List[Tuple[str, word.Color]] = []
    for letter in guess:
        while True:
            color = input(f"Enter the color for {letter}: ").lower()
            if color and COLOR_MAP.get(color[0]):
                break
        guessed.append((letter, COLOR_MAP[color[0]]))
    return guessed


def guess_loop(input_text: str, wordle: word.Word) -> None:
    """Main interactions to process"""
    guess: List[Tuple[str, word.Color]] = []
    guess = get_guess(input_text)
    while len(guess) != WORD_LENGTH:
        guess = get_guess(f"Guess must be {WORD_LENGTH} characters. Try again: ")
    wordle.guess(guess)
    view_available_words(wordle)
    print(wordle.known_letters)


def main() -> None:
    """The main interface of the program.

    When run this will as the user for their guesses
    and help narrow down the possible words.
    """
    with open("words.txt", "r") as f:
        word_list = set(line.strip() for line in f)
    wordle = word.Word(word_list, WORD_LENGTH)
    print("######################################")
    print("#    WELCOME TO THE WORDLE HELPER    #")
    print("# At any time enter 'ctrl+c' to exit #")
    print("######################################")
    guess_loop("Enter your guessed word: ", wordle)
    for cnt in range(MAX_GUESSES - 1):
        if "_" not in wordle.known_letters:
            print(f"Nailed it! Only took {cnt + 1} guesses.")
            break
        guess_loop("Enter your next guess: ", wordle)
    else:
        print(f"Too bad. The possible word(s) were {wordle.available_words}")


if __name__ == "__main__":
    main()
