# -*- coding: utf-8 -*-
import asyncio

from flask import Flask, render_template, request, jsonify

# import logger
from logger import logger

import sub
import user_data
from config import support, dp, bot
app = Flask(__name__)


@app.route('/withdraw')
def withdraw():
    pending_requests = user_data.execute_query("SELECT * FROM withdrawal_requests WHERE status = 'pending'")
    confirmed_requests = user_data.execute_query("SELECT * FROM withdrawal_requests WHERE status = 'confirmed'")

    # Преобразуем результаты запроса в список словарей для удобства использования в шаблоне
    pending_requests = [dict(zip(['id', 'user_id', 'amount', 'status', 'wallet', 'created_at'], row)) for row in pending_requests]
    confirmed_requests = [dict(zip(['id', 'user_id', 'amount', 'status', 'wallet', 'created_at'], row)) for row in confirmed_requests]

    return render_template('withdraw_req.html', pending_requests=pending_requests, confirmed_requests=confirmed_requests)


@app.route('/update_status/<int:id>', methods=['POST'])
def update_status(id):
    data = request.json
    new_status = data['status']

    try:
        # Обновляем статус
        user_data.execute_query(
            "UPDATE withdrawal_requests SET status = %s WHERE id = %s;",
            (new_status, id)
        )

        # Получаем user_id
        user_id_result = user_data.execute_query("SELECT user_id, amount FROM withdrawal_requests WHERE id = %s;", (id,))
        print(user_id_result, ' user_id_result')

        if user_id_result and len(user_id_result) > 0:
            user_id = user_id_result[0][0]
            amount = user_id_result[0][1]
            print(user_id, ' user_id')
            send_message_sync(bot, user_id, "Ваш запрос был обработан, ожидайте пополнение на кошелек")

            user_data.add_referral_balance(user_id, -float(amount), 'withdraw')

            success = True
        else:
            user_id = None
            success = False
    except Exception as e:
        print(f"Error updating status: {e}")
        user_id = None
        success = False

    return jsonify({'success': success, 'user_id': user_id})

@app.route('/statistic')
def index():
    user_data_ = user_data.show_user_data()
    links = user_data.show_links_info()
    sale_stats = sub.get_sale_stats()
    sale_paracents = sub.sale_paracent(sale_stats)
    count = user_data.all_users()
    return render_template('index.html', users=user_data_, links=links, sale_stats=sale_stats,
                           sale_paracents=sale_paracents, count=count)


@app.route('/sucsseful/')
def sucssefull_pay():
    return render_template('sucsseful.html')

@app.route('/filed/')
def filed_pay():
    return render_template('filed.html')

async def send_message_async(bot, chat_id, text):
    await bot.send_message(chat_id, text)

def send_message_sync(bot, chat_id, text):
    asyncio.run(send_message_async(bot, chat_id, text))


from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/notify', methods=['POST'])
def handle_postback():
    secret_token = '1boosZTJtRZQplpqeeeJ59Y4HFdRNau6U5yM'
    # Изменено на request.form для обработки данных в формате x-www-form-urlencoded
    status = request.form.get('status')
    invoice_id = request.form.get('invoice_id')
    amount_crypto = request.form.get('amount_crypto')
    currency = request.form.get('currency')
    order_id = request.form.get('order_id')
    token = request.form.get('token')
    if secret_token != token:
        return 300, 'неверный токен'
    if status == "success":
        logger.info(f'счет {invoice_id} ')


    # ... ваш код для обработки postback ...

    return jsonify({'message': 'Postback received'}), 200

if __name__ == '__main__':
    app.run(debug=True)
