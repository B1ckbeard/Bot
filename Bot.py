import telebot
from telebot.apihelper import ENABLE_MIDDLEWARE
import config
from telebot import types

import Com_service
import Com_service_35
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
    markup_inline.add(item1, item2)
    bot.send_message(message.chat.id, 'Выберите:', reply_markup = markup_inline)

@bot.callback_query_handler(func = lambda call: True)
def answer(call):
    if call.data == 'last':
        bot.send_message(call.message.chat.id, Com_service.select())
    elif call.data == 'add':
        markup_inline1 = types.InlineKeyboardMarkup()
        item3 = types.InlineKeyboardButton(text = 'Light', callback_data= 'light')
        item4 = types.InlineKeyboardButton(text = 'Cold_Water', callback_data= 'c_water')
        item5 = types.InlineKeyboardButton(text = 'Hot_Water', callback_data= 'h_water')
        item6 = types.InlineKeyboardButton(text = 'Save', callback_data= 'save')

        markup_inline1.add(item3, item4, item5, item6)
        bot.send_message(call.message.chat.id, 'Выберите:', reply_markup = markup_inline1)
    elif call.data == 'light':
        sent = bot.send_message(call.message.chat.id, 'Введите показание счетчика электроэнергии:')
        bot.register_next_step_handler(sent, electricityIndication)
    elif call.data == 'c_water':
        sent = bot.send_message(call.message.chat.id, 'Введите показание счетчика холодной воды:')
        bot.register_next_step_handler(sent, coldWaterIndication)
    elif call.data == 'h_water':
        sent = bot.send_message(call.message.chat.id, 'Введите показание счетчика горячей воды:')
        bot.register_next_step_handler(sent, hotWaterIndication)
    elif call.data == 'save':
        bot.send_message(call.message.chat.id, 'Сохранено')
        saveData()
        markup_inline2 = types.InlineKeyboardMarkup()
        item7 = types.InlineKeyboardButton(text = 'сумма', callback_data= 'price')
        markup_inline2.add(item7)
        bot.send_message(call.message.chat.id, 'Посчитать сумму?', reply_markup = markup_inline2)
    elif call.data == 'price':
        sent = bot.send_message(call.message.chat.id, Com_service.priceSum())

def electricityIndication(message):
    global el_ind
    el_ind = message.text
    bot.send_message(message.chat.id, f'{message.text}, Ok')

def coldWaterIndication(message):
    global c_water
    c_water = message.text
    bot.send_message(message.chat.id, f'{message.text}, Ok')

def hotWaterIndication(message):
    global h_water
    h_water = message.text
    bot.send_message(message.chat.id, f'{message.text}, Ok')
    
def saveData():
    Com_service.db_table_add(float(el_ind), float(c_water), float(h_water))
    print('data saved')



'''
@bot.message_handler(content_types=['text'])
def send_hello(message):
    if message.text == 'привет' or message.text == 'Привет':
        bot.send_message(message.from_user.id, 'Привет!')
    elif message.text == 'Пока' or message.text == 'пока':
        bot.send_message(message.from_user.id, 'Всего хорошего!')
    elif message.text == 'Мяу':
        bot.send_message(message.from_user.id, 'мау-мау)')'''


bot.polling(none_stop=True)
