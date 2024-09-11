# -*- coding: utf-8 -*-
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
import user_data
from aiogram import types
# from keyboards.admin_buutons import *
from keyboards import *
from config import dp, bot
from admin_butons import *
from states import GetuserInfo


@dp.message_handler(commands=['send_all'], state="*")
async def show_rassilka(message: types.Message):
    await message.answer('Введите текст поста:', reply_markup=ReplyKeyboardRemove())
    await GetuserInfo.get_users.set()


@dp.message_handler(state=GetuserInfo.get_users)
async def select_users_(message: types.Message, state: FSMContext):
    textpost = message.text
    await state.update_data(textpost=textpost)
    await GetuserInfo.select_users.set()
    await message.answer('Кому делаем рассылку?', reply_markup=select_users)


@dp.message_handler(state=GetuserInfo.select_users, text=['Всем', 'С подпиской', 'Без подписки'])
async def get_users_for_send(message: types.Message, state: FSMContext):
    selected_option = message.text
    print(selected_option, ' selected_option')
    await message.answer(f'Вы выбрали {selected_option}, нажмите Далее', reply_markup=dalee)

    await state.update_data(selected_option=selected_option)
    await GetuserInfo.text.set()


@dp.message_handler(state=GetuserInfo.text, text='Далее')
async def get_posttext(message: types.Message, state: FSMContext):
    await message.answer('Выберите то что вам нужно :', reply_markup=adminpanelmenu)
    await GetuserInfo.next_stage.set()


@dp.message_handler(state=GetuserInfo.next_stage, text='С фото 🏞')
async def get_photo(message: types.Message, state: FSMContext):
    await message.answer('Отправьте фото 🏞 :')
    await GetuserInfo.get_img.set()


@dp.message_handler(state=GetuserInfo.next_stage, text='С видео 🎥')
async def get_video(message: types.Message, state: FSMContext):
    await message.answer('Отправьте видео :')
    await GetuserInfo.get_video.set()


@dp.message_handler(state=GetuserInfo.get_img, content_types=types.ContentType.PHOTO)
async def get_photo_id(message: types.Message, state: FSMContext):
    fileid = message.photo[0].file_id
    await state.update_data(photoid=fileid)
    await GetuserInfo.finishpost.set()
    await message.answer('✅ Данные получены, нажмите "продолжить"', reply_markup=adminpanelcontinue)


@dp.message_handler(state=GetuserInfo.get_video, content_types=types.ContentType.VIDEO)
async def get_video_id(message: types.Message, state: FSMContext):
    if message.video:
        fileid = message.video.file_id
        await state.update_data(video_id=fileid)
        await GetuserInfo.finishpost.set()
        await message.answer('✅ Данные получены, нажмите "продолжить"', reply_markup=adminpanelcontinue)
    else:
        await message.answer('❗ Не удалось получить видео. Попробуйте еще раз.')


@dp.message_handler(state=GetuserInfo.next_stage, text='Пропустить ➡️')
@dp.message_handler(state=GetuserInfo.finishpost)
async def get_testpost(message: types.Message, state: FSMContext):
    data = await state.get_data()
    post_text = data.get('textpost')
    photoid = data.get('photoid')
    video_id = data.get('video_id')
    # keyboard = data.get('keyboard')
    user = message.from_user.id
    try:
        if photoid:
            await bot.send_photo(user, photo=photoid, caption=post_text,
                                 parse_mode='HTML', reply_markup=startposting)
        elif video_id:
            await bot.send_video(user, video=video_id, caption=post_text,
                                 parse_mode='HTML', reply_markup=startposting)

        else:
            await bot.send_message(user, disable_web_page_preview=True, text=post_text, parse_mode='HTML',
                                   reply_markup=startposting)
        await GetuserInfo.publish.set()
    except Exception as e:
        print(e)
        await bot.send_message(user,
                               text=f'Введенный текст не правильно форматирован! Убедитесь что все теги закрыты '
                                    f'правильно.\n Начните всё заново : /send_all')
        await state.finish()
        await state.reset_data()


@dp.callback_query_handler(state=GetuserInfo.publish, text='startposting')
async def sendposts(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    post_text = data.get('textpost')
    photoid = data.get('photoid')
    video_id = data.get('video_id')
    keyboard = data.get('keyboard')
    selected_users = data.get('selected_option')
    senpostcol = 0

    if selected_users == "Всем":
        user_ids = user_data.get_all_users()
    if selected_users == "С подпиской":
        user_ids = user_data.get_user_id_have_sub()
    if selected_users == "Без подписки":
        user_ids = user_data.get_user_id_have_not_sub()

    user_ids = [user_id[0] for user_id in user_ids]
    for user in user_ids:
        post_text = post_text.format_map({
        })
        try:
            if photoid:
                await bot.send_photo(user, photo=photoid, caption=post_text,
                                     parse_mode='HTML')
            elif video_id:
                await bot.send_video(user, video=video_id, caption=post_text,
                                     parse_mode='HTML')
            else:
                await bot.send_message(user, disable_web_page_preview=True, text=post_text, parse_mode='HTML',
                                       reply_markup=keyboard)
            senpostcol += 1
        except:
            pass
    await call.message.answer(f'✅ Пост успешно отправлен {senpostcol} пользователям \n', reply_markup=main_menu())
    await state.finish()
    await state.reset_data()


@dp.callback_query_handler(state=GetuserInfo.publish, text='cancelposting')
async def cancel_post(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(f'✅ Данные удалены.\n Начните всё заново : /send_all', reply_markup=main_menu())
    await state.finish()
    await state.reset_data()
