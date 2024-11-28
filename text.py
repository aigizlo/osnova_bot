# -*- coding: utf-8 -*-
import user_data
from config import url_polz_solah, url_politic_conf

instruction = """
<b><u> 💎 OSNOVA | Private Club </u></b> — 
закрытое сообщество для тех, кто хочет стать автором своей жизни, перестать быть жертвой обстоятельств, обрести контроль над своими успехами и добиться настоящих изменений.

<b><u>🔰 Что вас ждёт в клубе: </u></b>
<i> • Поддержка наставников</i>  — регулярные прямые эфиры и психологические разборы.
<i> • Индивидуальный план и отчёты </i> — шаги к лучшей версии себя.  
<i> • Сообщество единомышленников </i> — для обмена опытом и совместного роста.
<i> • Курсы и вебинары </i> — дисциплина, мотивация, доход, ответственность и отношения.  
<i> • Полезные знакомства</i> — найдите партнёров и поддержку.  
<i> • Практические задания и челенджи</i> — укрепляйте навыки каждую неделю и многое другое.

🎯 Вступайте в <b><u> 💎 OSNOVA | Private Club </u></b> и уверенно идите к своим целям не в одиночку!
"""

product = """
📚 Продукт: "ОСНОВА"
🗓 Тарифные планы:
"""


def ref_send_if_reg(first_name, last_name, user_name):
    txt = f"""
    👥 🌎 Поздравляем с верно принятым решением!

У вас новый партнер:
"""
    if first_name is not None:
        txt += f"{first_name} "
    if last_name is not None:
        txt += f"{last_name} "
    if user_name is not None:
        txt += f"@{user_name}\n"
    return txt


def ref_send_if_buy(ref_user_id, first_name, last_name, user_name, mounth, bot_name):
    ref_user_id = int(ref_user_id)
    balance = user_data.get_user_balance_bonus(ref_user_id)
    count = user_data.count_referrals(ref_user_id)

    txt = f"""
<strong>👥 🌎 Не словом, а делом!
Вы сделали мир вокруг себя лучше.</strong>

Ваш партнер """

    if first_name is not None:
        txt += f"{first_name} "
    if last_name is not None:
        txt += f"{last_name} "
    if user_name is not None:
        txt += f"@{user_name} "

    txt += f"купил подписку на {mounth} месяцев.\n\n"

    txt += f"""
<strong>💵 Ваша статистика:</strong>

- 1 Уровень 33,3%: активна
— Активных партнеров: {count}
— Партнерский баланс: {balance}$

<strong>✅ Ваша партнерская ссылка: </strong>

<code>https://t.me/{bot_name}?start={ref_user_id}</code>\n\n"""
    return txt


text_buy_tarif = '''
😇 Добро пожаловать в клуб
&quot;𝐎𝐒𝐍𝐎𝐕𝐀 | 𝐏𝐫𝐢𝐯𝐚𝐭𝐞 𝐂𝐥𝐮𝐛&quot;
 
Прочитай внимательно и жми кнопку &quot;ПРИНИМАЮ ПРАВИЛА&quot;, чтобы получить доступ в клуб.


<strong>✅ ФУНДАМЕНТАЛИСТАМ РАЗРЕШЕНО:</strong>

- Использовать все материалы клуба для достижения своих целей;
- Проявляться в чате и делиться позитивной энергией;
- Делиться своими успехами и поражениями;
- Спрашивать советы и помогать друг другу если попросят;
- Задавать вопросы.



❌ <strong>Обратная сторона клуба, что ЗАПРЕЩЕНО:

</strong>
- Рассылка сообщений участникам в ЛС;
- Грубое и неуважительное общение, оскорбления
- Копирование и распростратение материалов вне клуба;
- Создание сторонних чатов с участниками клуба;
- Вовлечение в собственные и чужие проекты;
- Ссылки на сторонние проекты и реферальные ссылки;
- Обсуждение чужих продуктов и других клубов.

Если вы увидели нарушение правил, сделайте скриншот и пришлите его в поддержку.

(Любой может быть удален из канала за нарушения правил или неадекватное поведение без возврата оплаты за подписку)

Смело жми 
<strong>&quot;ПРИНИМАЮ ПРАВИЛА&quot;</strong>'''


