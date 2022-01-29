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


def get_guess() -> List[Tuple[str, word.Color]]:
    guess = input("Enter your guessed word: ").upper()
    print("Enter '1' or 'b' for black, '2' or 'y' for yellow, '3' or 'g' for green.")
    guessed: List[Tuple[str, word.Color]] = []
    for letter in guess:
        while True:
            color = input(f"Enter the color for {letter}: ").lower()
            if color and COLOR_MAP.get(color[0]):
                break
        guessed.append((letter, COLOR_MAP[color[0]]))
    return guessed


def main() -> None:
    """The main interface of the program.

    When run this will as the user for their guesses
    and help narrow down the possible words.
    """
    with open("words.txt", "r") as f:
        word_list = set(line.strip() for line in f)
    wordle = word.Word(word_list, 5)
    print("######################################")
    print("#    WELCOME TO THE WORDLE HELPER    #")
    print("# At any time enter 'ctrl+c' to exit #")
    print("######################################")
    while True:
        guess: List[Tuple[str, word.Color]] = []
        while len(guess) != 5:
            guess = get_guess()
        wordle.guess(guess)


if __name__ == "__main__":
    main()
