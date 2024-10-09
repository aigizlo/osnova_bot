# -*- coding: utf-8 -*-
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class MyStates(FSMContext):

    start = 'start'
    # общее состояние для оплаты
    select_period = 'select_period'

    go_to_pay = 'go_to_pay'

    select_pay_method = 'select_pay_method'


    card_method = 'card_method'

    payment_method = 'payment_method'

    present_promo_state = 'present_promo_state'

    card_or_crypto_pay_select = "card_or_crypto_pay_select"

    insert_promo_code = 'insert_promo_code'

    pay_from_balance = 'pay_from_balance'

    # глав меню
    state_main_menu = 'state_main_menu'

    waiting_for_wallet = 'waiting_for_wallet'




    # balance
    state_balance = "state_balance"
    state_replenish_balance = "state_replenish_balance"
    state_send_pay_link = 'state_refill'




    state_choice_fee_tariff = 'state_choice_fee_tariff'


    # promocodes states (эти состояния не задейственны)
    state_promo_my = "state_promo_my"
    state_promo_create = "state_promo_create"
    state_promo_name = "state_promo_name"


class GetuserInfo(StatesGroup):
        twitter = State()
        get_username = State()
        address = State()
        text = State()
        next_stage = State()
        get_img = State()
        get_video = State()
        get_users = State()
        select_users = State()
        get_keyboard = State()
        finishpost = State()
        publish = State()
        reason = State()
        discord = State()


class Statistic(StatesGroup):
    date = State()
    next_stage = State()