def ref_link(user_id, bot_name, count, balance):
    txt_referal = f'''
<strong>👥 Партнерская программа</strong>


<u>🔰 Условия:</u>

1. За каждого подписчика вы получаете 33,3% от ежемесячной стоимости его подписки на продукт (в будущем их будет много).

На данный момент 33,3% это:

<strong>- от 1 мес | 30 дней = 5$ 
- от 3 мес | 90 дней = 13,5$
- от 12 мес | 365 дней = 50$</strong>

2. Бонус за развитие закрытого клуба &quot;ОСНОВА&quot; в размере 33,3% начисляются вам каждый месяц до тех пор, пока вы и привлеченный вами пользователь являетесь активными подписчикоми клуба
&quot;𝐎𝐒𝐍𝐎𝐕𝐀 | 𝐏𝐫𝐢𝐯𝐚𝐭𝐞 𝐂𝐥𝐮𝐛&quot;;

3. Минимальный порог вывода - <strong>$50</strong>;

4. Организаторы оставляет за собой право на прекращение партнерской программы и/или изменение условий в любой момент;

5. Партнерская ссылка может быть размещена под вашим контентом, который создается или распространяется вами.

<u>⛔️ <strong>Что запрещено:</strong></u>

1. Размещать партнерскую ссылку в комментариях в любой из соц сетей Шакирова Евгения и Яковенко Станислава (комментарии в Telegram, Instagram, YouTube и тд);

2. Любые мошеннические действия которые навредят закрытому клубу 
&quot;𝐎𝐒𝐍𝐎𝐕𝐀 | 𝐏𝐫𝐢𝐯𝐚𝐭𝐞 𝐂𝐥𝐮𝐛&quot;

3. Переманивать подписчиков клуба, чтобы они заново зашли в клуб, но уже по вашей партнерской ссылке.

<strong><u>💵 Ваша статистика:</u></strong>

- 1 Уровень 33,3%: активна
— Активных партнеров: {count}
— Партнерский баланс: {balance}

<strong>✅ Ваша партнерская ссылка: </strong>

<code>https://t.me/{bot_name}?start={user_id}</code>\n\n
    '''
    return txt_referal


# def not_ref_link(count, balance):
#     txt_referal = f'''
# <strong>👥 Партнерская программа</strong>
#
#
# <u>🔰 Условия:</u>
#
# 1. За каждого подписчика вы получаете 33,3% от ежемесячной стоимости его подписки на продукт (в будущем их будет много).
#
# На данный момент 33,3% это:
#
# <strong>- от 1 мес | 30 дней = 5$
# - от 3 мес | 90 дней = 13,5$
# - от 12 мес | 365 дней = 50$</strong>
#
# 2. Бонус за развитие закрытого клуба &quot;ОСНОВА&quot; в размере 33,3% начисляются вам каждый месяц до тех пор, пока вы и привлеченный вами пользователь являетесь активными подписчикоми клуба
# &quot;𝐎𝐒𝐍𝐎𝐕𝐀 | 𝐏𝐫𝐢𝐯𝐚𝐭𝐞 𝐂𝐥𝐮𝐛&quot;;
#
# 3. Минимальный порог вывода - <strong>$50</strong>;
#
# 4. Организаторы оставляет за собой право на прекращение партнерской программы и/или изменение условий в любой момент;
#
# 5. Партнерская ссылка может быть размещена под вашим контентом, который создается или распространяется вами.
#
# <u>⛔️ <strong>Что запрещено:</strong></u>
#
# 1. Размещать партнерскую ссылку в комментариях в любой из соц сетей Шакирова Евгения и Яковенко Станислава (комментарии в Telegram, Instagram, YouTube и тд);
#
# 2. Любые мошеннические действия которые навредят закрытому клубу
# &quot;𝐎𝐒𝐍𝐎𝐕𝐀 | 𝐏𝐫𝐢𝐯𝐚𝐭𝐞 𝐂𝐥𝐮𝐛&quot;
#
# 3. Переманивать подписчиков клуба, чтобы они заново зашли в клуб, но уже по вашей партнерской ссылке.
#
# <strong><u>💵 Ваша статистика:</u></strong>
#
# - 1 Уровень 33,3%: активна
# — Активных партнеров: {count}
# — Партнерский баланс: {balance}
#
# <strong>✅ Ваша партнерская ссылка: </strong>
#
# <code>https://t.me/{bot_name}?start={user_id}</code>\n\n
#     '''
#     return txt_referal


