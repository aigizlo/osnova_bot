import asyncio
import time

from aiogram import types
from aiogram.utils.exceptions import TelegramAPIError
import notifikation
import balance
import promo
import sub
import text
import keyboards
import user_data
from balance import add_withdrawal_request
from states import MyStates
from config import bot, dp
import aiogram
from aiogram.dispatcher import FSMContext
from logger import logger
import config
import const
import create_pay_links
from promo import generate_promo_code


@dp.callback_query_handler(lambda c: c.data.startswith("period:"), state='*')
async def select_period(callback_query: types.CallbackQuery, state: FSMContext):
    user_data_state = await state.get_data()
    user_id = callback_query.message.chat.id

    try:
        month = int(callback_query.data.split(':')[1])  # извлекаем месяц
    except Exception as e:
        try:
            month = user_data_state['month']
        except Exception as e:
            await bot.send_message(chat_id=user_id, text="Начните процесс оплаты сначала",
                                   reply_markup=keyboards.main_menu())
            try:
                if callback_query.message.message_id:
                    await bot.delete_message(chat_id=user_id, message_id=callback_query.message.message_id)
                    return
            except aiogram.utils.exceptions.MessageCantBeDeleted:
                logger.info("Сообщение не может быть удалено.")
                return

    price = config.prices.get(str(month))  # получаем цену, используя строковый ключ
    days = config.get_days.get(month)  # получаем дни, используя целочисленный ключ

    txt_tarrif_info = text.tarrif_info(month, price, days)
    try:
        if callback_query.message.message_id:
            await bot.delete_message(chat_id=user_id, message_id=callback_query.message.message_id)
    except aiogram.utils.exceptions.MessageCantBeDeleted:
        logger.info("Сообщение не может быть удалено.")
    logger.info(f" - {user_id}")

    # await state.set_state(MyStates.go_to_pay)
    # await state.set_state(MyStates.present_promo_state)
    await state.update_data(month=month, price=price, days=days)

    # отправляем информационное сообщение
    await bot.send_message(chat_id=user_id,
                           text=txt_tarrif_info,
                           parse_mode="HTML",
                           # Оплатить
                           # Применить промокод
                           # Подарить подписку
                           # Назад
                           reply_markup=keyboards.select_pay_method())
    logger.info(f'user_id - {user_id}, period - {month} месяц')


