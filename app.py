import telebot
from config import exchanges, TOKEN
import traceback
from exeption import ConvertionExeption, ExchangeConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду в следующем формате: \n <имя валюты> \
\n <в какую валюту перевести> \
\n <количество переводимой валюты> \
\n Посмотреть список валют: /values'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in exchanges.keys():
        text = '\n' .join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def Convertor(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise ConvertionExeption('Неверное количество параметров!')

        answer = ExchangeConverter.get_price(*values)
    except ConvertionExeption as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)

bot.polling()
