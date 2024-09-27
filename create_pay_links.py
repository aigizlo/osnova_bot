import requests
import hashlib
import json

import const


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
        "DATA": {
            "Phone": "+71234567890",  # Опционально
            "Email": "a@test.com"  # Опционально
            },
        "Receipt": {
            "Email": "a@test.ru",
            "Phone": "+79031234567",
            "Taxation": "osn",
            "Items": [
                {
                    "Name": "Наименование товара 1",
                    "Price": amount,
                    "Quantity": 1,
                    "Amount": amount,
                    "Tax": "vat10",
                    "Ean13": "303130323930303030630333435"
                },
            ]
        }
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
#         order_id="421",
#         description="Оплата заказа №12"
#     )
#     print(f"Payment URL: {payment_url}")
# except Exception as e:
#     print(f"Error: {str(e)}")
