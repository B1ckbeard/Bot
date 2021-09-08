import random

def dice_roll(x):
    if x == 1:
        return(random.randint(1, 6))
    elif x == 2:
        return(random.randint(2, 12))
    else:
        pass