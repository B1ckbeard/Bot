import random


def dice_roll(x):
    if x == 1:
        print(random.randint(1, 6))
    elif x == 2:
        print(random.randint(2, 12))


num = int(input())

dice_roll(num)
