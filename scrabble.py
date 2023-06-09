from colorama import init as colorama_init
from colorama import Back
from colorama import Style
from itertools import permutations
from random import randrange
from functools import reduce
import operator
def prod(iterable):
    return reduce(operator.mul, iterable, 1)

colorama_init()
color_dictionary = {"@" : Back.MAGENTA, "#" : Back.RED, "2" : Back.CYAN, "3" : Back.BLUE, " " : Back.YELLOW, "-" : Back.YELLOW}
points = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10}

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

    def __str__(self):
        return str((self.x, self.y, self.direction, self.text))

    def __repr__(self):
        return str((self.x, self.y, self.direction, self.text))

    def __eq__(self, obj):
        return isinstance(obj, Word) and obj.x == self.x and obj.y == self.y and obj.direction == self.direction and obj.text == self.text

class Bag:
    def __init__(self):
        self.bag = self.generate_bag()
        
    def generate_bag(self):
        return ['A']*9 + ['B']*2 + ['C']*2 + ['D']*4 + ['E']*12 + ['F']*2 + ['G']*3 + \
               ['H']*2 + ['I']*9 + ['J']*1 + ['K']*1 + ['L']*4 + ['M']*2 + ['N']*6 + \
               ['O']*8 + ['P']*2 + ['Q']*1 + ['R']*6 + ['S']*4 + ['T']*6 + ['U']*4 + \
               ['V']*2 + ['W']*2 + ['X']*1 + ['Y']*2 + ['Z']*1


    def choose_n_letters(self, n):
        chosen_tiles = []

        n = min(n, len(self.bag))
        
        while n > 0:
            spot = randrange(0, len(self.bag))
            chosen_tiles.append(self.bag.pop(spot))
            n -= 1
        
        return chosen_tiles

