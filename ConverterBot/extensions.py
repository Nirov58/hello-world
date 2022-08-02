import requests
import json
from config import keys


class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise ConversionException("Указаны одинаковые валюты")

        try:
            quote_ticker = keys[quote[0].upper() + quote[1::].lower()]
        except KeyError:
            raise ConversionException(f"Не удалось обработать валюту {quote}")

        try:
            base_ticker = keys[base[0].upper() + base[1::].lower()]
        except KeyError:
            raise ConversionException(f"Не удалось обработать валюту {base}")

        try:
            amount = float(amount)
        except ValueError:
            raise ConversionException(f"Не удалось обработать число валюты")

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")
        price = json.loads(r.content)[base_ticker]
        return price


class ConversionException(Exception):
    pass
