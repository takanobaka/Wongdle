from letter_state import LetterState

class Wongdle:
    # some code has been taken from https://github.com/pixegami/python-wordle as skeleton for project (just the basic wordle logic excluding the double guess bug)

    MAX_ATTEMPT = 6
    WORD_LENGTH = 5

    def __init__(self, word_list: list):
        self.word_list: list = word_list
        self.attempts = []
        self.secret = word_list[0]
        pass

    def attempt(self,word:str):
        self.attempts.append(word)

    def greedy_word_picker(self, word:str):
        dic_possibility = {}
        for i in self.word_list:
            self.secret = i
            pattern = self.pattern_generator(i,word)
            if pattern not in dic_possibility:
                dic_possibility[pattern] = [i]
            else:
                dic_possibility[pattern].append(i)
        
        toppattern = sorted(dic_possibility.items(), key=lambda x:len(x[1]), reverse=True)[0][0]
        self.word_list = dic_possibility[toppattern]
        self.secret = self.word_list[0]
        pass
        

    def pattern_generator(self,potential_secret:str,word:str):
        result = []
        secret_characters = set(potential_secret)
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
        pattern = "" 
        for i in result:
            if i.is_in_word:
                pattern+="2"
            elif i.is_in_position:
                pattern+="1"
            else:
                pattern+="0"
        return pattern

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
    
    