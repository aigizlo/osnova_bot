import asyncio
import const
import aiogram
from aiogram import types
from aiogram.dispatcher import FSMContext
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
    
    Введите ваш промокод:"""

    await bot.send_message(chat_id=user_id, text=answer, reply_markup=keyboards.back_to_main_menu())
    await state.set_state(MyStates.insert_promo_code)
    logger.info(f'user_id - {user_id} - 🎁 Применить промокод')


@dp.message_handler(state=MyStates.insert_promo_code)
async def insert_promo_codes(message: types.Message, state: FSMContext):
    user_id = message.chat.id
    promo_code = message.text
    is_promo_valid, promo_period = promo.check_promo_code(promo_code)
    if is_promo_valid:
        sub_active, answer = sub.activate_or_renewal_subscription(user_id, promo_period)
        if sub_active:
            promo.status_used_promo_code(user_id=user_id,
                                         promo_code=promo_code)
            if answer:
                await bot.send_message(user_id, answer)
                logger.info(f'user_id - {user_id} активировал промокод {promo_code} для продления на {promo_period} дней')
                return
        await asyncio.sleep(1)
        await bot.send_message(user_id, text.text_buy_tarif, reply_markup=keyboards.accept_button())
        member = await bot.get_chat_member(chat_id=const.channel_id, user_id=user_id)
        if member.status == 'kicked':
            await bot.unban_chat_member(chat_id=const.channel_id, user_id=user_id)
        logger.info(f'user_id - {user_id} Активировал промокод - {promo_code} для покупки на {promo_period} дней')
        logger.info(sub_active)
        await state.finish()
        return
    await message.answer(promo_period, parse_mode='HTML', reply_markup=keyboards.back_to_main_menu())
    await state.finish()
    logger.info(f'user_id - {user_id} - ввел неактивный промокод - {promo_code}')
