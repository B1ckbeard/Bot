import random

start_lvl = 1
cur_lvl = start_lvl
max_level = 10
start_gain = 0
gain = start_gain
bonus_gain = start_gain
power = cur_lvl + gain

cards_list = ['monster', 'curse', 'gain']

def open_door():
    global cur_lvl, gain, power, bonus_gain
    print('Тук-тук')
    print('твой уровень: ', + cur_lvl)
    print('твоя сила:', + power)

    card = random.choice(cards_list)
    if card == 'monster':
        monster_power = random.randint(0, 10)
        print('тебе досталась карта монстра с силой ', + monster_power)
        if power <= monster_power:
            number = random.randint(1, 6)
            print('монстр сильнее, попытаемся смыться, бросаем кубик')
            print('Выпало', + number)
            if number >= 4:
                print('ты слинял')
            elif number < 4:
                print('ты не смылся!')
                print('монстр применил к тебе непотребство, твой уровень -1')
                cur_lvl -= 1
        else:
            print('Ты победил монстра!, твой уровень +1')
            cur_lvl += 1
    elif card == 'gain':
        bonus_gain = start_gain
        bonus_gain += random.randint(1, 5)
        gain += bonus_gain
        print('Тебе выпало усиление +', bonus_gain)
    elif card == 'curse':
        print('тебе выпало проклятье, твой уровень -1')
        cur_lvl -= 1

    if cur_lvl == max_level:
        print('ты победил!')
    if cur_lvl <= 0:
        cur_lvl = 1
    power = gain + cur_lvl
    print('1lvl: ', + cur_lvl)
    print('gain: ', + gain)
    print('1power: ', + power)
    knock_knock()

def knock_knock():
    print('постучать в дверь снова?')
    answer = input()
    if answer == 'y':
        open_door()

open_door()