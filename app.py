import telebot
from config import curr, TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands = ['start', 'help'])
def help(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Добро пожаловать, {message.chat.username}!")
    text = 'Чтобы начать работу, введите команду боту в следующем формате: \n <имя валюты>' \
           ' <в какую валюту перевести>' \
           ' <количество переводимой валюты>' \
           '\nПример запроса: доллар рубль 10.25\n' \
           '\nВалюты можно вводить в произвольном регистре. Для корректной обработки запросов все значения будут приведены к нижнему регистру.' \
           '\nКоличество переводимой валюты может быть неотрицательным числом (целым или дробным).' \
           '\n\nДля просмотра всех доступных валют введите команду /values.'
    bot.reply_to(message, text)

@bot.message_handler(commands = ['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for vl in curr.keys():
        text = '\n - '.join((text, vl,))
    text += '\n\nПример запроса: доллар рубль 10.25'
    bot.reply_to(message, text)

@bot.message_handler(content_types = ['text'])
def convert(message: telebot.types.Message):
     try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Количество параметров должно быть равно трем. Подробнее - /help')

        # имя валюты, цену на которую надо узнать — base,
        # имя валюты, цену в которой надо узнать — quote,
        # количество переводимой валюты — amount
        base, qoute, amount = values
        total_qoute = CurrencyConverter.get_price(base, qoute, amount)
     except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
     except Exception as e:
        bot.reply_to(message, f'Ошибка приложения. Не удалось обработать команду.\n{e}')
     else:
        text = f"{amount} {curr[base.lower()]} = {total_qoute} {curr[qoute.lower()]} ({base.lower()} ➔ {qoute.lower()})"
        bot.send_message(message.chat.id, text)

bot.polling()