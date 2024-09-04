from aiogram import types
from aiogram.utils.exceptions import TelegramAPIError
import text
import keyboards.keyboards
from states import MyStates
from config import bot, dp
import aiogram
from aiogram.dispatcher import FSMContext
from logger import logger
import config


@dp.callback_query_handler(lambda c: c.data.startswith("period:"), state='*')
async def select_period(callback_query: types.CallbackQuery, state: FSMContext):
    user_data_state = await state.get_data()

    try:
        month = int(callback_query.data.split(':')[1])  # извлекаем месяц
    except:
        month = user_data_state['month']

    user_id = callback_query.message.chat.id

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
                           reply_markup=keyboards.keyboards.select_pay_method())


@dp.callback_query_handler(lambda c: c.data.startswith("go_pay"), state=MyStates.go_to_pay)
async def go_to_pay(callback_query: types.CallbackQuery, state: FSMContext):
    user_data_state = await state.get_data()

    month = user_data_state['month']
    print(month, ' month')
    user_id = callback_query.message.chat.id

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
                           reply_markup=keyboards.keyboards.go_pay())


@dp.callback_query_handler(lambda c: c.data.startswith("select_pay_method"), state=MyStates.go_to_pay)
async def selected_pay_method(callback_query: types.CallbackQuery, state: FSMContext):
    user_data_state = await state.get_data()

    month = user_data_state['month']
    user_id = callback_query.message.chat.id

    price = user_data_state['price'] # получаем цену, используя строковый ключ
    days = user_data_state['days']  # получаем дни, используя целочисленный ключ

    print(user_data_state)

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
                           reply_markup=keyboards.keyboards.select_card_or_usdt())









@dp.callback_query_handler(text="go_back", state="*")
async def go_back_(callback_query: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    print(f"Current state before going back: {current_state}")
    await select_period(callback_query, state)


@dp.callback_query_handler(text="go_back_to_main", state="*")
async def go_back_to_main(callback_query: types.CallbackQuery, state: FSMContext):
    user_data_state = await state.get_data()
    month = user_data_state.get('month')
    price = user_data_state.get('price')
    days = user_data_state.get('days')
    txt_tarrif_info = text.tarrif_info(month, price, days)
    try:
        if callback_query.message.message_id:
            await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    except aiogram.utils.exceptions.MessageCantBeDeleted:
        logger.info("Сообщение не может быть удалено.")
    await bot.send_message(chat_id=callback_query.message.chat.id,
                           text=txt_tarrif_info,
                           parse_mode="HTML",
                           reply_markup=keyboards.keyboards.keyboard_period())
    # await state.set_state(MyStates.select_period)

