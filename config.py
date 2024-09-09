import urllib3
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import const

support = "@byshakirov"

admin = 502811372
err_send = 502811372

admins = [502811372, 328521044, 1139164093]

# aiogram
bot = Bot(token=const.token)


storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)



prices = {
    "1": 15,
    "3": 40,
    "12": 150,
}

get_days = {
    1: 30,
    3: 90,
    12: 365,
}