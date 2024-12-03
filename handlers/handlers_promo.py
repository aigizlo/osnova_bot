import asyncio
import const
import aiogram
from aiogram import types
from aiogram.dispatcher import FSMContext

import user_data
from logger import logger
import sub
import text
import promo
from config import support, dp, bot
import keyboards
from states import MyStates


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('apply_promo'), state="*")
async def select_promo_code(callback_query: types.CallbackQuery, state: FSMContext):
    # 🎁 Применить промокод
    user_id = callback_query.from_user.id
    try:
        if callback_query.message.message_id:
            await bot.delete_message(chat_id=callback_query.message.chat.id,
                                     message_id=callback_query.message.message_id)
    except aiogram.utils.exceptions.MessageCantBeDeleted:
        logger.info("Сообщение не может быть удалено.")

    answer = f"""📚 Продукт: "ОСНОВА"
    
<u>В ответное сообщение введите ваш промокод</u>:"""

    await bot.send_message(chat_id=user_id, text=answer, reply_markup=keyboards.back_to_main_menu(), parse_mode="HTML")
    await state.set_state(MyStates.insert_promo_code)
    logger.info(f'user_id - {user_id} - Применить промокод')


@dp.message_handler(state=MyStates.insert_promo_code)
async def insert_promo_codes(message: types.Message, state: FSMContext):
    user_id = message.chat.id
    promo_code = message.text
    user_name = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    is_promo_valid, promo_period = promo.check_promo_code(promo_code)
    referer_user_id = user_data.get_referrer_user_id(user_id)
    ref_user_name = None
    if referer_user_id:
        ref_user_name = user_data.get_referrer_username(referer_user_id)
    if is_promo_valid:
        sub_active, answer = sub.activate_or_renewal_subscription(user_id, promo_period)
        user_balance = 0
        try:
            user_balance = user_data.get_user_balance_bonus(user_id)
        except:
            user_balance = 0
        if sub_active:

            try:
                for admin in const.admins_notify:
                    # Обрабатываем referer_user_id
                    ref_id = "НЕТ" if referer_user_id is None else referer_user_id
                    # Обрабатываем ref_username
                    ref_name = "НЕТ" if ref_user_name is None else f"@{ref_user_name}"
                    await bot.send_message(chat_id=admin,
                                           text=f"🟡 {promo_period//30} мес\n"
                                                f"💸 {promo_code}\n"
                                                f"⏳ {promo_period} дней, \n"
                                                f"📱 {user_id}, \n"
                                                f"👥 UserName: @{user_name}, \n"
                                                f"👤 First_Name: {first_name}, \n"
                                                f"👤 Last_Name: {last_name}, \n"
                                                f"📲 Ref: {ref_id}, {ref_name}\n"
                                                f"💰 Balance: {user_balance}")

            except Exception as e:
                logger.error('не удалось отправить инфу админу')
            promo.status_used_promo_code(user_id=user_id,
                                         promo_code=promo_code)
            if answer:
                await bot.send_message(user_id, answer)
                logger.info(f'user_id - {user_id} активировал промокод {promo_code} для продления на {promo_period} дней')
                return
        await asyncio.sleep(1)
        member_channel = await bot.get_chat_member(chat_id=const.channel_id, user_id=user_id)
        member_chat = await bot.get_chat_member(chat_id=const.chat_id, user_id=user_id)

        if member_channel.status == 'kicked':
            await bot.unban_chat_member(chat_id=const.channel_id, user_id=user_id)
            logger.info(f"Пользователь  {user_id} разбанен в канане")

        if member_chat.status == 'kicked':
            await bot.unban_chat_member(chat_id=const.chat_id, user_id=user_id)
            logger.info(f"Пользователь  {user_id} разбанен в чате")
        logger.info(f'user_id - {user_id} Активировал промокод - {promo_code} для покупки на {promo_period} дней')
        await bot.send_message(user_id, text.text_buy_tarif, reply_markup=keyboards.accept_button(), parse_mode="HTML")
        logger.info(sub_active)
        await state.finish()
        return
    await message.answer(promo_period, parse_mode='HTML', reply_markup=keyboards.back_to_main_menu())
    await state.finish()
    logger.info(f'user_id - {user_id} - ввел неактивный промокод - {promo_code}')
