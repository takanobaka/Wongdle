from wongdle import Wongdle
from colorama import Fore

def main():
    print("Hello World")
    wongdle = Wongdle("APPLE")

    while wongdle.can_attempt:
        x = input("Type your guess: ")
        if len(x)!=wongdle.WORD_LENGTH:
            print(Fore.RED+f"Please input {wongdle.WORD_LENGTH} word: "+Fore.RESET) #format the print statemetn with dynamic variables!
            continue
        wongdle.attempt(x)
        result = wongdle.guess(x)
        print(*result, sep = "\n") #print the *result will print result[0], result[1], etc. etc.
    if wongdle.is_solved:
        print("Nice.")
    else:
        print("u dum")



if __name__ == "__main__":
    main()
