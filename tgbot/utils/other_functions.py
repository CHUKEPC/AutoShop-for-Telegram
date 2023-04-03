# - *- coding: utf- 8 - *-
from tgbot.services.sqlite import get_user
from aiogram.types import Message, CallbackQuery
from design import open_profile_text
from tgbot.services.sqlite import update_settings
from tgbot.utils.utils_functions import get_admins
from tgbot.data.loader import bot
from tgbot.utils.utils_functions import get_unix

def convert_ref(ref):
    ref = int(ref)
    refs = ['реферал', 'реферала', 'рефералов']

    if ref % 10 == 1 and ref % 100 != 11:
        count = 0
    elif 2 <= ref % 10 <= 4 and (ref % 100 < 10 or ref % 100 >= 20):
        count = 1
    else:
        count = 2

    return f"{refs[count]}"

def open_profile(call: CallbackQuery = None, message: Message = None):
    user = get_user(id=call.from_user.id)
    user_id = user['id']
    user_name = user['user_name']
    balance = user['balance']
    total_refill = user['total_refill']
    reg_date = user['reg_date']
    ref_count = user['ref_count']
    return open_profile_text(user_id, user_name, balance, total_refill, reg_date, ref_count)


# Автоматическая очистка ежедневной статистики после 00:00
async def update_profit_day():

    update_settings(profit_day=get_unix())


# Автоматическая очистка еженедельной статистики в понедельник 00:00
async def update_profit_week():
    update_settings(profit_week=get_unix())

async def autobackup_db():
    db_path = "tgbot/data/database.db"
    with open(db_path, "rb") as data:
        for admin in get_admins():
            await bot.send_document(chat_id=admin, document=data, caption="<b>⚙️ АвтоБэкап базы данных ⚙️</b>")