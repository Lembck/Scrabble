def fetch_words():
    with open("scrabble_dictionary.txt", "r") as f:
        return set(tuple(x[:-1]) for x in f.readlines())

WORDS = fetch_words()

class Cell:
    def __init__(self, x, y, letter):
        self.x = x
        self.y = y
        self.letter = letter

class Word:
    def __init__(self, x, y, direction, text):
        self.x = x
        self.y = y
        self.direction = direction
        self.text = text

class Scrabble:
    BOARD_SIZE = 15
    EMPTY = ' '
    
    def __init__(self):
        self.board = self.new_board()
        self.fresh_game = True
        self.words = []

    def new_board(self):
        return [[self.EMPTY] * self.BOARD_SIZE for x in range(self.BOARD_SIZE)]

    def is_index_in_bounds(self, x, y):
        return x <= 14 and y <= 14 and x >= 0 and y >= 0

    def is_index_available(self, x, y):
        return self.is_index_in_bounds(x,y) and self.board[x][y] == self.EMPTY

    def is_a_letter(self, x, y):
        return self.is_index_in_bounds(x,y) and self.board[x][y] != self.EMPTY

    def iia(self, x, y, letter):
        if letter == "_":
            return self.is_index_in_bounds(x, y) and self.board[x][y] != self.EMPTY
        return self.is_index_available(x, y)

    def set_letter(self, x, y, letter):
        self.board[x][y] = letter

    def set_letters(self, cells):
        for cell in cells:
            self.set_letter(cell.x, cell.y, cell.letter)

    def get_letter(self, x, y):
        return self.board[x][y] 

    def get_horizontal_word(self, x, y):
        if not self.is_index_in_bounds(x,y) or self.board[x][y] == self.EMPTY:
            return False
        leftmost_index = x
        while self.is_a_letter(leftmost_index - 1, y):
            leftmost_index -= 1
        rightmost_index = x
        while self.is_a_letter(rightmost_index + 1, y):
            rightmost_index += 1
        if leftmost_index == rightmost_index:
            return False
        letters = [self.get_letter(i, y) for i in range(leftmost_index, rightmost_index+1)]

        return ''.join(letters)

    def get_vertical_word(self, x, y):
        if not self.is_index_in_bounds(x,y) or self.board[x][y] == self.EMPTY:
            return False
        upmost_index = y
        while self.is_a_letter(x, upmost_index - 1):
            upmost_index -= 1
        downmost_index = y
        while self.is_a_letter(x, downmost_index + 1):
            downmost_index += 1
        if upmost_index == downmost_index:
            return False
        letters = [self.get_letter(x, i) for i in range(upmost_index, downmost_index+1)]

        return ''.join(letters)

    def get_word(self, x, y, direction):
        if direction == "H":
            return self.get_horizontal_word(x, y)
        else:
            return self.get_vertical_word(x, y)

    def get_x_y_incs(self, direction):
        x_inc = 1 if direction == "H" else 0
        y_inc = 1 if direction == "V" else 0
        return x_inc, y_inc

    def opposite_direction(self, word):
        if word.direction == "H":
            return "V"
        return "H"

    def get_side_words(self, word):
        if word.direction == "H":
            return [self.get_word(letter_x, word.y, "V") for letter_x in range(word.x, word.x + len(word.text))]
        return [self.get_word(word.x, letter_y, "H") for letter_y in range(word.y, word.y + len(word.text))]


    # requires all letters:
    # - to be in the same row or column
    # - to not replace existing letters on the board
    # - to not have gaps in between
    def is_word_placeable(self, word):
        if self.fresh_game:
            ys = list(range(word.y, len(word.text)+word.y))
            xs = list(range(word.x, len(word.text)+word.x))
            
            if (word.x == 7 and 7 in ys) or (word.y == 7 and 7 in xs):
                return True
            else:
                return False

        
        x_inc, y_inc = self.get_x_y_incs(word.direction)
        letter_range = range(len(word.text))
        word_placeable = all(self.iia(word.x + x_inc * i, word.y + y_inc * i, word.text[i]) for i in letter_range)

        return word_placeable


    def play_word(self, word, display = True):
        letters_played = []

        #is every other letter placeable (is there a letter on the board for _'s)
        x_inc, y_inc = self.get_x_y_incs(word.direction)
        if self.is_word_placeable(word):
            for i in range(len(word.text)):
                if word.text[i] == "_" and self.board[x][y] != self.EMPTY:
                    continue
                x, y, letter = word.x + x_inc * i, word.y + y_inc * i, word.text[i]
                letters_played.append(Cell(x, y, self.board[x][y]))
                self.set_letter(x, y, letter)
        else:
            print("Please ensure the played word is on the board and doesn't overlap existing words", word.text)
            return

        def error(*args):
            self.set_letters(letters_played)
            print(*args)

        # now check if the main word is correct
        final_word = self.get_word(word.x, word.y, word.direction)
        if not final_word or tuple(final_word) not in WORDS:
            error("Sorry, that is not a word", final_word)

        
        if self.fresh_game:
            self.fresh_game = False
            return

        side_words = self.get_side_words(word)
        
        if all(side_word == False for side_word in side_words):
            error("Please ensure the played word touches existing words")
            
        if any(side_word and tuple(side_word) not in WORDS for side_word in side_words):
            error("Sorry, that word created an invalid side words", side_words)

        if display:
            self.display()


    def play_words(self, words):
        for word in words:
            self.play_word(word, False)
        self.display()
        

    def display(self):
        flipped = list(zip(*self.board))
        for column in flipped:
            print("|", "-".join(column), "|")

def make_word(x, y, horizontal, text):
    if x < 0 or y < 0 or x > 14 or y > 14:
        return False
    direction = "H" if horizontal else "V"
    return Word(x, y, direction, text)




Board = Scrabble()
Board.play_word(make_word(7, 4, False, "HELLO"))
Board.play_word(make_word(5, 7, False, "HELP"))
Board.display()