class Scrabble:
    BOARD_SIZE = 15
    
    def __init__(self, player_count):
        self.board = self.new_board()
        self.fresh_game = True
        self.bag = Bag()
        self.players = player_count
        self.current_player = 0
        self.points = [0] * player_count
        self.words = []

    def award_current_player(self, x):
        self.points[self.current_player] += x

    def next_player(self):
        self.current_player = (self.current_player + 1) % self.players

    def calculate_points(self, multipliers):
        def word_multiplier(x):
            if x == "@":
                return 2
            elif x == "#":
                return 3
            return 1

        def to_number(x):
            if str(x).isnumeric():
                return int(x)
            return 1

        def letter_multiplier(letter_pair):
            return points[letter_pair[0]] * to_number(letter_pair[1])
            
        word_multiplier = prod([word_multiplier(multiplier[1]) for multiplier in multipliers])
        letter_values = sum([letter_multiplier(multiplier) for multiplier in multipliers])
        return word_multiplier * letter_values

    def new_board(self):
        with open("starting_board.txt", "r") as f:
            return [x[2:-3].split("-") for x in f.readlines()]

    def cell_is_in_bounds(self, x, y):
        return x <= 14 and y <= 14 and x >= 0 and y >= 0

    def cell_is_alpha(self, x, y):
        return self.board[x][y].isalpha()

    def cell_is_unplayed(self, x, y):
        return self.cell_is_in_bounds(x, y) and not self.cell_is_alpha(x, y)

    def cell_is_played(self, x, y):
        return self.cell_is_in_bounds(x, y) and self.cell_is_alpha(x, y)

    def cell_is_placeable(self, x, y, letter):
        if letter == "_" or letter == self.board[x][y]:
            return self.cell_is_played(x, y)
        return self.cell_is_unplayed(x, y)

    def get_letter(self, x, y):
        return self.board[x][y] 

    def set_letter(self, x, y, letter):
        self.board[x][y] = letter

    def set_letters(self, cells):
        for cell in cells:
            self.set_letter(cell.x, cell.y, cell.letter)

    def get_row(self, y):
        return [self.board[x][y] for x in range(15)]

    def get_column(self, x):
        return self.board[x]

    def get_horizontal_word(self, x, y):
        if not self.cell_is_played(x, y):
            return False
        
        leftmost_index = x
        while self.cell_is_played(leftmost_index - 1, y):
            leftmost_index -= 1
        rightmost_index = x
        while self.cell_is_played(rightmost_index + 1, y):
            rightmost_index += 1
        if leftmost_index == rightmost_index:
            return False
        letters = [self.get_letter(i, y) for i in range(leftmost_index, rightmost_index+1)]

        return [Word(leftmost_index, y, "H", ''.join(letters)), (x,y)]

    def get_vertical_word(self, x, y):
        if not self.cell_is_played(x, y):
            return False
        
        upmost_index = y
        while self.cell_is_played(x, upmost_index - 1):
            upmost_index -= 1
        downmost_index = y
        while self.cell_is_played(x, downmost_index + 1):
            downmost_index += 1
        if upmost_index == downmost_index:
            return False
        letters = [self.get_letter(x, i) for i in range(upmost_index, downmost_index+1)]

        return [Word(x, upmost_index, "V", ''.join(letters)), (x,y)]

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
        try:
            word_placeable = all(self.cell_is_placeable(word.x + x_inc * i, word.y + y_inc * i, word.text[i]) for i in letter_range)
        except:
            print(word)

        return word_placeable


    def play_word(self, word, display = True, try_mode = False):
        cells_played = []
        multipliers = {}
        overlapped = False
        letters_used = len(word.text)
        
        #is every other letter placeable (is there a letter on the board for _'s)
        x_inc, y_inc = self.get_x_y_incs(word.direction)
        if self.is_word_placeable(word):
            for i in range(len(word.text)):
                x, y, letter = word.x + x_inc * i, word.y + y_inc * i, word.text[i]
                if (letter == "_" or letter == self.board[x][y]) and self.cell_is_played(x, y):
                    overlapped = True
                    multipliers[(x,y)] = (self.board[x][y], self.board[x][y])
                    letters_used -= 1
                    if letter == "_":
                        word.text = word.text[:i] + self.board[x][y] + word.text[i+1:]
                    continue
                
                cells_played.append(Cell(x, y, self.board[x][y]))
                multipliers[(x,y)] = (word.text[i], self.board[x][y])
                self.set_letter(x, y, letter)
        else:
            if not try_mode:
                print("Please ensure the played word is on the board and doesn't overlap existing words", word.text)
            return

        def error(*args):
            self.set_letters(cells_played)
            if not try_mode:
                print(*args)
            return


        result = [(word.text, self.calculate_points(list(multipliers.values())))]
        # now check if the main word is correct
        final_word = self.get_word(word.x, word.y, word.direction)[0].text
        if not final_word or tuple(final_word) not in WORDS:
            error("Sorry, that is not a word", final_word)
            return


        if not self.fresh_game:
            side_words = self.get_side_words(word)
            
            if all(side_word == False for side_word in side_words) and not overlapped:
                error("Please ensure the played word touches existing words")
                return
            
            if any(side_word and tuple(side_word[0].text) not in WORDS for side_word in side_words):
                error("Sorry, that word created an invalid side words", side_words)
                return
            
            for side_word in side_words:
                if side_word and side_word[0] not in self.words:
                    text = side_word[0].text
                    def calculate_multiplier(i):
                        x_s, y_s, d = side_word[0].x, side_word[0].y, side_word[0].direction
                        x_inc, y_inc = self.get_x_y_incs(d)
                        letter_spot = (x_s + x_inc * i, y_s + y_inc * i)
                        if letter_spot in multipliers:
                            return multipliers[letter_spot][1]
                        return ' '
                    side_word_multipliers = [(text[i], calculate_multiplier(i)) for i in range(len(text))]
                    result.append((text, self.calculate_points(side_word_multipliers)))
                    if not try_mode:
                        self.words.append(side_word[0])

        if display:
            self.display()

        if try_mode:
            self.set_letters(cells_played)
        else:
            self.words.append(word)
            self.fresh_game = False

        total_points = sum([x[1] for x in result])

        if letters_used == 7:
            total_points += 50
        
        return (word, total_points)
        

    def play_words(self, words):
        for word in words:
            print(self.play_word(word, False))
        self.display()
        

    def display(self, colored=False):
        flipped = list(zip(*self.board))
        def clean_up(x):
            if x in "@#23 -":
                return f"{color_dictionary[x]} {Back.RESET}"
            return f"{color_dictionary[' ']}{x}"
        for column in flipped:
            if colored:
                print(f"{Style.BRIGHT}|", "".join([clean_up(x) for x in "-".join(column)]) + f"{Back.RESET}", "|")
            else:
                print("|", "-".join(column), "|")

def make_word(x, y, horizontal, text):
    if x < 0 or y < 0 or x > 14 or y > 14:
        return False
    direction = "H" if horizontal else "V"
    return Word(x, y, direction, text)




Board = Scrabble(2)

EXAMPLE_GAME = [make_word(3, 7, True, "DRAIN"),
        make_word(4, 6, False, "G_OUP"),
        make_word(6, 6, False, "Q_"),
        make_word(2, 8, True, "ZO_"),
        make_word(7, 3, False, "EXTI_CT"),
        make_word(4, 4, True, "FLA_"),
        make_word(3, 10, False, "UH"),
        make_word(7, 8, True, "_HARM"),
        make_word(9, 6, False, "DR_W"),
        make_word(5, 2, False, "SU_K"),
        make_word(2, 2, True, "VAV_"),
        make_word(3, 1, False, "J_R"),
        make_word(10, 8, False, "_EM"),
        make_word(2, 11, False, "OY"),
        make_word(7, 3, False, "_______S"),
        make_word(2, 2, False, "_OID"),
        make_word(1, 4, False, "BIT"),
        make_word(0, 5, False, "GAP"),
        make_word(11, 8, False, "_EAN"),
        make_word(1, 12, False, "OI"),
        make_word(0, 13, False, "BI"),
        make_word(2, 0, True, "RAGE"),
        make_word(0, 0, True, "EN____"),
        make_word(7, 3, True, "_LITE"),
        make_word(10, 4, True, "OWN"),
        make_word(11, 2, False, "N__"),
        make_word(12, 10, False, "REF"),
        make_word(13, 4, False, "SECLUDE"),
        make_word(10, 1, True, "NAIL"),
        make_word(12, 7, True, "S_Y"),]

