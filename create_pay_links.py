import requests
import hashlib
import json

import const
from logger import logger


def create_payment_link(amount, order_id, description):
    password = const.TERMINALPASSWORD
    terminal_key = const.TERMINALKEY
    url = 'https://securepay.tinkoff.ru/v2/Init'

    # Убедимся, что amount - это целое число
    amount = int(amount)

    # Создаем словарь с параметрами для токена
    token_params = {
        "Amount": str(amount),
        "Description": description,
        "OrderId": order_id,
        "Password": password,
        "TerminalKey": terminal_key
    }

    # Сортируем ключи словаря
    sorted_keys = sorted(token_params.keys())

    # Создаем строку для токена
    token_string = ''.join(token_params[key] for key in sorted_keys)

    # Создаем токен с помощью SHA-256
    token = hashlib.sha256(token_string.encode('utf-8')).hexdigest()

    # Создаем payload для запроса
    payload = {
        "TerminalKey": terminal_key,
        "Amount": amount,
        "OrderId": order_id,
        "Description": description,
        "Token": token,
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        result = response.json()
        print(result)

        if result.get("Success"):
            return result.get("PaymentURL")
        else:
            error_code = result.get("ErrorCode")
            error_message = result.get("Message")
            raise Exception(f"Error {error_code}: {error_message}")

    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")


# # Пример использования
# try:
#     payment_url = create_payment_link(
#         amount=10000,  # Сумма в копейках
#         order_id="4321",
#         description="Оплата заказа №12"
#     )
#     print(f"Payment URL: {payment_url}")
# except Exception as e:
#     print(f"Error: {str(e)}")

def create_pay_link_crypto(amount, order_id, description):
    import const
    amount = float(amount)
    url = "https://api.cryptocloud.plus/v1/invoice/create"
    headers = {
        "Authorization": f"Token {const.crypto_API}",
        "Content-Type": "application/json"
    }

    data = {
        'shop_id': const.crypto_shop_id,
        "amount": amount,
        "currency": "USD",
        "description": description,
        'order_id': order_id,
    }

    response = requests.post(url, headers=headers, json=data)

    result = response.json()

    # Проверяем ответ
    if response.status_code == 200:
        print("Success:", response.json())
        url = result.get('pay_url')
        invoice_id = result.get('invoice_id')
        logger.info(f'Ссылка для оплаты криптой успешно создана {url}')
        return url, invoice_id
    else:
        logger.error("Fail:", response.status_code, response.text)
        return False, False

# Пример использования
# try:
#     payment_url = create_pay_link_crypto(
#         amount=100,  # Сумма в копейках
#         order_id="1",
#         description="Оплата заказа №12"
#     )
#     print(f"Payment URL: {payment_url}")
# except Exception as e:
#     print(f"Error: {str(e)}")
