import random
from itertools import permutations
from itertools import product

def fetch_words():
    with open("scrabble_dictionary.txt", "r") as f:
        return set(tuple(x[:-1]) for x in f.readlines())

WORDS = fetch_words()

def generate_bag():
    return ['A']*9 + ['B']*2 + ['C']*2 + ['D']*4 + ['E']*12 + ['F']*2 + ['G']*3 + \
           ['H']*2 + ['I']*9 + ['J']*1 + ['K']*1 + ['L']*4 + ['M']*2 + ['N']*6 + \
           ['O']*8 + ['P']*2 + ['Q']*1 + ['R']*6 + ['S']*4 + ['T']*6 + ['U']*4 + \
           ['V']*2 + ['W']*2 + ['X']*1 + ['Y']*2 + ['Z']*1

bag = generate_bag()


def refresh_bag():
    bag = generate_bag()

def no_more_than(n, x):
    if n > x:
        return x
    return n

def choose_n_letters(n):
    chosen_tiles = []

    n = no_more_than(n, len(bag))
    
    while n > 0:
        spot = random.randrange(0, len(bag))
        chosen_tiles.append(bag.pop(spot))
        n -= 1
    
    return chosen_tiles

def display_board(board):
    for x in board:
        print(x)

def make_empty_board():
    return [[0] * 13 for x in range(13)]

def set_word(word, board, spot, direction):
    if direction == "VERTICAL":
        direction = [1, 0]
    else:
        direction = [0, 1]
    for letter in word:
        board[spot[0]][spot[1]] = letter
        spot[0] += direction[0]
        spot[1] += direction[1]
    return board
    
def choose_half_letters(lst):
    half_size = len(lst) // 2
    chosen_letters = lst[:half_size+1]
    #leftover_letters = lst[half_size+1:]
    return chosen_letters#, leftover_letters

def choose_halves(lst):
    half_size = len(lst) // 2
    chosen_letters = lst[:half_size+1]
    leftover_letters = lst[half_size+1:]
    return chosen_letters, leftover_letters

def check_for_words(perms):
    return WORDS.intersection(perms)

def find_unique_chars(longer_str, substring):
    longer_list = list(longer_str)
    substring_list = list(substring)
    
    for char in substring_list:
        if char in longer_list:
            longer_list.remove(char)
    
    return ''.join(longer_list)

def get_adjacent_letters(word, index_of_letter):
    adjacent_letters = []
    if index_of_letter > 0:
        adjacent_letters.append(word[index_of_letter-1])
    if index_of_letter <= len(word)-2:
        adjacent_letters.append(word[index_of_letter+1])
    return adjacent_letters

def faster(hand, doubled = [], adjacent = []):
    #print("HAND", hand, "Doubled", doubled, "Adjacent", adjacent)
    
    if (len(hand) >= 14):
        halves = permutations(hand, 7)
        for half in halves:
            if half in WORDS:
                rest = find_unique_chars(hand, half)
                for letter in find_unique_chars(half,  doubled):
                    index_of_letter = half.index(letter)
                    adjacent_letters = get_adjacent_letters(half, index_of_letter)
                    banned_letters = half[index_of_letter:index_of_letter+1]
                    #print("running with", half)
                    result = faster(rest + letter, doubled + list(letter),
                                    adjacent + adjacent_letters)
                    if result:
                        return (half, result)
        

    
    elif (len(hand) <= 7):
        perms = permutations(''.join(hand))
        full_matches = check_for_words(perms)
        if full_matches:
            return full_matches

    
    halves = permutations(hand, len(hand) // 2)
    for half in halves:
        if half in WORDS:
            remaining = find_unique_chars(hand, half)
            #print(half, doubled)
            if doubled and doubled[-1] in half:
                adjacent = adjacent + get_adjacent_letters(half, half.index(doubled[-1]))
            for letter in find_unique_chars(half, doubled + adjacent):
                second = tuple(remaining) + tuple(letter)
                seconds = check_for_words(permutations(second))
                if seconds:
                    return (half, seconds, doubled + list(letter))

def main(n):
    refresh_bag()
    hand = choose_n_letters(n)
    print(hand)
    return faster(hand)
