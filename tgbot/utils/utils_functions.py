# - *- coding: utf- 8 - *-
import time
import configparser

from datetime import datetime
from tgbot.data import config
from tgbot.data.loader import bot

# Получение текущего unix времени
def get_unix(full=False):
    if full:
        return time.time_ns()
    else:
        return int(time.time())


# Разбив списка по количеству переданных значений
def split_messages(get_list, count):
    return [get_list[i:i + count] for i in range(0, len(get_list), count)]


# Получение текущей даты
def get_date():
    this_date = datetime.today().replace(microsecond=0)
    this_date = this_date.strftime("%d.%m.%Y %H:%M:%S")

    return this_date

# Получение админов
def get_admins():
    read_admins = configparser.ConfigParser()
    read_admins.read("settings.ini")

    admins = read_admins['settings']['admin_id'].strip().replace(" ", "")

    if "," in admins:
        admins = admins.split(",")
    else:
        if len(admins) >= 1:
            admins = [admins]
        else:
            admins = []

    while "" in admins: 
        admins.remove("")
    while " " in admins: 
        admins.remove(" ")

    admins = list(map(int, admins))

    return admins



# Разбив списка по количеству переданных значений
def split_messages(get_list, count):
    return [get_list[i:i + count] for i in range(0, len(get_list), count)]


# Конвертация дней
def convert_day(day):
    day = int(day)
    days = ['день', 'дня', 'дней']

    if day % 10 == 1 and day % 100 != 11:
        count = 0
    elif 2 <= day % 10 <= 4 and (day % 100 < 10 or day % 100 >= 20):
        count = 1
    else:
        count = 2

    return f"{day} {days[count]}"

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


# Удаление отступов у текста
def ots(get_text: str):
    if get_text is not None:
        split_text = get_text.split("\n")
        if split_text[0] == "": split_text.pop(0)
        if split_text[-1] == "": split_text.pop(-1)
        save_text = []

        for text in split_text:
            while text.startswith(" "):
                text = text[1:]

            save_text.append(text)
        get_text = "\n".join(save_text)

    return get_text

async def send_admins(msg: str, channel: bool):
    channel_id = config.logs_channel_id
    if channel_id == "":
        for admin in get_admins():
            await bot.send_message(chat_id=admin, text=msg)
    else:
        if channel == True:
            await bot.send_message(chat_id=channel_id, text=msg)
        elif channel == False:
            for admin in get_admins():
                await bot.send_message(chat_id=admin, text=msg)