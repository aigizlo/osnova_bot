import urllib3
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

#проверка на подписку в канал (на сервере)
# tg_channel = "@corbots"
# tg_channel_link = 'https://t.me/+3QK8nXUXRC0zNGMy'
# tg_chat = 'https://t.me/+ES53Pv5mO0MyZTQy '




# проверка на подписку в канал (на сервере)
tg_channel = "@off_radar"
tg_channel_link = 'https://t.me/off_radar'
tg_chat = ''


# локально
bot_name = 'offradar_VPNbot'
token = '6820291522:AAHbWTF-zSlL3bIdDqmjqSajYBsGbueRlQs'

# на сервере
# bot_name = 'vpnklyuchi_bot'
# token = '6509663632:AAGG38zVCvSe89tb46ZlhhQiZx53ADABHIQ'

support = "@byshakirov"

admin = 502811372
err_send = 502811372

# aiogram
bot = Bot(token=token)


storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)


host = "localhost"
user = "root"
password = ""
# password = "new_password"
database = "OSNOVA"



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