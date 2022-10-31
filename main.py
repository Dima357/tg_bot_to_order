import telebot
from telebot import types

bot = telebot.TeleBot("TOKEN")


@bot.message_handler(commands=['start'])
def start(message):
    home_photo = open('floor/home_photo.jpeg', 'rb')
    markup = types.InlineKeyboardMarkup()
    help = types.InlineKeyboardButton('Помощь', callback_data='Помощь')
    choice = types.InlineKeyboardButton('Виды полов', callback_data='Виды полов')
    basket = types.InlineKeyboardButton('Корзина', callback_data='Корзина')
    markup.add(help, choice, basket)
    try:
        bot.edit_message_caption(chat_id=message.chat.id, message_id=message.id,
                                 caption='', reply_markup=markup)
    except telebot.apihelper.ApiTelegramException:
        bot.delete_message(chat_id=message.chat.id, message_id=message.id)
        bot.send_photo(message.chat.id, home_photo, reply_markup=markup, parse_mode='html')


@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback_data(callback):
    if callback.data == 'Меню':
        start(callback.message)
    elif callback.data == 'Помощь':
        help(callback.message)
    elif callback.data == 'Виды полов':
        choice(callback.message)
    elif callback.data == 'Водяной':
        water_floor(callback.message)
    elif callback.data == 'Электрический':
        electric_floor(callback.message)
    elif callback.data == 'Электро-водяной':
        blend_floor(callback.message)
    elif callback.data == 'Корзина':
        basket(callback.message)
    elif callback.data == 'Оплатить заказ':
        pay(callback.message)
    else:
        bot.send_message(chat_id=callback.message.chat.id, text='Произошла ошибка')


@bot.message_handler(commands=['help'])
def help(message):
    home_photo = open('floor/home_photo.jpeg', 'rb')
    greet = 'Бот для подбора теплых полов\n' \
            'Вы можете указать текстом команды\n' \
            'Например: меню, помощь, виды полов'
    markup = types.InlineKeyboardMarkup(row_width=1)
    back = types.InlineKeyboardButton(text='<< Меню', callback_data='Меню')
    markup.add(back)
    try:
        bot.edit_message_caption(chat_id=message.chat.id, message_id=message.id,
                                 caption=greet, reply_markup=markup)
    except telebot.apihelper.ApiTelegramException:
        bot.delete_message(chat_id=message.chat.id, message_id=message.id)
        bot.send_photo(chat_id=message.chat.id, photo=home_photo, caption=greet, reply_markup=markup)


def choice(message):
    home_photo = open('floor/home_photo.jpeg', 'rb')
    greet = 'Виды полов:'
    markup = types.InlineKeyboardMarkup(row_width=3)
    water = types.InlineKeyboardButton(text='Водяной', callback_data='Водяной')
    electric = types.InlineKeyboardButton(text='Электрический', callback_data='Электрический')
    blend = types.InlineKeyboardButton(text='Электро-водяной', callback_data='Электро-водяной')
    basket = types.InlineKeyboardButton(text='Корзина', callback_data='Корзина')
    back = types.InlineKeyboardButton(text='<< Меню', callback_data='Меню')
    markup.add(water, electric, blend, back, basket)
    try:
        bot.edit_message_caption(chat_id=message.chat.id, message_id=message.id,
                                 caption=greet, reply_markup=markup)
    except telebot.apihelper.ApiTelegramException:
        bot.delete_message(chat_id=message.chat.id, message_id=message.id)
        bot.send_photo(message.chat.id, home_photo, greet, reply_markup=markup)


def basket(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    calculate_money = types.InlineKeyboardButton(text='Оплатить заказ', callback_data='Оплатить заказ')
    back = types.InlineKeyboardButton(text='<< Меню', callback_data='Меню')
    markup.add(calculate_money, back)
    bot.edit_message_caption(chat_id=message.chat.id, message_id=message.id,
                             caption='Корзина', reply_markup=markup)


def pay(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    menu = types.InlineKeyboardButton(text='Меню', callback_data='Меню')
    basket = types.InlineKeyboardButton(text='Корзина', callback_data='Корзина')
    markup.add(basket, menu)
    bot.edit_message_caption(chat_id=message.chat.id, message_id=message.id,
                             caption='Оплата', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def text_from_user(message):
    if 'меню' in message.text.lower():
        start(message)
    elif 'помощь' in message.text.lower():
        help(message)
    else:
        answer = 'Проверьте правильность ввода\n'\
                         'Возможные варианты\n' \
                         'меню, помощь'
        bot.send_message(message.chat.id, answer)


bot.infinity_polling()
