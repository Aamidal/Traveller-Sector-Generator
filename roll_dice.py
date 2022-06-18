#roll_dice.py
from random import randint

def roll_dice(x = 1):
    '''Roll x 6 sided dice, return the sum.'''
    count = 0
    total = 0
    while count < x:
        count = count + 1
        total = total + randint(1, 6)
    return total