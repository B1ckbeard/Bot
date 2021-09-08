import telebot
#from telebot.apihelper import ENABLE_MIDDLEWARE
import config
from telebot import types

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
    item1 = types.InlineKeyboardButton(text = 'Last info', callback_data = 'last')
    item2 = types.InlineKeyboardButton(text = 'Last Sum', callback_data = 'price')
    item3 = types.InlineKeyboardButton(text = 'Delete last', callback_data = 'del_question')
    item4 = types.InlineKeyboardButton(text = 'Add', callback_data = 'add')
    markup_inline.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id, 'Выберите:', reply_markup = markup_inline)

@bot.callback_query_handler(func = lambda call: True)
def answer(call):
    if call.data == 'last':
        bot.send_message(call.message.chat.id, Com_service.select_last_record())
    elif call.data == 'add':
        indicationMethodChoice(call.message, 'elec')
    elif call.data == 'save':#сохранить показания в БД
        saveData(call.message)
        #добавить в метод суммы
        markup_inline2 = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text = 'сумма', callback_data = 'price')
        markup_inline2.add(item1)
        bot.send_message(call.message.chat.id, 'Посчитать сумму?', reply_markup = markup_inline2)
    elif call.data == 'price':#пок. в текущем месяце - пок. пред. месяца * тариф
        bot.send_message(call.message.chat.id, Com_service.price_sum())
    elif call.data == 'del_question':
        markup_inline3 = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text= 'Удалить', callback_data= 'del')
        markup_inline3.add(item1)
        bot.send_message(call.message.chat.id, 'Вы действительно хотите удалить последнюю запись?', reply_markup=markup_inline3)
    elif call.data == 'del':
        delData(call.message)

def indicationMethodChoice(message, met):
    if met == 'elec':
        mes1 = bot.send_message(message.chat.id, 'Введите показание счетчика электроэнергии:')
        bot.register_next_step_handler(mes1, electricityIndication)
    elif met == 'c_water':
        mes1 = bot.send_message(message.chat.id, 'Введите показание счетчика холодной воды:')
        bot.register_next_step_handler(mes1, coldWaterIndication)
    elif met == 'h_water':
        mes1 = bot.send_message(message.chat.id, 'Введите показание счетчика горячей воды:')
        bot.register_next_step_handler(mes1, hotWaterIndication)

def electricityIndication(message):
    try:
        global el_ind
        el_ind = float(message.text)
    except ValueError as error:
        bot.send_message(message.chat.id, f'Неверный тип данных "{error} ", повторите ввод')
        indicationMethodChoice(message, 'elec')
    else:
        bot.send_message(message.chat.id, f'{message.text}, Ok')
        indicationMethodChoice(message, 'c_water')

def coldWaterIndication(message):
    try:
        global c_water
        c_water = float(message.text)
    except ValueError as error:
        bot.send_message(message.chat.id, f'Неверный тип данных "{error} ", повторите ввод')
        indicationMethodChoice(message, 'c_water')
    else:
        bot.send_message(message.chat.id, f'{message.text}, Ok')
        indicationMethodChoice(message, 'h_water')

def hotWaterIndication(message):
    try:
        global h_water
        h_water = float(message.text)
    except ValueError as error:
        bot.send_message(message.chat.id, f'Неверный тип данных "{error} ", повторите ввод')
        indicationMethodChoice(message, 'h_water')
    else:
        bot.send_message(message.chat.id, f'{message.text}, Ok')
        showInditations(message)

def showInditations(message):#показать введенные данные
    bot.send_message(message.chat.id, f'свет: {el_ind}, х_вода: {c_water}, г_вода: {h_water}')
    markup_inline2 = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton(text = 'Save', callback_data= 'save')
    markup_inline2.add(item1)
    bot.send_message(message.chat.id, 'Сохранить?', reply_markup = markup_inline2)
    
def saveData(message):#Сохранить показания в БД
    Com_service.db_table_add(float(el_ind), float(c_water), float(h_water))
    print('data saved')
    bot.send_message(message.chat.id, 'Сохранено')

def delData(message):#Удалить последнюю запись
    Com_service.delete_last_record()
    bot.send_message(message.chat.id, 'Последняя запись удалена')

@bot.message_handler(content_types=['text'])
def send_hello(message):
    if message.text == 'привет' or message.text == 'Привет':
        bot.send_message(message.from_user.id, 'Привет!')
    elif message.text == 'Пока' or message.text == 'пока':
        bot.send_message(message.from_user.id, 'Всего хорошего!')
    elif message.text == 'Мяу':
        bot.send_message(message.from_user.id, 'мау-мау)')

bot.polling(none_stop=True)