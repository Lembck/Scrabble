##1 point: E (x12), A (x9), I (x9), O (x8), N (x6), R (x6), T (x6), L (x4), S (x4), U (x4)
##2 points: D (x4), G (x3)
##3 points: B (x2), C (x2), M (x2), P (x2)
##4 points: F (x2), H (x2), V (x2), W (x2), Y (x2)
##5 points: K (x1)
##8 points: J (x1), X (x1)
##10 points: Q (x1), Z (x1)
import random
from itertools import permutations
from itertools import product

def fetch_words():
    with open("scrabble_dictionary.txt", "r") as f:
        return set(tuple(x[:-1]) for x in f.readlines())
print("fetching words")
WORDS = fetch_words()
print("fetched words")

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
                    return (half, seconds)


def helper(hand):
    print("HAND", hand)
    perms = permutations(''.join(hand))
    
    if (len(hand) <= 7):
        full_matches = check_for_words(perms)
        if full_matches:
            return full_matches

    half_index = len(hand) // 2

    halves = permutations(hand, half_index)
    for half in halves:
        if half in WORDS:
            remaining = hand.copy()
            for x in half:
                remaining.remove(x)
            for letter in half:
                second = tuple(remaining) + tuple(letter)
                seconds = check_for_words(permutations(second))
                if seconds:
                    return (half, seconds)
            
    return

def main(n):
    refresh_bag()
    hand = choose_n_letters(n)
    print(hand)
    return faster(hand)
##
##    #print("getting first halves")
##    #first_halves = list(map(choose_half_letters, perms))
##    #print("got them")
##    #firsts = [x for (x,y) in halves]
##    #seconds = [y for (x,y) in halves]
##    
##    #print("checking")
##    #maybe = check_for_words(first_halves)
##    #print("checked")
##   # if maybe:
##    #already_checked_first_halves = []
##    for perm in perms:
##        first_half, second_half = choose_halves(perm)
##        #if first_half in already_checked_first_halves:
##        #    continue
##        #already_checked_first_halves.append(first_half)
##        if first_half in WORDS:
##            print("yes", first_half)
##            for letter in first_half:
##                found = check_for_words(permutations(second_half + tuple(letter)))
##                if found:
##                    print("Oh yea")
##                    return (first_half, found)
####        for word in maybe:
####            rest = find_unique_chars(hand, word)
####            for letter in word:
####                found = check_for_words(permutations(rest + letter))
####                if found:
####                    print("Oh yea")
####                    return (word, found)
##
##
##
##
##
##
##
