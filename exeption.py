import requests
import json
from config import exchanges

class ConvertionExeption(Exception):
    pass

class ExchangeConverter():
    @staticmethod
    def Convert (quote, base, amount):
        try:
            quote_key = exchanges[quote.lower()]
        except KeyError:
            raise ConvertionExeption(f"Валюта {quote} не найдена!")

        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise ConvertionExeption(f"Валюта {base} не найдена!")

        if quote_key == base_key:
            raise ConvertionExeption(f'Нельзя перевести одинаковые валюты {base}. Измените валюту')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionExeption(f'Не удалось обработать количество {amount}')

        r = requests.get(f"https://api.exchangeratesapi.io/latest?base={quote_key}&symbols={base_key}")
        resp = json.loads(r.content)
        new_price = resp['rates'][base_key] * amount
        new_price = round(new_price, 3)
        message = f"Цена {amount} {quote} в {base} : {new_price}"
        return message