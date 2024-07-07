from typing import List
from wongdle import Wongdle
from colorama import Fore
from letter_state import LetterState

def main():
    print("Welcome to Wongdle, the most cheat-free wordle out there!")
    # load valid words list into game
    word_set = load_word_set("data/wordle_words.txt")
    
    # letting user decide if they want to see computer cheating
    debug = True if input("\n View computer's thinking process? (Y/N) ").upper()=="Y" else False

    wongdle = Wongdle(list(word_set),debug)
    
    while wongdle.can_attempt:
        x = input("\nType your guess: ").upper()
        if len(x)!=wongdle.WORD_LENGTH:
            print(Fore.RED+f"Please input {wongdle.WORD_LENGTH} word: "+Fore.RESET) # using formatting for dynamic variables
            continue
        if x not in word_set:
            print(Fore.RED+f"Please input valid word: "+Fore.RESET) 
            continue
        wongdle.attempt(x)
        pattern = wongdle.greedy_word_picker(x)
        display_results(wongdle,pattern)

    if wongdle.is_solved:
        print("You... beat... the computer!?!? ... respect.")
    else:
        print(f"Word was: {wongdle.secret}")
        print("Sorry, you just lost... fair and square!")


def display_results(wongdle:Wongdle, pattern: str):
    # print(f"\nYou have {wongdle.remaining_attempts} attempts remaining.")
    
    # taking the latest user guess and the pattern decided by greedy to display hinted colour result
    latest_user_guess_letter_state = wongdle.patternToLetterState(wongdle.attempts[-1],pattern)
    colouredGuess = convert_result_to_color(latest_user_guess_letter_state)
    wongdle.addColouredGuess(colouredGuess)

    for result in wongdle.coloured_guesses:
        print(result)

    for _ in range(wongdle.remaining_attempts):
        print(" ".join(["_"]*wongdle.WORD_LENGTH))

    if wongdle.debug:
        print(f"\nComputer has {len(wongdle.word_list)} words left to cheat with.")
        print(f"Secret word has been set to: {wongdle.secret} ")
    

def convert_result_to_color(result: List[LetterState]):
    result_with_color = []
    for letter in result:
        if letter.is_in_position:
            color = Fore.GREEN
        elif letter.is_in_word:
            color = Fore.YELLOW
        else:
            color = Fore.WHITE
        colored_letter = color + letter.character + Fore.RESET
        result_with_color.append(colored_letter)
    
    return " ".join(result_with_color)

def load_word_set(file_path:str):
    word_set = set()
    with open(file_path, "r") as f:
        for line in  f.readlines():
            word = line.strip().upper()
            word_set.add(word)
    return word_set

if __name__ == "__main__":
    main()