@dp.callback_query_handler(lambda c: c.data.startswith("go_pay"), state='*')
async def select_go_to_pay(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.message.chat.id
    user_data_state = await state.get_data()
    # 💳 Оплатить
    month = user_data_state['month']
    price = config.prices.get(str(month))  # получаем цену, используя строковый ключ
    days = config.get_days.get(month)  # получаем дни, используя целочисленный ключ

    txt_tarrif_info = text.tarrif_info_2(month, price, days)
    try:
        if callback_query.message.message_id:
            await bot.delete_message(chat_id=user_id, message_id=callback_query.message.message_id)
    except aiogram.utils.exceptions.MessageCantBeDeleted:
        logger.info("Сообщение не может быть удалено.")

    await state.set_state(MyStates.select_pay_method)

    logger.info('ждем select_pay_method')

    # отправляем информационное сообщение
    await bot.send_message(chat_id=user_id,
                           text=txt_tarrif_info,
                           parse_mode="HTML",
                           disable_web_page_preview=True,
                           # Перейти к оплате
                           # Назад
                           reply_markup=keyboards.go_to_pay())
    logger.info(f'user_id {user_id} - 💳 Оплатить {month} месяцев')


@dp.callback_query_handler(lambda c: c.data.startswith("select_pay_method"), state=MyStates.select_pay_method)
async def select_pay_method(callback_query: types.CallbackQuery, state: FSMContext):
    # Перейти к оплате
    user_data_state = await state.get_data()
    print('select_pay_method')
    month = user_data_state['month']
    user_id = callback_query.message.chat.id
    price = int(user_data_state['price'])  # получаем цену, используя строковый ключ
    logger.info(f' price {price}')
    days = user_data_state['days']  # получаем дни, используя целочисленный ключ
    pay_id = balance.create_pay_id(user_id, float(str(price) + '.00'))
    logger.info(price * 100)
    logger.info('--------------')
    logger.info(pay_id)
    await state.update_data(pay_id=pay_id)

    payment_url = create_pay_links.create_payment_link(
        amount=price * 10000,  # Сумма в копейках
        order_id=str(pay_id),
        description=f"Оплата заказа {pay_id} для пользователя {user_id} на сумму {price}"
    )
    try:
        if callback_query.message.message_id:
            await bot.delete_message(chat_id=user_id, message_id=callback_query.message.message_id)
    except aiogram.utils.exceptions.MessageCantBeDeleted:
        logger.info("Сообщение не может быть удалено.")

    # await state.set_state(MyStates.card_method)
    # отправляем информационное сообщение
    await bot.send_message(chat_id=user_id,
                           text="Выберите способ оплаты",
                           parse_mode="HTML",
                           # Оплата картой
                           # Оплата USTD
                           reply_markup=keyboards.select_card_or_usdt(payment_url))
    logger.info(f'user_id {user_id} - Перейти к оплате {month} месяцев {days} - дней {price} цена')

    time.sleep(10)

    await bot.send_message(chat_id=user_id,
                           text="Нажмите, для проверки платежа",
                           reply_markup=keyboards.check_status_payment())


@dp.callback_query_handler(lambda c: c.data.startswith("check_status_payment"), state='*')
async def select_check_status_payment(callback_query: types.CallbackQuery, state: FSMContext):
    logger.info('check_status_payment')

    user_data_state = await state.get_data()
    user_id = callback_query.message.chat.id
    user_name = callback_query.message.from_user.username
    first_name = callback_query.message.from_user.first_name
    last_name = callback_query.message.from_user.last_name


    ref_data = user_data.get_user_name_frst_name_last_name(user_id)
    logger.info(f'{ref_data} , ')

    try:
        pay_id = user_data_state['pay_id']
        logger.info(f"""'pay_id' {pay_id}""")
    except Exception as e:
        pay_id = balance.get_last_pay_id(user_id)
        logger.info(f"""'select_last_pay_id' {pay_id}""")

    if balance.check_status_transactions(int(pay_id)):
        await bot.send_message(chat_id=user_id,
                               text="Платеж уже обработан")
        try:
            if callback_query.message.message_id:
                await bot.delete_message(chat_id=user_id, message_id=callback_query.message.message_id)
        except Exception as e:
            logger.info("Сообщение не может быть удалено.")
        return

    pay_status = notifikation.check_order(pay_id)
    logger.info(f'{pay_status} - pay_status')
    promo_info = promo.get_promo_id_from_transactions(int(pay_id))

    logger.info(f'{pay_status[2]} - pay_status[2]')

    if promo_info and pay_status[0]:
        promo_code = promo_info[1]
        promo_perod = promo_info[2]
        logger.info(f'Подарочный промоко {promo_code} на {promo_perod} дней')
        answer = text.text_if_buy_promo(promo_code=promo_code,
                                        bot_name=const.bot_name,
                                        month=promo_perod / 30,
                                        ref_user_id=user_id)
        await bot.send_message(chat_id=user_id,
                               text=answer,
                               parse_mode='HTML')
        # Уведомляем админа
        await bot.send_message(chat_id=const.admin,
                               text=f"INFO: ПОКУПКА ПРОМОКОДА НА {promo_perod / 30} мес "
                                    f"- tg: {user_id}, \n"
                                    f"username: @{user_name}, \n"
                                    f"first_name: {first_name}, \n"
                                    f"last_name : {last_name}, \n")
        await referralka(user_id, pay_status[2], promo_perod)
        return

    if pay_status[0]:
        # Покупка прошла
        amount = pay_status[2]
        period = period_json.get(amount)
        await bot.send_message(chat_id=const.admin,
                               text=f"INFO: ПОКУПКА ПОДПИСКИ НА  {period / 30} мес "
                                    f"- tg: {user_id}, \n"
                                    f"username: @{user_name}, \n"
                                    f"first_name: {first_name}, \n"
                                    f"last_name : {last_name}, \n")
        sub_active, answer_if_user_buy = sub.activate_or_renewal_subscription(user_id, period)
        await referralka(user_id, amount, period)

        if not sub_active:
            await bot.send_message(user_id, "Произошла ошибка, обратитесь к администратору")
            return

        await asyncio.sleep(1)
        if answer_if_user_buy:
            await bot.send_message(user_id, answer_if_user_buy)
            return
        await bot.send_message(user_id, text.text_buy_tarif, reply_markup=keyboards.accept_button(),
                               parse_mode="HTML")
        member_channel = await bot.get_chat_member(chat_id=const.channel_id, user_id=user_id)
        member_chat = await bot.get_chat_member(chat_id=const.chat_id, user_id=user_id)

        if member_channel.status == 'kicked':
            await bot.unban_chat_member(chat_id=const.channel_id, user_id=user_id)
            logger.info(f"Пользователь  {user_id} разбанен в канане")

        if member_chat.status == 'kicked':
            await bot.unban_chat_member(chat_id=const.chat_id, user_id=user_id)
            logger.info(f"Пользователь  {user_id} разбанен в чате")
        logger.info(f'user_id - {user_id} купил подписку на  {period} дней')
        logger.info(sub_active)
        await state.finish()
        try:
            if callback_query.message.message_id:
                await bot.delete_message(chat_id=user_id, message_id=callback_query.message.message_id)
        except Exception as e:
            logger.info("Сообщение не может быть удалено.")

    else:
        await bot.send_message(chat_id=user_id,
                               text=pay_status[1], reply_markup=keyboards.check_status_payment())


period_json = {
    150000: 30,
    400000: 90,
    1500000: 365
}


async def referralka(user_id, amount, period):
    ref_trx = user_data.referral_transactions(user_id, float(amount))
    logger.info(f'{ref_trx}, ref_trx')
    if ref_trx:
        referer_user_id = user_data.get_referrer_user_id(user_id)
        ref_data = user_data.get_user_name_frst_name_last_name(user_id)
        logger.info(f'{ref_data} , ')
        answer = text.ref_send_if_buy(int(referer_user_id),
                                      first_name=ref_data[0],
                                      last_name=ref_data[1],
                                      user_name=ref_data[2],
                                      bot_name=const.bot_name,
                                      mounth=int(period / 30))
        await bot.send_message(referer_user_id, answer, parse_mode='HTML')


@dp.callback_query_handler(text="go_back", state="*")
async def select_go_back_(callback_query: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    await select_period(callback_query, state)


@dp.callback_query_handler(text="go_back_to_main", state="*")
async def select_go_back_to_main(callback_query: types.CallbackQuery, state: FSMContext):
    user_data_state = await state.get_data()
    user_id = callback_query.message.chat.id
    month = user_data_state.get('month')
    price = user_data_state.get('price')
    days = user_data_state.get('days')
    await state.update_data(present=None)

    txt_tarrif_info = text.tarrif_info(month, price, days)
    try:
        if callback_query.message.message_id:
            await bot.delete_message(chat_id=callback_query.message.chat.id,
                                     message_id=callback_query.message.message_id)
    except aiogram.utils.exceptions.MessageCantBeDeleted:
        logger.info("Сообщение не может быть удалено.")
    await bot.send_message(chat_id=callback_query.message.chat.id,
                           text=txt_tarrif_info,
                           parse_mode="HTML",
                           # 1 месяц - 30 дней - 15 USD
                           # 3 месяц - 90 дней - 40 USD
                           # 12 месяц - 365 дней - 150 USD
                           reply_markup=keyboards.keyboard_period())
    logger.info(f'user_id - {user_id} Вышел назад в глав меню')


@dp.callback_query_handler(text="accept_rules", state="*")
async def select_accept_rules(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.message.chat.id
    # Принимаю правила
    await bot.send_message(chat_id=user_id,
                           text="Подпишитесь на канал",
                           parse_mode="HTML",
                           # Подписаться
                           # Проверить подписку
                           reply_markup=keyboards.subscribe())

    logger.info(f'user_id - {user_id} Подписаться на канал')


@dp.callback_query_handler(lambda c: c.data == "subscribe_check", state="*")
async def select_subscribe_no_thanks(callback_query: types.CallbackQuery):
    user_id = callback_query.message.chat.id
    chat_member = await bot.get_chat_member(chat_id=const.channel_id,
                                            user_id=user_id)
    logger.info(f"BUTTON:subscribe_check user - {user_id}")
    if chat_member.status in ["member", "administrator", "creator", "owner"]:
        await bot.send_message(chat_id=user_id,
                               text="Проверка пройдена\n"
                                    "Вступай в наш чат",
                               reply_markup=keyboards.join_chat(),
                               # Чат «ФУНДАМЕНТАЛИСТЫ - вступить
                               parse_mode="HTML")
        logger.info(f"""user_id - {user_id} подписался на канал""")

        try:
            if callback_query.message.message_id:
                await bot.delete_message(chat_id=callback_query.message.chat.id,
                                         message_id=callback_query.message.message_id)
        except aiogram.utils.exceptions.MessageCantBeDeleted:
            logger.info("Сообщение не может быть удалено.")

    else:
        await bot.send_message(chat_id=user_id,
                               text="Проверка не пройдена\n"
                                    "Подпишитесь на канал",
                               reply_markup=keyboards.subscribe(),
                               # Подписаться на канал
                               # Пройти проверку
                               parse_mode="HTML")
        logger.info(f"""user_id - {user_id} НЕ подписался на канал""")
        try:
            if callback_query.message.message_id:
                await bot.delete_message(chat_id=callback_query.message.chat.id,
                                         message_id=callback_query.message.message_id)
        except aiogram.utils.exceptions.MessageCantBeDeleted:
            logger.error("Не удалось удалить сообщение")


@dp.callback_query_handler(text="renewal_sub", state="*")
async def select_renewal_sub(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.message.chat.id
    await state.update_data(present=None)

    # Принимаю правила
    await bot.send_message(chat_id=user_id,
                           text="Выберите срок продления",
                           parse_mode="HTML",
                           # 1 месяц - 30 дней - 15 USD
                           # 3 месяц - 90 дней - 40 USD
                           # 12 месяц - 365 дней - 150 USD
                           reply_markup=keyboards.keyboard_period())
    logger.info(f'user_id - {user_id} Продлить подписку')


@dp.callback_query_handler(text="withdraw_money", state="*")
async def request_wallet(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    data = user_data.get_status_withdraw(user_id)
    if data:
        data = data[0]
        logger.info(f'{data}')
        if data[3] == "pending":
            await bot.send_message(user_id,
                                   "Ваша заявка в обработке, ожидайте решения")
            await bot.send_message(user_id,
                                   f"Кошелек - {data[4]}\n"
                                   f"Сумма - {data[2]}",
                                   reply_markup=keyboards.cansel_withdraw())
            return
    await bot.send_message(user_id,
                           "‼️Если вы укажете неверный номер кошелька, сумма может быть утеряна без возможности "
                           "возврата.‼️\n\n "
                           "👇👇👇Пожалуйста, отправьте ваш кошелек TRC20 USDT.👇👇👇",
                           reply_markup=keyboards.cansel_withdraw_requests())
    await state.set_state(MyStates.waiting_for_wallet)

    logger.info(f'user_id - {user_id} requested to withdraw money')


@dp.message_handler(state=MyStates.waiting_for_wallet)
async def process_wallet(message: types.Message, state: FSMContext):
    wallet = message.text.strip()
    user_id = message.from_user.id
    balance = user_data.get_user_balance_bonus(user_id)

    if len(wallet) == 34 and wallet.startswith('T'):
        # Кошелек прошел проверку

        add_withdrawal_request(user_id, float(balance), wallet)

        await bot.send_message(const.admin, f"Заявка на вывод от пользователя {user_id} на сумму {balance}$\n"
                                            f"Отправьте средства решите заявку тут {const.link_stat}withdraw ",
                               parse_mode="HTML")
        await message.reply("Спасибо! Ваш кошелек принят. Мы обработаем ваш запрос на вывод средств в течении 3-5 "
                            "рабочих дней.")
        await state.finish()
        logger.info(f'user_id - {message.from_user.id} provided valid wallet: {wallet}')
    else:
        # Кошелек не прошел проверку
        await message.reply("Ошибка! Кошелек должен начинаться с буквы 'T' и содержать ровно 34 символа.\n"
                            "Пожалуйста, проверьте и отправьте корректный кошелек TRC20 USDT.",
                            reply_markup=keyboards.cansel_withdraw_requests())
        logger.warning(f'user_id - {message.from_user.id} provided invalid wallet: {wallet}')


# Добавьте этот хэндлер, чтобы пользователь мог отменить операцию
@dp.callback_query_handler(text="cancel", state=MyStates.waiting_for_wallet)
async def cancel_wallet_input(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    await bot.send_message(user_id, "Операция отменена. Если вы хотите вывести средства, начните процесс заново.")
    await state.finish()

    logger.info(f'user_id - {user_id} cancelled wallet input')


@dp.callback_query_handler(text="withdraw_cancel", state="*")
async def select_go_back_(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    user_data.delete_withdraw_request(user_id)
    await bot.send_message(user_id,
                           "Заявка на вывод удалена")


@dp.callback_query_handler(lambda c: c.data == "gift_subscription", state='*')
async def gift_subscription(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.message.chat.id
    logger.info(f"BUTTON:gift_subscription user - {user_id}")

    user_data_state = await state.get_data()

    period = int(user_data_state['days'])
    amount = int(user_data_state['price'])
    promo, promo_id = generate_promo_code(period)

    price = int(user_data_state['price'])  # получаем цену, используя строковый ключ
    logger.info(f' price {price}')
    days = user_data_state['days']  # получаем дни, используя целочисленный ключ
    pay_id = balance.create_pay_id(user_id, float(str(price) + '.00'), promo_id[0])
    logger.info(price * 100)
    logger.info('--------------')
    logger.info(pay_id)
    await state.update_data(pay_id=pay_id)

    payment_url = create_pay_links.create_payment_link(
        amount=price * 10000,  # Сумма в копейках
        order_id=str(pay_id),
        description=f"Оплата заказа {pay_id} для пользователя {user_id} на сумму {price}"
    )

    await bot.send_message(chat_id=user_id,
                           text="Выберите способ оплаты",
                           parse_mode="HTML",
                           # Оплата картой
                           # Оплата USTD
                           reply_markup=keyboards.select_card_or_usdt(payment_url))

    time.sleep(10)

    await bot.send_message(chat_id=user_id,
                           text="Нажмите, для проверки платежа",
                           reply_markup=keyboards.check_status_payment())

    try:
        if callback_query.message.message_id:
            await bot.delete_message(chat_id=callback_query.message.chat.id,
                                     message_id=callback_query.message.message_id)
    except aiogram.utils.exceptions.MessageCantBeDeleted:
        logger.error("Не удалось удалить сообщение")
