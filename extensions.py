import requests
import json
from config import curr

class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base: str, qoute: str, amount: str):
        base = base.lower()
        qoute =qoute.lower()
        if qoute == base:
            raise APIException('Не допускается ввод одинаковых валют! Подробнее - /help')
        try:
            base_ticker = curr[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}. Для просмотра списка доступных валют используйте команду /values')

        try:
            qoute_ticker = curr[qoute]
        except KeyError as e:
            raise APIException(f'Не удалось обработать валюту {qoute}')

        try:
            amount = float(amount)
        except ValueError as e:
            raise APIException(f'Не удалось обработать количество {amount}.'
                               f'\n\nКоличество переводимой валюты может быть неотрицательным числом (целым или дробным). Подробнее - /help')

        if float(amount) < 0:
            raise APIException(f'Количество валюты ({amount}) должно быть неотрицательным числом. Пожалуйста, повторите ввод. Подробнее - /help')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={qoute_ticker}')
        total_qoute = round(json.loads(r.content)[curr[qoute]] * amount, 2)

        return total_qoute