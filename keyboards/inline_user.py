# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.services.sqlite import get_settings, get_payments, get_all_categories, get_positions, get_items, \
get_pod_category, get_pod_categories, get_position
from design import products, profile, faq, support, refill, faq_chat_inl, faq_news_inl, support_inl, ref_system, promocode, \
last_purchases_text, back, close_text, refill_link_inl, refill_check_inl, qiwi_text, yoomoney_text, lava_text, lzt_text, crystalPay_text
from tgbot.data import config
from tgbot.utils.utils_functions import get_admins

def sub():
    s = InlineKeyboardMarkup()
    s.row(InlineKeyboardButton(text='Подписаться', url=config.channel_url))
    s.row(InlineKeyboardButton(text="Проверить✅", callback_data='subprov'))

    return s

def user_menu(user_id):
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(products, callback_data="products:open"))
    kb.append(InlineKeyboardButton(profile, callback_data="profile"))
    kb.append(InlineKeyboardButton(faq, callback_data="faq:open"))
    kb.append(InlineKeyboardButton(support, callback_data="support:open"))
    kb.append(InlineKeyboardButton(refill, callback_data="refill"))
    kb.append(InlineKeyboardButton("⚙️ Меню Администратора", callback_data="admin_menu"))

    keyboard.add(kb[0], kb[1])
    keyboard.add(kb[2], kb[3])
    keyboard.add(kb[4])

    if user_id in get_admins():
        keyboard.add(kb[5])

    return keyboard


def faq_inl():
    keyboard = InlineKeyboardMarkup()
    kb = []
    news = get_settings()['news']
    chat = get_settings()['chat']

    kb.append(InlineKeyboardButton(faq_chat_inl, url=chat))
    kb.append(InlineKeyboardButton(faq_news_inl, url=news))

    keyboard.add(kb[0], kb[1])

    return keyboard

def support_inll():
    keyboard = InlineKeyboardMarkup()
    kb = []
    kb.append(InlineKeyboardButton(support_inl, url=get_settings()['support']))

    keyboard.add(kb[0])

    return keyboard

def chat_inl():
    keyboard = InlineKeyboardMarkup()
    kb = []
    link = get_settings()['chat']

    kb.append(InlineKeyboardButton(faq_chat_inl, url=link))

    keyboard.add(kb[0])

    return keyboard

def news_inl():
    keyboard = InlineKeyboardMarkup()
    kb = []
    link = get_settings()['news']

    kb.append(InlineKeyboardButton(faq_news_inl, url=link))

    keyboard.add(kb[0])

    return keyboard

def profile_inl():
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(ref_system, callback_data="ref_system"))
    kb.append(InlineKeyboardButton(promocode, callback_data="promo_act"))
    kb.append(InlineKeyboardButton(last_purchases_text, callback_data="last_purchases"))
    kb.append(InlineKeyboardButton(back, callback_data="back_to_user_menu"))

    keyboard.add(kb[0])
    keyboard.add(kb[1], kb[2])
    keyboard.add(kb[3])

    return keyboard

def back_to_profile():
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(back, callback_data="profile"))

    return keyboard

def back_to_user_menu():
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(back, callback_data="back_to_user_menu"))

    return keyboard


def close_inl():
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(close_text, callback_data="close_text_mail"))

    keyboard.add(kb[0])

    return keyboard

def refill_open_inl(way, amount, link, id):
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(refill_link_inl, url=link))
    kb.append(InlineKeyboardButton(refill_check_inl, callback_data=f"check_opl:{way}:{amount}:{id}"))

    keyboard.add(kb[0])
    keyboard.add(kb[1])

    return keyboard

