#! /usr/bin/python

import re
from pathlib import Path
from typing import List, Set, Tuple

import colorama

import word

colorama.init()

COLOR_MAP = {
    "1": (word.Color.BLACK, colorama.Fore.WHITE),
    "b": (word.Color.BLACK, colorama.Fore.WHITE),
    "2": (word.Color.YELLOW, colorama.Fore.YELLOW),
    "y": (word.Color.YELLOW, colorama.Fore.YELLOW),
    "3": (word.Color.GREEN, colorama.Fore.GREEN),
    "g": (word.Color.GREEN, colorama.Fore.GREEN),
}

MAX_GUESSES = 6
WORD_LENGTH = 5
WORDS_FILE = Path("Wordle - A daily word game_files") / "main.e65ce0a5.js.download"


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


def get_guess(
    input_text: str = "Enter your guess: ",
) -> List[Tuple[str, Tuple[word.Color, str]]]:
    guess = input(input_text).upper()
    while len(guess) != WORD_LENGTH:
        guess = input(f"Guess must be {WORD_LENGTH} characters. Try again: ").upper()
    print("Enter '1' or 'b' for black, '2' or 'y' for yellow, '3' or 'g' for green.")
    guessed: List[Tuple[str, Tuple[word.Color, str]]] = []
    for letter in guess:
        while True:
            color = input(f"Enter the color for {letter}: ").lower()
            if color and COLOR_MAP.get(color[0]):
                break
        guessed.append((letter, COLOR_MAP[color[0]]))
    return guessed


def guess_loop(input_text: str, wordle: word.Word) -> None:
    """Main interactions to process"""
    guess = get_guess(input_text)
    print(
        *(f"{letter[1][1]}{letter[0]}" for letter in guess),
        sep="",
        end=f"{colorama.Style.RESET_ALL}\n",
    )
    wordle.guess([(letter[0], letter[1][0]) for letter in guess])
    if "_" in wordle.known_letters:
        view_available_words(wordle)


def get_words(file: Path) -> Set[str]:
    # pattern is ["WORDS","WORDS",..."WORDS"]
    pattern = re.compile(rf'\[(?:"\w{{{WORD_LENGTH}}}",)+"\w{{{WORD_LENGTH}}}"\]')
    with file.open(encoding="UTF-8") as f:
        data = f.read()
    match = pattern.search(data.upper())
    if not match:
        return set()
    found = match.group(0)
    return set(found[2:-2].split('","'))


def main() -> None:
    """The main interface of the program.

    When run this will as the user for their guesses
    and help narrow down the possible words.
    """
    word_list = get_words(WORDS_FILE)
    wordle = word.Word(word_list, WORD_LENGTH)
    print("######################################")
    print("#    WELCOME TO THE WORDLE HELPER    #")
    print("# At any time enter 'ctrl+c' to exit #")
    print("######################################")
    guess_loop("Enter your guessed word: ", wordle)
    guesses = 1
    for cnt in range(MAX_GUESSES - 1):
        if "_" not in wordle.known_letters:
            print(f"Nailed it! Only took {cnt + 1} guesses.")
            break
        guess_loop("Enter your next guess: ", wordle)
        guesses += 1
    if guesses == MAX_GUESSES:
        print(f"Too bad. The possible word(s) were {wordle.available_words}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print("\nBye!")
