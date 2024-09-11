from config import dp, bot, admins
from aiogram import types
import sub
import const
import keyboards
import promo
from links import tracker

from logger import logger

import user_data


@dp.message_handler(commands=['promo'], state="*")
async def create_promo(message: types.Message):
    command_parts = message.get_args().split()
    telegram_id = message.from_user.id
    if message.from_user.id not in admins:
        await message.reply(f"Данная команда только для администраторов")
        logger.info(f"ADMIN COMMAND - создать промокод, User - {telegram_id}, , НЕТ ПРАВ ДЛЯ ДАННОЙ КОМАНДЫ")
        return

    elif len(command_parts) != 2:
        await message.reply("Неверное количество аргументов, пример - создать промокод MYPROMO 30")
        logger.info(f"ADMIN COMMAND - /balance, User - {telegram_id}, Неверное количество аргументов")
        return
    code = command_parts[0]
    period = command_parts[1]
    result, answer = promo.create_promo_code(code, int(period))
    if not result:
        await message.reply(answer)
        return
    await message.reply(answer)
    # await message.reply(answer)
    logger.info(f"ADMIN_COMMANDS /free,  , admin - {message.from_user.id}")


@dp.message_handler(commands=['promo_info'], state="*")
async def check_free_keys(message: types.Message):
    if message.from_user.id not in admins:
        await message.reply("Данная команда только для администраторов")
        return
    txt = "Команда показывает отчет по промокодам\n"

    report = promo.generate_promo_code_report()

    await message.reply(txt + str(report))
    logger.info(f"ADMIN_COMMANDS promo_info,  , admin - {message.from_user.id}")


@dp.message_handler(commands=['admin'], state="*")
async def admin_command(message: types.Message):
    telegram_id = message.from_user.id
    if message.from_user.id not in admins:
        await message.reply(f"Данная команда только для администраторов")
        logger.info(f"ADMIN COMMAND - /free, User - {telegram_id} ,НЕТ ПРАВ ДЛЯ ДАННОЙ КОМАНДЫ")
        return
    answer = f"""/get_logs - получить все логи(для прогера) \n
/all_users - количество всех пользователей\n
/promo_info - отчет по промокодам\n
/admin - ваши команды\n
/promo -создать промокод, например"/promo PROMO 30", где "PROMO"-промокод, "30"-дни\n
/user - инфо об юзере, например /user @byshakirov или по id /user 502811372 \n
/clear_promo - удаляет использованные и просроченные промокоды \n
/create_links - создать ссылку, через пробел название \n
/send_all -просмотр статистики \n
/stats -просмотр статистики \n\n
"""


    await message.reply(answer)
    return
# create_links

@dp.message_handler(commands=['count_users'], state="*")
async def all_users_command(message: types.Message):
    if message.from_user.id not in admins:
        await message.reply("Данная команда только для администраторов")
        return
    txt = "Команда показывает общее число пользователей: \n"
    answer = user_data.all_users()
    await message.reply(txt + str(answer))
    logger.info(f"ADMIN_COMMANDS /all_users,  , admin - {message.from_user.id}")


@dp.message_handler(commands=['all_users'], state="*")
async def all_users_command(message: types.Message):
    if message.from_user.id not in admins:
        await message.reply("Данная команда только для администраторов")
        return
    txt = "Команда показывает общее число пользователей: \n"
    answer = user_data.all_users()
    await message.reply(txt + str(answer))
    logger.info(f"ADMIN_COMMANDS /all_users,  , admin - {message.from_user.id}")


@dp.message_handler(commands=['user'], state="*")
async def user_info_command(message: types.Message):
    if message.from_user.id not in admins:
        await message.reply("Данная команда только для администраторов")
        return
    argument = message.get_args()
    if not argument:
        return
    if argument[0] == '@':
        user_name = argument[1::]
        user_info = user_data.get_user_info(user_name=user_name)
        await message.answer(user_info, parse_mode='HTML',
                             disable_web_page_preview=True)
        return

    user_id = argument
    user_info = user_data.get_user_info(user_id=int(user_id))
    await message.answer(user_info, parse_mode='HTML',
                         disable_web_page_preview=True)