#Board.play_word(EXAMPLE_GAME[0])

def row_or_column_to_template(row):
    template = []
    for letter in row:
        if letter.isalpha():
            template.append(letter)
        else:
            template.append('')
    return template

def fill_template_once(template, perm, gap_number):
    gap_spot = [i for i, n in enumerate(template) if n == ''][gap_number]
    
    while perm != []:
        template[template.index('', gap_spot)] = perm.pop(0)
        
    gaps_before = [i for i, n in enumerate(template[:gap_spot]) if n == '']
    start = 0
    if gaps_before != []:
        start = gaps_before[-1]+1

    gaps_after = [i for i, n in enumerate(template[gap_spot:]) if n == '']
    end = 15
    if gaps_after:
        end = gap_spot + gaps_after[0]

    return (template[start:end], start)

def fill_templates(template, perms):
    result = {}
    for perm in perms:
        total_gaps = sum([x == '' for x in template])
        for gap_number in range(total_gaps+1-len(perm)):
            filled_template = fill_template_once(template.copy(), list(perm).copy(), gap_number)
            word_as_tuple, start = tuple(''.join(filled_template[0])), filled_template[1]
            
            if word_as_tuple in result:
                if start not in result[word_as_tuple]:
                    result[word_as_tuple].append(start)
            else:
                result[word_as_tuple] = [start]
    return result
    

def words_from_hand_in_template(Hand, template):
    all_valid_words_w_starts = []
    for i in range(7, 1, -1):
        perms = list(permutations(''.join(Hand), i))
        words_w_starts = fill_templates(template, perms)
        found_words = list(words_w_starts.keys())
        valid_words = WORDS.intersection(found_words)
        if valid_words:
            valid_words_w_starts = [(word, words_w_starts[word]) for word in valid_words]
            all_valid_words_w_starts.extend(valid_words_w_starts)
    return all_valid_words_w_starts

def grow_trues(boolean_list):
    result = []
    for i in range(len(boolean_list)):
        if boolean_list[i] or (i-1 >= 0 and boolean_list[i-1]) or (i+1 < len(boolean_list) and boolean_list[i+1]):
            result.append(i)
    return result

def playable_rows():
    if Board.fresh_game:
        return [7]
    rows_with_a_letter = []
    for y in range(15):
        rows_with_a_letter.append(any(cell.isalpha() for cell in Board.get_row(y)))
    return(grow_trues(rows_with_a_letter))

def playable_columns():
    if Board.fresh_game:
        return [7]
    columns_with_a_letter = []
    for x in range(15):
        columns_with_a_letter.append(any(cell.isalpha() for cell in Board.get_column(x)))
    return(grow_trues(columns_with_a_letter))
        

Hand = Board.bag.choose_n_letters(7)
        
def all_possible_moves(Hand):
    print("Generating all possible moves for: ", Hand)
    templates = []
    moves = []
    for y in playable_rows():
        row = Board.get_row(y)
        template = row_or_column_to_template(row)
        templates.append((template, -1, y))
        valid_words = words_from_hand_in_template(Hand, template)
        for valid_word in valid_words:
            valid_word, spots = valid_word
            for spot in spots:
                word = make_word(spot, y, True, valid_word)
                result = Board.play_word(word, display=False, try_mode=True)
                if result:
                    moves.append(result)
                    
    
        
    for x in playable_columns():
        column = Board.get_column(x)
        template = row_or_column_to_template(column)
        templates.append((template, x, -1))
        valid_words = words_from_hand_in_template(Hand, template)
        for valid_word in valid_words:
            valid_word, spots = valid_word
            for spot in spots:
                word = make_word(x, spot, False, valid_word)
                result = Board.play_word(word, display=False, try_mode=True)
                if result:
                    moves.append(result)
               
    moves = sorted(moves, key=lambda move: move[1], reverse=True)
    [print(move) for move in moves[:5]] 
#)all_possible_moves(Hand)


EXAMPLE_GAME2 = [make_word(7,7,True,"CREAK"),
                 make_word(10,1,False,"VIHUEL_"),
                 make_word(12,7,False,"SHIMMED"),
                 make_word(9, 13, True, "WADDY"),
                 make_word(9, 14, True, "OY"),
                 make_word(9, 10, True, "FRUMP"),
                 make_word(14, 4, False, "BOUGIES"),
                 make_word(7, 0, False, "BACTERI_"),
                 make_word(6, 6, True, "Q_")]
Board.play_words(EXAMPLE_GAME2[:-1])

#all_possible_moves("ABCRITE")
#print(Board.play_word(make_word(7, 0, False, "BACTERI_")))
#all_possible_moves("EENRTZQ")
#print(Board.play_word(make_word(6, 6, True, "Q_")))
all_possible_moves("DINOOTT")
print(Board.play_word(make_word(11, 2, False, "DOT")))
