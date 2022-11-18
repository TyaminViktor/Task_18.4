import telebot
from Extensions import APIException, CryptoConversion
from Config import token, keys

bot = telebot.TeleBot(token)


@bot.message_handler(commands=["start", "help"])
def starter(message: telebot.types.Message):
    text = "Для конвертации валют введите следущие параметры через пробел: \n'имя конвертируемой валюты' \
'количество конвертируемой валюты' \
'имя конечной валюты' \
\nДля получения списка конвертируемых валют нажмите /value"
    bot.reply_to(message, text)


@bot.message_handler(commands=["value"])
def currency(message: telebot.types.Message):
    text = "Доступные к конвертации валюты:"
    for key in keys.keys():
        text = "\n".join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text"])
def convertasion(message: telebot.types.Message):
    data = message.text.split(" ")
    try:
        if len(data) != 3:
            raise APIException("Задано неверное количество параметров.")
        payoff, count, obtain = data
        answer = CryptoConversion.get_price(payoff, count, obtain, keys, bot, message)
    except APIException as e:
        bot.reply_to(message, f"Ввод неверных данных пользователем \n {e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду \n {e}")
    else:
        text = f"Результат конвертации {count} {payoff} в {obtain} - {answer}"
        bot.reply_to(message, text)


bot.polling(none_stop=True)