def tarrif_info(month, price, days):
    tarrif_info = f'''
    📚 Продукт: 
&quot;𝐎𝐒𝐍𝐎𝐕𝐀 | 𝐏𝐫𝐢𝐯𝐚𝐭𝐞 𝐂𝐥𝐮𝐛&quot;

🗓 Тарифный план {month} месяц

- Цена: {price} USD
- Период {days} дней'''
    return tarrif_info


def tarrif_info_2(month, price, days):
    txt = f'''
    📚 Продукт: "ОСНОВА"

    🗓 Тарифный план: {month} месяц

    — Сумма к оплате: {price} USD
    — Период: {days} дней
    — Тип платежа: Автоплатеж с интервалом в {days} дней

    После оплаты будет предоставлен доступ:

    — Канал
    &quot;𝐎𝐒𝐍𝐎𝐕𝐀 | 𝐏𝐫𝐢𝐯𝐚𝐭𝐞 𝐂𝐥𝐮𝐛&quot;
    — Чат 
    &quot;<strong>ФУНДАМЕНТАЛИСТ</strong>&quot;

    🚨 Оплачивая подписку, Вы принимаете условия <a href="{url_polz_solah}">Пользовательского соглашения</a> и <a href="{url_politic_conf}">Политики конфиденциальности</a>

    '''
    return txt


def my_tarif_info(date=None):
    if date:
        txt = f"""
замен
📚 Продукт: 
<strong>&quot;ОСНОВА&quot;</strong>

<strong>🗓 Тарифный план:</strong>
— ваша подписка активна до {date}


🚨 Оплачивая подписку, Вы принимаете условия <a href="{url_polz_solah}">Пользовательского соглашения</a> и <a href="{url_politic_conf}">Политики конфиденциальности</a>
"""
        return txt
    txt = f"""
📚 Продукт:
<strong>&quot;ОСНОВА&quot;</strong>


<strong>🗓 Тарифный план:</strong>
— У вас отсутствует активная подписка!


— Сумма к оплате: 15 USD
— Период: 30 дней
— Тип платежа: Автоплатеж с интервалом в 30 дней

После оплаты будет предоставлен доступ:

— Канал
&quot;𝐎𝐒𝐍𝐎𝐕𝐀 | 𝐏𝐫𝐢𝐯𝐚𝐭𝐞 𝐂𝐥𝐮𝐛&quot;

— Чат <strong>«ФУНДАМЕНТАЛИСТЫ»</strong>

🚨 Оплачивая подписку, Вы принимаете условия <a href="{url_polz_solah}">Пользовательского соглашения</a> и <a href="{url_politic_conf}">Политики конфиденциальности</a>"""

    return txt


text_expired_sub_1month = """
<b>😇 Привет, есть новости! </b>
📚 Твоя подписка на продукт <b>"ОСНОВА"</b> закончится <b>через 2 дня.</b>

Так как платеж был криптовалютой и здесь нет функции авто  продления, то необходимо сделать это вручную.

<b>Действуй по кнопке ниже 👇</b>


<b>😉 Пи. Эс.</b>
Этот месяц был очень насыщенным! Ты же заходил(а) в чат?!😁
Мы надеемся, что ты вырвался (-лась) из болота прокрастинации и тебе удалось пройти "ВКЛЮЧЕНИЕ", а это значит, что ты и твоя жизнь уже меняются в лучшую сторону! 


🏆 Успей продлить подписку и закрепе результат! 
Дальше будет еще больше рабочих методологий и лайфхаков, как стать лучшей версией себя! 

🎯 Наша миссия - это построить сообщество из как можно больше ответственных, взрослых и осознанных людей вокруг нас! 
Все только начинается🔥

🚨 Чтобы оставаться в энергетическом потоке и не потерять доступ к клубу со всем материалам, жми кнопку ниже — там будут все инструкции, как продлить подписку👇
"""

