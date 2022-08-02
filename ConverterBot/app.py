import telebot
from config import TOKEN, keys
from extensions import Converter, ConversionException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def start_help(message: telebot.types.Message):
    text = "Это бот для конвертации валют.\nВводить данные надо в следующем формате:\n<имя конвертируемой валюты>, " \
           "<имя валюты, в которую хотите конвертировать первую>, <количество конвертируемой валюты>\nПосмотреть " \
           "список всех доступных валют: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text"])
def convert(message: telebot.types.Message):
    try:
        data = message.text.split(", ")

        if len(data) != 3:
            raise ConversionException("Неверное число параметров")

        quote, base, amount = data
        price = Converter.get_price(quote, base, amount)
    except ConversionException as e:
        bot.reply_to(message, f"Пользовательская ошибка:\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду:\n{e}")
    else:
        text = f"Цена {amount} {quote[0].upper() + quote[1::].lower()} в" \
               f" {base[0].upper() + base[1::].lower()} равна {price * float(amount)}"
        bot.send_message(message.chat.id, text)


bot.polling()
