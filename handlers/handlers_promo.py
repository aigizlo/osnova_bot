import asyncio

import aiogram
from aiogram import types
from aiogram.dispatcher import FSMContext
from logger import logger
import sub
import text
from config import support, dp, bot, file_ids
import keyboards.keyboards
from states import MyStates



@dp.callback_query_handler(lambda c: c.data and c.data.startswith('apply_promo'), state=MyStates.go_to_pay)
async def select_promo_code(callback_query: types.CallbackQuery, state: FSMContext):
    telegram_id = callback_query.from_user.id
    user_data_state = await state.get_data()
    month = user_data_state.get('month')
    # удаляем предыдущее сообщение
    try:
        if callback_query.message.message_id:
            await bot.delete_message(chat_id=callback_query.message.chat.id,
                                     message_id=callback_query.message.message_id)
    except aiogram.utils.exceptions.MessageCantBeDeleted:
        logger.info("Сообщение не может быть удалено.")

    answer = f"""📚 Продукт: "ОСНОВА"
    
    Введите ваш промокод:"""

    await bot.send_message(chat_id=telegram_id, text=answer, reply_markup=keyboards.keyboards.back_to_main_menu())
    await state.set_state(MyStates.insert_promo_code)


# спрашиваем имя сервера
@dp.message_handler(state=MyStates.insert_promo_code)
async def process_key_name(message: types.Message, state: FSMContext):
    telegram_id = message.chat.id
    promo_code = message.text
    print(promo_code)
    user_data_state = await state.get_data()
    is_promo_valid, promo_period = sub.check_promo_code(promo_code)
    if is_promo_valid:
        sub_active = sub.activate_subscription(telegram_id, promo_period, promo_code)
        await message.answer(sub_active)
        await asyncio.sleep(1)
        await bot.send_message(telegram_id, text.text_buy_tarif)
        logger.info(sub_active)
        await state.finish()
        return
    await message.answer(promo_period, parse_mode='HTML', reply_markup=keyboards.keyboards.back_to_main_menu())
    await state.finish()
    logger.info(promo_period)


# @dp.message_handler(state=MyStates.state_key_name)
# async def process_key_name(message: types.Message, state: FSMContext):
#     # это класс, для быстрого получения данных
#     # сохраняем название сервра юзера в переменную
#     key_name = message.text
#     user_info = user_data.get_userid_firsname_nickname(message.from_user.id)
#     # ищем его user_id
#     try:
#         user_id = user_info[0]
#         # здесь все переменные состояния
#         user_data_state = await state.get_data()
#         amount = user_data_state["amount"]
#         # возвращаем в глав меню есл нажали НАЗАД
#         if message.text == '🔙Назад':
#             keyboard = main_menu()
#             await message.answer("Главное меню:/n" + instruction, parse_mode="HTML", reply_markup=keyboard)
#             await state.finish()
#             return
#         # если имя длинное - переспрашиваем
#         if len(key_name) > 35:
#             await message.answer(ask_server_name_2)
#             return
#         # проверяем на повторность имени у конкретного юзера
#         if check_names(user_id, key_name):
#             await message.answer(ask_server_name_3)
#             return
#         # исключаем любые другие символы кроме букв и цифр
#         if not re.match(allowed_characters_pattern, key_name):
#             await message.answer(ask_server_name_4)
#             return
#         # обновляем переменные состояния для передачи их дальше
#         await state.update_data(key_name=key_name, action="pay")
#
#         # спрашиваем способ оплаты и показываем сумму
#         answer = payment_amount_prompt(amount)
#
#         # показываем инлайн клаву для выбора способа оплаты
#         pay_keyboard = get_pay_method_keyboard()
#
#         await message.answer(answer, parse_mode='HTML', reply_markup=pay_keyboard)
#         # отлов состояния pay_from_balance
#         await state.set_state(MyStates.pay_from_balance)
#
#         logger.info(f"Указывает имя ключа, user - {user_info}, имя ключа - {key_name}")
#     except Exception as e:
#         logger.info(f"ERROR:Указывает имя ключа, user - {user_info},ошибка - {e}")
#         await message.answer(answer_error, reply_markup=main_menu())