from typing import List
from wongdle import Wongdle
from colorama import Fore
from letter_state import LetterState
import random

def main():
    print("Hello World")
    word_set = load_word_set("data/wordle_words.txt")
    secret = random.choice(list(word_set))
    # wongdle = Wongdle(secret)

    wongdle = Wongdle("APPLE")
    while wongdle.can_attempt:
        x = input("\nType your guess: ").upper()
        if len(x)!=wongdle.WORD_LENGTH:
            print(Fore.RED+f"Please input {wongdle.WORD_LENGTH} word: "+Fore.RESET) #format the print statemetn with dynamic variables!
            continue
        if x not in word_set:
            print(Fore.RED+f"Please input valid word: "+Fore.RESET) 
            continue
        wongdle.attempt(x)
        display_results(wongdle)

    if wongdle.is_solved:
        print("You got it!")
    else:
        print(f"Word was: {secret}")
        print("u dum.")


def display_results(wongdle:Wongdle):
    print("\n")
    print(f"You have {wongdle.remaining_attempts} attempts remaining.")
    for word in wongdle.attempts:
        result = wongdle.guess(word)
        colored_result_str = convert_result_to_color(result)
        print(colored_result_str)
    for _ in range(wongdle.remaining_attempts):
        print(" ".join(["_"]*wongdle.WORD_LENGTH))

def convert_result_to_color(result: List[LetterState]):
    result_with_color = []
    for letter in result:
        if letter.is_in_position:
            color = Fore.GREEN
        elif letter.is_in_word:
            color = Fore.YELLOW
        else:
            color = Fore.WHITE
        colored_letter = color+letter.character + Fore.RESET
        result_with_color.append(colored_letter)
    
    return " ".join(result_with_color)

def draw_border_around(lines: List[str], size: int = 9, pad: int = 1):
    top_border = ""
    pass


def load_word_set(file_path:str):
    word_set = set()
    with open(file_path, "r") as f:
        for line in  f.readlines():
            word = line.strip().upper()
            word_set.add(word)
    return word_set

if __name__ == "__main__":
    main()