text_expired_sub_3month = """
<b>😇 Привет, есть новости! </b>
📚 Твоя подписка на продукт <b>"ОСНОВА" </b>закончится <b>через 2 дня.</b>

Так как платеж был криптовалютой и здесь нет функции авто  продления, то необходимо сделать это вручную.

<b>Действуй по кнопке ниже 👇</b>


😉 Мы надеемся, что твои 3 месяца были самыми эффективными.

🏆 Успей продлить подписку и достягай новые вершины! 
Дальше будет еще больше рабочих методологий и лайфхаков, как стать лучшей версией себя! 

🎯 Напоминаем, что наша миссия - это построить сообщество из как можно больше ответственных, взрослых и осознанных людей вокруг нас! И ты уже часть этого сообщества! 

🚨 Чтобы оставаться в энергетическом топоке и делать лучше мир вокруг себя, жми кнопку ниже — там будут все инструкции, как продлить подписку👇
"""

text_expired_sub_12month = """
<b>😇 Привет, вот и пролетел год! Поздравляем 🙌 </b>
📚 Твоя подписка на продукт <b>"ОСНОВА"</b> закончится через <b>2 дня.</b>

🎯 Наша миссия - это построить сообщество из как можно больше ответственных, взрослых и осознанных людей вокруг нас! 
И судя по тому, что ты с нами уже год, то у нас это получается! 

😎 Продливаем?!
Мы думаем, что да!

🚨 Чтобы оставаться в энергетическом топоке и не потерять доступ к клубу со всем материалам, жми кнопку ниже — там будут все инструкции, как продлить подписку👇
"""

text_3_days_notify = """Как сказал Бодо Шефер:
<b>"Если Вы решили что-то сделать, но не начали это делать в течение 72 часов — в 85% случаев Вы не сделаете это никогда!"</b> 

Так давайте не будем следовать этой статистике, а сделаем выбор и купим себе подписку на лучшую жизнь.
"""

text_6_days_notify = """
<b>"Начал(а) думать — реши, 
решил(а) — действуй".</b>

<i>Прошло уже 6 дней, а Вы все еще думаете какую подписку оформить!?

Все очень просто!
Посчитайте до 5 и берите любую! 

"Основа" — это самый быстрый путь к лучшей версии себя.</i>

<b>👇🏼Выбирайте тарифный план и присоединяйтесь!
До встречи с вашей новой, сильной версией себя!</b>
"""

text_9_days_notify = """
<b>🤨 Ага, уже пролетело 9 дней! 
А Вы все откладываете на потом сделать свой выбор!</b>

<i>В этом и заключается большая проблема современников - прокрастинации и нерешительность!   
Выбирайте тариф и за первые 7 дне Вы поймете как избавиться от это проблемы! 

Многие были на Вашем месте! 
Сегодня мы знаем как помочь и поддержать Вас! 
Вы не один(на) такой(ая)! 


"Основа" — это самый быстрый путь к лучшей версии себя.</i>

<b>👇🏼Выбирайте тарифный план и присоединяйтесь!
До встречи с вашей новой, сильной версией себя!</b>
"""

txt_check_status = """Нажмите, для проверки платежа\n
Внимание!\n
Если вы оплачивали USDT, то зачисление может длиться от 1 до 10 минут\n
Время ожидание зависит от нагрузки сети"""


def txt_create_promo1(code, admin_id):
    txt = f'''Переходи по ссылке 🔗 \n\n
https://t.me/OSNOVA_club_bot?start={admin_id}\n\n
🎁 И получай месячную подписку в подарок по промокоду в 
<b>"𝐎𝐒𝐍𝐎𝐕𝐀 | 𝐏𝐫𝐢𝐯𝐚𝐭𝐞 𝐂𝐥𝐮𝐛"</b>\n

Твой промокод: 👉🏻 <code>{code}</code>
(тыкни на него и он скопируется)\n

Он активен всего 72 часа. 
Не тяни! <a href="https://t.me/osnova_feedbackk">Отзывы!</a>
🤝 <b>Добро пожаловать в клуб!</b>
'''
    return txt


