from letter_state import LetterState

class Wongdle:
    # some code has been taken from https://github.com/pixegami/python-wordle as skeleton for project (just the basic wordle logic excluding the double guess bug)

    MAX_ATTEMPT = 6
    WORD_LENGTH = 5

    def __init__(self, secret: str):
        self.secret: str = secret
        self.attempts = []
        pass

    def attempt(self,word:str):
        self.attempts.append(word)
    def guess(self,word:str):
        result = []
        secret_characters = set(self.secret)
        dic_char = {}
        for i in secret_characters: # add occurence of each character to track if letter has been guessed or not (APPLE vs HELLO case)
            if str(i) not in dic_char:
                dic_char[str(i)]=1
            else:
                dic_char[str(i)]+=1
        
        for i in range(self.WORD_LENGTH):
            character = word[i]
            letter = LetterState(character)
            letter.is_in_word = character in self.secret
            letter.is_in_position = character == self.secret[i]
            if letter.is_in_position:
                dic_char[str(character)]-=1
            result.append(letter)

        for i in result: # adding logic for case where L can be guessed again 
            if str(i.character) in dic_char and dic_char[str(i.character)]<1:
                i.is_in_word = False
            
        return result

    @property
    def is_solved(self):
        return len(self.attempts)>0 and self.attempts[-1]==self.secret
    
    @property
    def remaining_attempts(self) -> int:
        return self.MAX_ATTEMPT - len(self.attempts)
        
    #property means you can use as attribute instead of a method (no need brackets)
    @property
    def can_attempt(self):
        return self.remaining_attempts > 0 and not self.is_solved
    
    