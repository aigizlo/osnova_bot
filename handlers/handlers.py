from aiogram import types
from aiogram.utils.exceptions import TelegramAPIError
import text
import keyboards
from states import MyStates
from config import bot, dp
import aiogram
from aiogram.dispatcher import FSMContext
from logger import logger
import config
import const


@dp.callback_query_handler(lambda c: c.data.startswith("period:"), state='*')
async def select_period(callback_query: types.CallbackQuery, state: FSMContext):
    user_data_state = await state.get_data()
    user_id = callback_query.message.chat.id

    try:
        month = int(callback_query.data.split(':')[1])  # извлекаем месяц
    except:
        month = user_data_state['month']
    price = config.prices.get(str(month))  # получаем цену, используя строковый ключ
    days = config.get_days.get(month)  # получаем дни, используя целочисленный ключ

    txt_tarrif_info = text.tarrif_info(month, price, days)
    try:
        if callback_query.message.message_id:
            await bot.delete_message(chat_id=user_id, message_id=callback_query.message.message_id)
    except aiogram.utils.exceptions.MessageCantBeDeleted:
        logger.info("Сообщение не может быть удалено.")
    logger.info(f" - {user_id}")

    await state.set_state(MyStates.go_to_pay)
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


@dp.callback_query_handler(lambda c: c.data.startswith("go_pay"), state=MyStates.go_to_pay)
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

    # отправляем информационное сообщение
    await bot.send_message(chat_id=user_id,
                           text=txt_tarrif_info,
                           parse_mode="HTML",
                           # Перейти к оплате
                           # Назад
                           reply_markup=keyboards.go_to_pay())
    logger.info(f'user_id {user_id} - 💳 Оплатить {month} месяцев')


@dp.callback_query_handler(lambda c: c.data.startswith("select_pay_method"), state=MyStates.go_to_pay)
async def select_pay_method(callback_query: types.CallbackQuery, state: FSMContext):
    # Перейти к оплате
    user_data_state = await state.get_data()
    month = user_data_state['month']
    user_id = callback_query.message.chat.id
    price = user_data_state['price']  # получаем цену, используя строковый ключ
    days = user_data_state['days']  # получаем дни, используя целочисленный ключ
    try:
        if callback_query.message.message_id:
            await bot.delete_message(chat_id=user_id, message_id=callback_query.message.message_id)
    except aiogram.utils.exceptions.MessageCantBeDeleted:
        logger.info("Сообщение не может быть удалено.")

    # отправляем информационное сообщение
    await bot.send_message(chat_id=user_id,
                           text="Выберите способ оплаты",
                           parse_mode="HTML",
                           # Оплата картой
                           # Оплата USTD
                           reply_markup=keyboards.select_card_or_usdt())

    logger.info(f'user_id {user_id} - Перейти к оплате {month} месяцев {days} - дней {price} цена')


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
async def select_go_back_(callback_query: types.CallbackQuery, state: FSMContext):
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
    # Принимаю правила
    await bot.send_message(chat_id=user_id,
                           text="Выберите срок продления",
                           parse_mode="HTML",
                           # 1 месяц - 30 дней - 15 USD
                           # 3 месяц - 90 дней - 40 USD
                           # 12 месяц - 365 дней - 150 USD
                           reply_markup=keyboards.keyboard_period())
    logger.info(f'user_id - {user_id} Продлить подписку')