def txt_create_promo3(code, admin_id):
    txt = f'''Переходи по ссылке 🔗 \n\n
https://t.me/OSNOVA_club_bot?start={admin_id}\n\n
🎁 И получай трехмесячную подписку в подарок по промокоду в 
<b>"𝐎𝐒𝐍𝐎𝐕𝐀 | 𝐏𝐫𝐢𝐯𝐚𝐭𝐞 𝐂𝐥𝐮𝐛"</b>\n

Твой промокод: 👉🏻 <code>{code}</code>
(тыкни на него и он скопируется)\n

Он активен всего 72 часа. 
Не тяни! <a href="https://t.me/osnova_feedbackk">Отзывы!</a>
🤝 <b>Добро пожаловать в клуб!</b>
'''
    return txt


def txt_create_promo12(code, admin_id):
    txt = f'''Переходи по ссылке 🔗 \n\n
https://t.me/OSNOVA_club_bot?start={admin_id}\n\n
🎁 И получай годовую подписку в подарок по промокоду в 
<b>"𝐎𝐒𝐍𝐎𝐕𝐀 | 𝐏𝐫𝐢𝐯𝐚𝐭𝐞 𝐂𝐥𝐮𝐛"</b>\n

Твой промокод: 👉🏻 <code>{code}</code>
(тыкни на него и он скопируется)\n

Он активен всего 72 часа. 
Не тяни! <a href="https://t.me/osnova_feedbackk">Отзывы!</a>
🤝 <b>Добро пожаловать в клуб!</b>
'''
    return txt


def txt_if_not_rules(sub_date):
    if_not_rules = f"""
    📚 Продукт: 
<strong>&quot;ОСНОВА&quot;</strong>

<strong>🗓 Тарифный план:</strong>
— ваша подписка активна до {sub_date}

⚠️ Вы не подписались на канал и не вступили в закрытый чат клуба!
Исправляйтесь по кнопке ниже!

<b>🚨 Оплачивая или продливая подписку, Вы принимаете условия Пользовательского соглашения и Политики конфиденциальности.</b>"""
    return if_not_rules


def txt_gift_promo(code, user_id, number, days):
    txt = f'''🎁 Подарочный промокод {number}/1000👇: \n\n
<code>{code}</code>

👆(тыкни на него и он скопируется) \n
в закрытый клуб <b>"𝐎𝐒𝐍𝐎𝐕𝐀 | 𝐏𝐫𝐢𝐯𝐚𝐭𝐞 𝐂𝐥𝐮𝐛"</b> на {days} дней.\n
<b>💥 Внимание, он активен 72 часа.</b>
💡 Перешлите данное сообщение новому резиденту клуба.
Он получит доступ ссылке: 
https://t.me/OSNOVA_club_bot?start={user_id}\n\n
<b>😇  Добро пожаловать в клуб!.</b>
🤝 Отзывы о клубе: @osnova_feedbackk
'''
    return txt


def text_if_buy_promo(promo_code, bot_name, ref_user_id, month):
    txt = f"""
<b>👥 🌎 Не словом, а делом! 
Вы делаете мир вокруг себя лучше.</b>

🎁 <b>Подарочный промокод </b>

<code>{promo_code}</code>

на подписку в закрытый клуб

<b>"𝐎𝐒𝐍𝐎𝐕𝐀 | 𝐏𝐫𝐢𝐯𝐚𝐭𝐞 𝐂𝐥𝐮𝐛"</b>

на {int(month)} месяца(ев) для вашего партнера
активен 72 часа.

💡 Перешлите данное сообщение вашему партнеру!
Мы ждем его в закрытом клубе 

<b>"𝐎𝐒𝐍𝐎𝐕𝐀 | 𝐏𝐫𝐢𝐯𝐚𝐭𝐞 𝐂𝐥𝐮𝐛"</b>

по ссылке -
https://t.me/{bot_name}?start={ref_user_id}\n

🛒 <i>P.s. Партнерские вознаграждения с промокодов не начисляются.</i>	
"""
    return txt