def refill_inl():
    keyboard = InlineKeyboardMarkup()
    kb = []
    qiwi = get_payments()['pay_qiwi']
    yoomoney = get_payments()['pay_yoomoney']
    lava = get_payments()['pay_lava']
    crystal = get_payments()['pay_crystal']
    lolz = get_payments()['pay_lolz']

    if qiwi == "True":
        kb.append(InlineKeyboardButton(qiwi_text, callback_data="refill:qiwi"))
    if yoomoney == "True":
        kb.append(InlineKeyboardButton(yoomoney_text, callback_data="refill:yoomoney"))
    if lava == "True":
        kb.append(InlineKeyboardButton(lava_text, callback_data="refill:lava"))
    if lolz == "True":
        kb.append(InlineKeyboardButton(lzt_text, callback_data="refill:lolz"))
    if crystal == "True":
        kb.append(InlineKeyboardButton(crystalPay_text, callback_data="refill:crystal"))

    if len(kb) == 5:
        keyboard.add(kb[0])
        keyboard.add(kb[1], kb[2])
        keyboard.add(kb[3], kb[4])
    elif len(kb) == 4:
        keyboard.add(kb[0], kb[1])
        keyboard.add(kb[2], kb[3])
    elif len(kb) == 3:
        keyboard.add(kb[0])
        keyboard.add(kb[1], kb[2])
    elif len(kb) == 2:
        keyboard.add(kb[0], kb[1])
    elif len(kb) == 1:
        keyboard.add(kb[0])

    keyboard.add(InlineKeyboardButton(back, callback_data="back_to_user_menu"))

    return keyboard

def back_to_user_menu():
    keyboard = InlineKeyboardMarkup()
    kb = []

    keyboard.add(InlineKeyboardButton(back, callback_data="back_to_user_menu"))

    return keyboard

def open_products():
    keyboard = InlineKeyboardMarkup()

    for category in get_all_categories():
        name = category['name']
        cat_id = category['id']
        keyboard.add(InlineKeyboardButton(name, callback_data=f"open_category:{cat_id}"))

    keyboard.add(InlineKeyboardButton(back, callback_data="back_to_user_menu"))

    return keyboard

def open_pod_cat_positions(pod_cat_id):
    keyboard = InlineKeyboardMarkup()

    for pos in get_positions(pod_cat_id=pod_cat_id):
        name = pos['name']
        pos_id = pos['id']
        price = pos['price']
        items = f"{len(get_items(position_id=pos_id))}шт"
        if pos['infinity'] == "+":
            items = "[Безлимит]"
        keyboard.add(InlineKeyboardButton(f"{name} | {price}₽ | {items}", callback_data=f"open_pos:{pos_id}"))

    keyboard.add(InlineKeyboardButton(back, callback_data=f"open_category:{get_pod_category(pod_cat_id)['cat_id']}"))

    return keyboard
def open_positions(cat_id):
    keyboard = InlineKeyboardMarkup()

    for pod_cat in get_pod_categories(cat_id):
        name = pod_cat['name']
        pod_cat_id = pod_cat['id']
        keyboard.add(InlineKeyboardButton(name, callback_data=f"open_pod_cat:{pod_cat_id}"))
    for pos in get_positions(cat_id):
        if pos['pod_category_id'] is not None:
            continue
        name = pos['name']
        pos_id = pos['id']
        price = pos['price']
        items = f"{len(get_items(position_id=pos_id))}шт"
        if pos['infinity'] == "+":
            items = "[Безлимит]"
        keyboard.add(InlineKeyboardButton(f"{name} | {price}₽ | {items}", callback_data=f"open_pos:{pos_id}"))

    keyboard.add(InlineKeyboardButton(back, callback_data=f"products:open"))

    return keyboard

def pos_buy_inl(pos_id):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton("🛍️ Купить", callback_data=f"buy_pos:{pos_id}"))
    keyboard.add(InlineKeyboardButton(back, callback_data=f"open_category:{get_position(pos_id)['category_id']}"))

    return keyboard

def choose_buy_items(pos_id, amount):
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(f"✅ Да, хочу", callback_data=f"buy_items:yes:{pos_id}:{amount}"))
    kb.append(InlineKeyboardButton(f"❌ Нет, не хочу", callback_data=f"buy_items:no:{pos_id}:{amount}"))

    keyboard.add(kb[0], kb[1])

    return keyboard