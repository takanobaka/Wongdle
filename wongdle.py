from letter_state import LetterState
import collections, heapq

class Wongdle:
    # some code has been taken from https://github.com/pixegami/python-wordle as skeleton for project (just the basic wordle logic excluding the double guess bug)

    MAX_ATTEMPT = 6
    WORD_LENGTH = 5

    def __init__(self, word_list: list, debug: bool):
        self.word_list: list = word_list
        self.attempts = []
        self.displayed = []
        self.secret = word_list[0]
        self.debug: bool  = debug
        pass

    def attempt(self,word:str):
        #adds the guessed word into attempts for log
        self.attempts.append(word)
    def addDisplayedGuess(self, result:LetterState):
        #adds the guessed word into attempts for log
        self.displayed.append(result)

    def greedy_word_picker(self, word:str):
        """Uses user inputted word to greedily select secret word from pattern group with most options"""
        words_by_pattern_dic = collections.defaultdict(list)
        for potential_secret_word in self.word_list:
            pattern = self.pattern_generator(potential_secret_word, word)
            words_by_pattern_dic[pattern].append(potential_secret_word)
        words_array = []
        for grouped_words_by_pattern in words_by_pattern_dic.values():
            words_array.append(tuple([-len(grouped_words_by_pattern)]+grouped_words_by_pattern))
        
        heapq.heapify(words_array)
        self.word_list = words_array[0][1:]
        self.secret = words_array[0][1]

        # replaced below logic to sort array with heap structure (see above) to reduce time complexity from O(n log(n)) to O(n)
            # toppattern = sorted(words_by_pattern_dic.items(), key=lambda x:len(x[1]), reverse=True)[0][0]
            # print(self.secret, word, toppattern)
            # self.word_list = words_by_pattern_dic[toppattern]
            # self.secret = self.word_list[0]
        pass
        

    def pattern_generator(self,potential_secret:str,word:str):
        """Precalculates the potential pattern hints to return to user. 
        Returns a pattern for the potential secret word against the user inputted word to be used for grouping"""
        result = []
        char_counter = collections.Counter(potential_secret)

        for i in range(self.WORD_LENGTH):
            user_input_char = word[i]
            letter = LetterState(user_input_char)
            letter.is_in_word = user_input_char in potential_secret
            letter.is_in_position = user_input_char == potential_secret[i]
            if letter.is_in_position:
                char_counter[user_input_char]-=1
            result.append(letter)
        
        pattern = "" 
        for letter in result:
            if str(letter.character) in char_counter and char_counter[str(letter.character)]<1:
                letter.is_in_word = False 
                # ^ adding logic for case where HELLO is inputted for secret word (APPLE), 
                # APPLE
                # HELLO
                # PAPRE
                # L in correct place should be green, L in wrong place should be grey.
            
            if letter.is_in_position:
                pattern+="1"
            elif letter.is_in_word:
                pattern+="2"
            else:
                pattern+="0"
        return pattern

    def guess(self,word:str):
        result = []
        counter = collections.Counter(self.secret)
        
        for i in range(self.WORD_LENGTH):
            character = word[i]
            letter = LetterState(character)
            letter.is_in_word = character in self.secret
            letter.is_in_position = character == self.secret[i]
            if letter.is_in_position:
                counter[str(character)]-=1
            result.append(letter)

        for i in result: # adding logic for case where L can be guessed again 
            if str(i.character) in counter and counter[str(i.character)]<1:
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
    
    