import random

start_level = 1
current_level = start_level
max_level = 10
gain = 0
power = current_level + gain

cards_list = ['monster', 'curse', 'gain']

if current_level == max_level:
    print('ты победил!')
elif current_level <= 0:
    current_level = 1

def open_door():
    global current_level
    global gain
    print('Тук-тук')
    card = random.choice(cards_list)
    if card == 'monster':
        battle()
    elif card == 'gain':
        print('выпало усиление, мощь +1')
        gain += 1
        knock_Knock()
    elif card == 'curse':
        print('тебе выпало проклятье, уровень -1')
        current_level -= 1
        knock_Knock()
def knock_Knock():
    print('постучать в дверь снова?')
    answer = input()
    if answer == 'y':
        open_door()
def battle():
    monster_power = random.randint(0, 10)
    print('тебе досталась карта монстра с силой ', + monster_power)
    print('твоя сила = ', + power)
    if power <= monster_power:
        off_it()
        knock_Knock()
    else:
        print('Ты победил монстра!, уровень +1')
        current_level += 1
        knock_Knock()
def off_it():
    number = random.randint(0, 6)
    print('бросаем кубик')
    print('Выпало', + number)
    if number >= 4:
        print('ты слинял')
    elif number < 4:
        print('ты не смылся!')
        print('монстр применил к тебе непотребство, уровень -1')
        current_level -= 1

open_door()