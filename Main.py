import telebot
#from telebot.apihelper import ENABLE_MIDDLEWARE
import config
from telebot import types
#from telebot.types import *

import Com_service
#import Com_service_35
#import Munchkin
#import Dice_roll

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "Добро пожаловать!")

@bot.message_handler(commands=['flat25'])
def get_user_info(message):
    markup_inline = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton(text = 'Last info', callback_data= 'last')
    item2 = types.InlineKeyboardButton(text = 'Add', callback_data= 'add')
    item3 = types.InlineKeyboardButton(text = 'Delete last', callback_data= 'del')
    markup_inline.add(item1, item2, item3)
    bot.send_message(message.chat.id, 'Выберите:', reply_markup = markup_inline)

@bot.callback_query_handler(func = lambda call: True)
def answer(call):
    if call.data == 'last':
        bot.send_message(call.message.chat.id, Com_service.select())
    elif call.data == 'add':
        mes1 = bot.send_message(call.message.chat.id, 'Введите показание счетчика электроэнергии:')
        bot.register_next_step_handler(mes1, electricityIndication)
    elif call.data == 'save':#сохранить показания в БД
        saveData()
        bot.send_message(call.message.chat.id, 'Сохранено')
        markup_inline2 = types.InlineKeyboardMarkup()
        item3 = types.InlineKeyboardButton(text = 'сумма', callback_data= 'price')
        markup_inline2.add(item3)
        bot.send_message(call.message.chat.id, 'Посчитать сумму?', reply_markup = markup_inline2)
    elif call.data == 'price':#пок. в текущем месяце - пок. пред. месяца * тариф
        sent = bot.send_message(call.message.chat.id, Com_service.priceSum())
    elif call.data == 'del':
        bot.send_message(call.message.chat.id, 'Последняя запись удалена')


def electricityIndication(message):
    global el_ind
    el_ind = message.text
    #bot.send_message(message.chat.id, f'{message.text}, Ok')
    if message != '':
        mes2 = bot.send_message(message.chat.id, 'Введите показание счетчика холодной воды:')
        bot.register_next_step_handler(mes2, coldWaterIndication)

def coldWaterIndication(message):
    global c_water
    c_water = message.text
    #bot.send_message(message.chat.id, f'{message.text}, Ok')
    if message != '':
        mes3 = bot.send_message(message.chat.id, 'Введите показание счетчика горячей воды:')
        bot.register_next_step_handler(mes3, hotWaterIndication)

def hotWaterIndication(message):
    global h_water
    h_water = message.text
    #bot.send_message(message.chat.id, f'{message.text}, Ok')
    showInditations(message)

def showInditations(message):
    bot.send_message(message.chat.id, f'свет: {el_ind}, х_вода: {c_water}, г_вода: {h_water}')
    markup_inline2 = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton(text = 'Save', callback_data= 'save')
    markup_inline2.add(item1)
    bot.send_message(message.chat.id, 'Сохранить?', reply_markup = markup_inline2)
    
#Сохранить показания в БД
def saveData():
    Com_service.db_table_add(float(el_ind), float(c_water), float(h_water))
    print('data saved')
    
#Удалить последнюю запись
def delData():
    Com_service.delLast()


@bot.message_handler(content_types=['text'])
def send_hello(message):
    if message.text == 'привет' or message.text == 'Привет':
        bot.send_message(message.from_user.id, 'Привет!')
    elif message.text == 'Пока' or message.text == 'пока':
        bot.send_message(message.from_user.id, 'Всего хорошего!')
    elif message.text == 'Мяу':
        bot.send_message(message.from_user.id, 'мау-мау)')

bot.polling(none_stop=True)