@dp.message_handler(commands=['clear_promo'], state="*")
async def clear_promo_command(message: types.Message):
    if message.from_user.id not in admins:
        await message.reply("Данная команда только для администраторов")
        return
    result = promo.clear_used_promo()
    answer = "Использованные или просроченные промокоды удалены"
    await message.answer(answer, disable_web_page_preview=True)


@dp.message_handler(commands=['create_links'], state="*")
async def create_links(message: types.Message):
    if message.from_user.id not in admins:
        await message.reply("Данная команда только для администраторов")
        return
    name = message.get_args()
    if not name:
        await message.answer('Повтори попытку с названием через пробел', disable_web_page_preview=True)
        return
    link = tracker.generate_link(const.bot_name, name)
    await message.answer(link, disable_web_page_preview=True)

@dp.message_handler(commands=['stats'], state="*")
async def create_links(message: types.Message):
    if message.from_user.id not in admins:
        await message.reply("Данная команда только для администраторов")
        return
    await message.answer(const.link_stat, disable_web_page_preview=True)

#
#
# @dp.message_handler(commands=['balance'], state="*")
# async def balance_command(message: types.Message):
#     keyboards = main_menu_inline()
#     command_parts = message.get_args().split()  # Разбиваем аргументы на части
#     admins = get_list_admins_telegram_id()
#
#     telegram_id = message.from_user.id
#
#     if message.from_user.id not in (admins + admin_from_config):
#         await message.reply(f"Данная команда только для администраторов")
#         logger.info(f"ADMIN COMMAND - /balance, User - {telegram_id}, НЕТ ПРАВ ДЛЯ ДАННОЙ КОМАНДЫ")
#
#     elif len(command_parts) != 2:
#         await message.reply("Неверное количество аргументов, пример - /balance 142 1 или /balance 142 0")
#         logger.info(f"ADMIN COMMAND - /balance, User - {telegram_id}, Неверное количество аргументов")
#
#     else:
#         user_id = command_parts[0]
#         amount = command_parts[1]
#         try:
#             execute_query(sql_add_balance, (user_id, amount,))
#
#             await message.reply(f"Для пользователя {user_id} пополнен баланс на {amount}.", reply_markup=keyboards)
#             logger.info(
#                 f"ADMIN COMMAND - /balance, User - {telegram_id}, Для пользователя {user_id} пополнен баланс на {amount}")
#         except QueryExecutionError as e:
#             logger.error(f"Ошибка при выполнении команды /balance user {telegram_id},ошибка {e}")
#             await message.reply(
#                 f"Произошла ошибка при выполнении команды /balance. Пожалуйста, обратитесь к администратору.",
#                 reply_markup=keyboards)

#
# @dp.message_handler(commands=['admin'], state="*")
# async def add_del_admin_command(message: types.Message):
#     keyboard = main_menu_inline()
#     command_parts = message.get_args().split()  # Разбиваем аргументы на части
#
#     admins = get_list_admins_telegram_id()
#
#     telegram_id = message.from_user.id
#
#     logger.info(f"ADMIN COMMAND - /admin, ADMIN - {telegram_id} ")
#
#     if message.from_user.id not in (admins + admin_from_config):
#         await message.reply(f"Данная команда только для администраторов", reply_markup=keyboard)
#         logger.info(f"ADMIN COMMAND - /admin, User - {telegram_id}, НЕТ ПРАВ ДЛЯ ДАННОЙ КОМАНДЫ")
#
#     elif len(command_parts) != 2:
#         await message.reply("Неверное количество аргументов, пример - /admin 142 1 или /admin 142 0")
#         logger.info(f"ADMIN COMMAND - /admin, User - {telegram_id},  , Неверное количество аргументов")
#     else:
#         user_id = command_parts[0]
#         digit = command_parts[1]
#
#         action = ''
#         try:
#             execute_query(sql_add_admin, (digit, user_id,))
#             if int(digit) == 1:
#                 action = "Добавлен новый администратор"
#             elif int(digit) == 0:
#                 action = "Разжалован администратор"
#             logger.info(f"ADMIN COMMAND - /admin, ADMIN - {telegram_id},  {action} - {user_id}")
#
#             await message.reply(f"{action} - {user_id}")
#         except QueryExecutionError as e:
#             logger.error(f"Ошибка при выполнении команды /admin: {e},  ,")
#             await message.reply(f"Произошла ошибка при выполнении команды /admin,  ,")


