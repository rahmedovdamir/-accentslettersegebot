import telebot
import random

TOKEN = '6852173996:AAHJTJPjSdUyhbkMiTRPAVB1iM9SNt-BRr4'

bot = telebot.TeleBot(TOKEN)

word = None


@bot.message_handler(commands=['start'])
def start(message):
    options1 = ['да', 'нет']
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    buttons = [telebot.types.InlineKeyboardButton(text=option1, callback_data=option1) for option1 in options1]
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, 'Привет! Хочешь поработать?', reply_markup=keyboard)


def modify_vowels(words):
    vowels = 'аеёиоуыэюя'
    result = []

    for index, letter in enumerate(words):
        if letter.lower() in vowels:
            modified_word = words[:index] + letter.upper() + words[index + 1:]
            result.append(modified_word)

    return result


@bot.message_handler(func=lambda message: 'да' in message.text.lower())
def work(message):
    with open('Ударения.txt', 'r', encoding='utf-8') as file:
        words = file.read().splitlines()

    global word

    word = random.choice(words)

    options = modify_vowels(word.lower())

    question = f'Какое правильное ударение в слове "{word.lower()}"?'

    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    buttons = [telebot.types.InlineKeyboardButton(text=option, callback_data=option) for option in options]
    keyboard.add(*buttons)

    bot.send_message(message.chat.id, question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == 'да':
        work(call.message)
    elif call.data == 'нет':
        bot.send_message(call.message.chat.id, 'Удачи!')
    if call.data == word:
        options1 = ['да', 'нет']
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
        buttons = [telebot.types.InlineKeyboardButton(text=option1, callback_data=option1) for option1 in options1]
        keyboard.add(*buttons)
        bot.send_message(call.message.chat.id, 'Молодец! Хочешь продолжить?', reply_markup=keyboard)
    if call.data != word and call.data != 'да' and call.data != 'нет':
        bot.send_message(call.message.chat.id, 'Неверно! Ты можешь попробовать еще раз! Либо продолжить работу с новыми словами!')


bot.polling()
