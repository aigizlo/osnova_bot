# from time import sleep
# from logger import logger
# import aiogram
# from aiogram.utils.exceptions import TelegramAPIError
# from telebot_ import sync_send_message
#
# from get_conn import create_connection
#
# from config import *
#
#
# @dp.callback_query_handler(lambda c: c.data == "period:", state="*")
# async def select_period(callback_query: types.CallbackQuery):
#
#     # обновляем последнее действие пользователя
#     month = int(callback_query.data.split(':')[1])  # получаем цену
#
#     # удаляем капчу
#     try:
#         if callback_query.message.message_id:
#             await bot.delete_message(chat_id=callback_query.message.chat.id,
#                                      message_id=callback_query.message.message_id)
#     except aiogram.utils.exceptions.MessageCantBeDeleted:
#         logger.info("Сообщение не может быть удалено.")
#     logger.info(f"CAPTCHA:SUCSSESS - {user_id}")
#
#     # kb_free_tariff = free_tariff()
#
#     # отправялем пиветственный текст
#     await bot.send_photo(chat_id=callback_query.message.chat.id,
#                          photo=file_ids['menu'],
#                          caption=instruction,
#                          parse_mode="HTML",
#                          reply_markup=main_menu_inline())