#

#
#
# @dp.message_handler(commands=['get_logs'], state="*")
# async def check_free_keys(message: types.Message):
#     admins = get_list_admins_telegram_id()
#     telegram_id = message.from_user.id
#     if message.from_user.id not in (admins + admin_from_config):
#         await message.reply(f"Данная команда только для администраторов")
#         logger.info(f"ADMIN COMMAND - /free, User - {telegram_id} ,НЕТ ПРАВ ДЛЯ ДАННОЙ КОМАНДЫ")
#         return
#     await message.reply('Загружаем логи')
#     path_bot_logs = "/home/admin/for_bot_corparation/bot.log"
#
#     with open(path_bot_logs, 'rb') as document:
#         await bot.send_document(message.from_user.id, document)
#         logger.info(f"ADMIN_COMMANDS /get_log(bot.log),  , admin - {message.from_user.id}")
#
#
# @dp.message_handler(commands=['admin_commands'], state="*")
# async def check_free_keys(message: types.Message):
#     admins = get_list_admins_telegram_id()
#     telegram_id = message.from_user.id
#     if message.from_user.id not in (admins + admin_from_config):
#         await message.reply(f"Данная команда только для администраторов")
#         logger.info(f"ADMIN COMMAND - /free, User - {telegram_id} ,НЕТ ПРАВ ДЛЯ ДАННОЙ КОМАНДЫ")
#         return
#     answer = f"/get_logs - получить все логи\n\n" \
#              f"/user_info - информация о пользователе 1 аргумент user_id или user_name, пример - /user_info 212 или /user_info @user_name\n\n" \
#              f"/all_users - количество всех пользователей\n\n" \
#              f"/free - количество свободных ключей на сервере\n\n" \
#              f"/admin - назначит/разжаловать админа 2 аргумента (/admin 17 0) 17 - user_id, 1 - назначить 0 - разжаловать " \
#              f"/trial - Команда показывает общее число пользователей взявших ключ бесплатно\n\n" \
#              f"/get_count_users - Команда показывает общее число пользователей присоединенных в какую то дату (2024-01-25)\n\n" \
#              f"/balance - начисляем вычитаем деньги с баланса(/balance (user_id) (summa)) или вычесть (/balance (user_id) -(summa))\n\n" \
#              f"/key_for - дарим ключ пользователю, пример /key_for (user_id) (day) \n\n" \
#              f"/delete_keys - удаляет ключ, пример /delete_keys (key_id) \n\n" \
#              f"/prolong_key - продлеваем ключ пользователю, пример /prolong_key (key_id) (месяц) \n\n"
#     await message.reply(answer)
#
#
#
#
# @dp.message_handler(commands=['all_keys'], state="*")
# async def check_free_keys(message: types.Message):
#     admins = get_list_admins_telegram_id()
#
#     if message.from_user.id not in (admins + admin_from_config):
#         await message.reply("Данная команда только для администраторов")
#         return
#
#     txt = "Команда показывает общее число ключей, купленных и взятых бесплатно\n"
#
#     answer = user_data.get_count_all_keys()
#
#     await message.reply(txt + str(answer))
#     logger.info(f"ADMIN_COMMANDS /all_keys,  , admin - {message.from_user.id}")
#
#
# @dp.message_handler(commands=['get_count_users'], state="*")
# async def check_free_keys(message: types.Message):
#     admins = get_list_admins_telegram_id()
#
#     if message.from_user.id not in (admins + admin_from_config):
#         await message.reply("Данная команда только для администраторов")
#         return
#     command_parts = message.get_args().split()
#
#     if len(command_parts) != 1:
#         await message.reply("Неверное количество аргументов, пример команды /get_count_users 2024-01-25")
#
#         return
#
#     answer = user_data.get_count_user_with_date(command_parts[0])
#
#     logger.info(f'{len(command_parts)}, {command_parts}')
#
#     txt = f"Команда показывает общее число пользователей присоединенных в {command_parts[0]}\n"
#     #
#     #
#     await message.reply(txt + str(answer))
#     logger.info(f"ADMIN_COMMANDS /all_keys,  , admin - {message.from_user.id}")
#
#
# @dp.message_handler(commands=['key_for'], state="*")
# async def present_key(message: types.Message):
#     admins = get_list_admins_telegram_id()
#
#     if message.from_user.id not in (admins + admin_from_config):
#         await message.reply("Данная команда только для администраторов")
#         return
#
#     command_parts = message.get_args().split()  # Разбиваем аргументы на части
#
#     admin_info = user_data.get_user_data(message.from_user.id)
#
#     admin_user_id, admin_first_name = admin_info.get("user_id"), admin_info.get("first_name")
#
#     try:
#
#         logger.info(f"ADMIN COMMAND - /admin, ADMIN - {admin_user_id} ")
#
#         if len(command_parts) != 2:
#             await message.reply(
#                 """Неверное количество аргументов, пример - /key_for 142 31 (142 user_id, 31 количество дней)""")
#             logger.info(f"ADMIN COMMAND - /admin, ADMIN - {admin_user_id}, Неверное количество аргументов")
#             return
#
#         user_id = int(command_parts[0])
#         day = int(command_parts[1])
#
#         user_info = user_data.get_user_data2(user_id)
#
#         if not user_info:
#             await message.reply(f'Пользователя {user_id} не существует')
#             return
#
#         if day > 365:
#             await message.reply("Значение day не более 365")
#             return
#
#         key_id, key_value, server_id = add_keys(user_id, day)
#
#         answer = text_free_tariff(server_id)
#
#         key_value2 = f'<code>{key_value}</code>'
#
#         user_telegram_id = user_info.get("telegram_id")
#
#         await bot.send_message(chat_id=user_telegram_id,
#                                text=answer,
#                                parse_mode="HTML",
#                                disable_web_page_preview=True)
#         await bot.send_message(chat_id=user_telegram_id,
#                                text=key_value2, reply_markup=in_main_menu(),
#                                parse_mode="HTML")
#
#         await bot.send_message(chat_id=admin_info.get("telegram_id"),
#                                text=f"""Пользователю user_id - {user_id}, username - {user_info.get("username")}, подарен ключ на {day} дней""", )
#
#         logger.info(f"""ADMIN_COMMAND:Подарен ключ {key_id} на срок - {day} пользователю {user_id} , администратором
#         user_id - {admin_info.get("user_id")}""")
#     except Exception as e:
#         logger.error(
#             f'''ERROR - ADMIN_COMMAND - Ошибка при дарении ключа пользователю {user_id}, admin  - {admin_user_id}, ошибка - {e}''')
#
#
# @dp.message_handler(commands=['prolong_key'], state="*")
# async def prolong_key(message: types.Message):
#     admins = get_list_admins_telegram_id()
#
#     if message.from_user.id not in (admins + admin_from_config):
#         await message.reply("Данная команда только для администраторов")
#         return
#
#     command_parts = message.get_args().split()  # Разбиваем аргументы на части
#
#     admin_info = user_data.get_user_data(message.from_user.id)
#
#     admin_user_id, admin_telegram_id = admin_info.get("user_id"), admin_info.get("telegram_id")
#
#     try:
#
#         logger.info(f"ADMIN COMMAND - /prolong_key, ADMIN - {admin_user_id} ")
#
#         if len(command_parts) != 2:
#             await message.reply(
#                 """Неверное количество аргументов, пример - /key_for 142 31 (142 user_id, 31 количество дней)""")
#             logger.info(f"ADMIN COMMAND - /prolong_key, ADMIN - {admin_user_id}, Неверное количество аргументов")
#             return
#
#         key_id = int(command_parts[0])
#
#         month = int(command_parts[1])
#
#         user_id = user_data.whose_key(key_id)
#
#         if not user_id:
#             await message.reply(f'Ключа - {key_id} не существует')
#             return
#
#         if month > 12:
#             await message.reply("Значение month не более 12")
#             return
#         user_info = user_data.get_user_data2(user_id)
#
#         telegram_id = user_info.get("telegram_id")
#
#         key_id = renewal_keys_admin_command(int(key_id), month)
#         if key_id:
#             answer = f"✅ Вы успешно продлили \"<b>Ключ № {key_id}</b>\" "
#
#             sync_send_photo(telegram_id, file_ids['renewal_ok'], answer, "HTML", main_menu_telebot())
#             await bot.send_message(admin_telegram_id,
#                                    f"""Пользователю {user_id} успешно продлен ключ {key_id} на {month} месяцев""")
#
#     except Exception as e:
#         logger.error(f"""ERROR - ADMIN COMMAND - /prolong_key, ошибка - {e}""")
#
#
# @dp.message_handler(commands=['delete_keys'], state="*")
# async def delete_keys(message: types.Message):
#     admins = get_list_admins_telegram_id()
#
#     if message.from_user.id not in (admins + admin_from_config):
#         await message.reply("Данная команда только для администраторов")
#         return
#
#     command_parts = message.get_args()  # Разбиваем аргументы на части
#
#     admin_info = user_data.get_user_data(message.from_user.id)
#
#     admin_user_id, admin_telegram_id = admin_info.get("user_id"), admin_info.get("telegram_id")
#
#     logger.info(f"ADMIN COMMAND - /delete_keys, ADMIN - {admin_user_id} ")
#
#     key_id = int(command_parts)
#
#     if not delete_key(key_id):
#         await bot.send_message(admin_telegram_id, f"Ключ {key_id} не был удален из за проблем на сервере")
#         logger.info(
#             f"ADMIN COMMAND - /delete_keys, ключ {key_id} не был удален из за проблем на сервере, ADMIN - {admin_user_id} ")
#
#     await bot.send_message(admin_telegram_id, f"Ключ {key_id} успешно удален")
#     logger.info(f"ADMIN COMMAND - /delete_keys, ключ {key_id} успешно удален , ADMIN - {admin_user_id} ")

#
# @dp.message_handler(commands=['new_location'], state="*")
# async def delete_keys(message: types.Message):
#     admins = get_list_admins_telegram_id()
#
#     if message.from_user.id not in (admins + admin_from_config):
#         await message.reply("Данная команда только для администраторов")
#         return
#
#     command_parts = message.get_args()  # Разбиваем аргументы на части
#
#     admin_info = user_data.get_user_data(message.from_user.id)
#
#     admin_user_id, admin_telegram_id = admin_info.get("user_id"), admin_info.get("telegram_id")
#
#     logger.info(f"ADMIN COMMAND - /delete_keys, ADMIN - {admin_user_id} ")
#
#     key_id = int(command_parts)
#
#     if not delete_key(key_id):
#         await bot.send_message(admin_telegram_id, f"Ключ {key_id} не был удален из за проблем на сервере")
#         logger.info(f"ADMIN COMMAND - /delete_keys, ключ {key_id} не был удален из за проблем на сервере, ADMIN - {admin_user_id} ")
#
#     await bot.send_message(admin_telegram_id, f"Ключ {key_id} успешно удален")
#     logger.info(f"ADMIN COMMAND - /delete_keys, ключ {key_id} успешно удален , ADMIN - {admin_user_id} ")
