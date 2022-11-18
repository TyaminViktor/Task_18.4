import json, requests, telebot


class APIException(Exception):
    pass


class CryptoConversion:
    @staticmethod
    def get_price(payoff: str, count: str, obtain: str, keys: dict, bot: telebot, message: telebot.types.Message):
        if payoff == obtain:
            raise APIException("Перевод валюты самой в себя не требуется.")
        if payoff not in keys.keys():
            text = f"Валюта {payoff} не существует или недоступна для конвертации. Для получения списка конвертируемых валют нажмите /value"
            raise APIException(bot.reply_to(message, text))
        if obtain not in keys.keys():
            text = f"Валюта {obtain} не существует или недоступна для конвертации. Для получения списка конвертируемых валют нажмите /value"
            raise APIException(bot.reply_to(message, text))
        try:
            count = round(float(count), 2)
        except APIException:
            text = "Количество конвертируемой валюты должно быть числом, написанным цифрами"
            raise APIException(bot.reply_to(message, text))
        if count < 0:
            text = "Количество конвертируемой валюты не может быть меньше 0"
            raise APIException(bot.reply_to(message, text))
        if count == 0:
            text = "Нельзя конвертировать то, чего нет, детка!"
            raise APIException(bot.reply_to(message, text))
        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={keys[payoff]}&tsyms={keys[obtain]}")
        answer = json.loads(r.content)[keys[obtain]] * count
        return answer
