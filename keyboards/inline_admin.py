# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.services.sqlite import get_settings, get_user, get_all_categories, get_pod_categories, get_positions, get_items
from design import back, qiwi_text, yoomoney_text, lava_text, lzt_text, crystalPay_text


def admin_menu():
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton("🖤 Общие настройки", callback_data="settings"))
    kb.append(InlineKeyboardButton("🎲 Доп. настройки", callback_data="extra_settings"))
    kb.append(InlineKeyboardButton("❗ Выключатели", callback_data="on_off"))
    kb.append(InlineKeyboardButton("📊 Статистика", callback_data="stats"))
    kb.append(InlineKeyboardButton("🔍 Искать", callback_data="find:"))
    kb.append(InlineKeyboardButton("💎 Управление товарами", callback_data="pr_edit"))
    kb.append(InlineKeyboardButton("📌 Рассылка", callback_data="mail_start"))
    kb.append(InlineKeyboardButton("💰 Платежные системы", callback_data="payments"))
    kb.append(InlineKeyboardButton(back, callback_data="back_to_user_menu"))

    keyboard.add(kb[0])
    keyboard.add(kb[1])
    keyboard.add(kb[2])
    keyboard.add(kb[3])
    keyboard.add(kb[4])
    keyboard.add(kb[5])
    keyboard.add(kb[6])
    keyboard.add(kb[7])
    keyboard.add(kb[8])

    return keyboard

def back_sett():
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(back, callback_data="settings_back"))

    return keyboard

def extra_back():
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(back, callback_data="extra_settings"))

    keyboard.add(kb[0])

    return keyboard

def extra_settings_inl():
    keyboard = InlineKeyboardMarkup()
    kb = []


    kb.append(InlineKeyboardButton(f"💎 Создать промокод", callback_data="promo_create"))
    kb.append(InlineKeyboardButton(f"🎲 Удалить промокод", callback_data="promo_delete"))
    kb.append(InlineKeyboardButton(f"2️⃣ Изменить кол-во рефералов для 2 лвла", callback_data="ref_lvl_edit:2"))
    kb.append(InlineKeyboardButton(f"3️⃣ Изменить кол-во рефералов для 3 лвла", callback_data="ref_lvl_edit:3"))
    kb.append(InlineKeyboardButton(back, callback_data="settings_back"))

    keyboard.add(kb[0], kb[1])
    keyboard.add(kb[2])
    keyboard.add(kb[3])
    keyboard.add(kb[4])

    return keyboard

def on_off_inl():
    keyboard = InlineKeyboardMarkup()
    kb = []

    work = get_settings()['is_work']
    purchases = get_settings()['is_buy']
    refills = get_settings()['is_refill']
    ref_system = get_settings()['is_ref']
    notify = get_settings()['is_notify']
    sub = get_settings()['is_sub']

    if sub == "True":
        sub_emoji = "✅"
    else:
        sub_emoji = "❌"

    if notify == "True":
        notify_emoji = "✅"
    else:
        notify_emoji = "❌"

    if work == "True":
        work_emoji = "✅"
    else:
        work_emoji = "❌"

    if purchases == "True":
        buy_emoji = "✅"
    else:
        buy_emoji = "❌"

    if refills == "True":
        refill_emoji = "✅"
    else:
        refill_emoji = "❌"

    if ref_system == "True":
        ref_emoji = "✅"
    else:
        ref_emoji = "❌"

    kb.append(InlineKeyboardButton(f"Тех. Работы | {work_emoji}", callback_data="work:on_off"))
    kb.append(InlineKeyboardButton(f"Покупки | {buy_emoji}", callback_data="buys:on_off"))
    kb.append(InlineKeyboardButton(f"Пополнения | {refill_emoji}", callback_data="refills:on_off"))
    kb.append(InlineKeyboardButton(f"Реф. Система | {ref_emoji}", callback_data="ref:on_off"))
    kb.append(InlineKeyboardButton(f"Увед. О новых юзерах | {notify_emoji}", callback_data="notify:on_off"))
    kb.append(InlineKeyboardButton(f"Проверка подписки | {sub_emoji}", callback_data="sub:on_off"))
    kb.append(InlineKeyboardButton(back, callback_data="settings_back"))

    keyboard.add(kb[0])
    keyboard.add(kb[1])
    keyboard.add(kb[2])
    keyboard.add(kb[3])
    keyboard.add(kb[4])
    keyboard.add(kb[5])
    keyboard.add(kb[6])

    return keyboard

def settings_inl():
    keyboard = InlineKeyboardMarkup()
    kb = []

    faq = get_settings()['faq']
    support = get_settings()['support']
    chat = get_settings()['chat']
    news = get_settings()['news']
    ref_percent_1 = get_settings()['ref_percent_1']
    ref_percent_2 = get_settings()['ref_percent_2']
    ref_percent_3 = get_settings()['ref_percent_3']

    if faq is None or faq == "-" or faq == "None":
        faq_emoji = "❌"
    else:
        faq_emoji = "✅"

    if support is None or support == "-" or support == "None":
        sup_emoji = "❌"
    else:
        sup_emoji = "✅"

    if chat is None or chat == "-" or chat == "None":
        chat_emoji = "❌"
    else:
        chat_emoji = "✅"

    if news is None or news == "-" or news == "None":
        news_emoji = "❌"
    else:
        news_emoji = '✅'

    kb.append(InlineKeyboardButton(f"FAQ | {faq_emoji}", callback_data="faq:edit"))
    kb.append(InlineKeyboardButton(f"Тех. Поддержка | {sup_emoji}", callback_data="sup:edit"))
    kb.append(InlineKeyboardButton(f"Чат | {chat_emoji}", callback_data="chat:edit"))
    kb.append(InlineKeyboardButton(f"Новостной | {news_emoji}", callback_data="news:edit"))
    kb.append(InlineKeyboardButton(f"Реф. Процент 1 лвл. | {ref_percent_1}%", callback_data="ref_percent:edit:1"))
    kb.append(InlineKeyboardButton(f"Реф. Процент 2 лвл. | {ref_percent_2}%", callback_data="ref_percent:edit:2"))
    kb.append(InlineKeyboardButton(f"Реф. Процент 3 лвл. | {ref_percent_3}%", callback_data="ref_percent:edit:3"))
    kb.append(InlineKeyboardButton(back, callback_data="settings_back"))

    keyboard.add(kb[0])
    keyboard.add(kb[1])
    keyboard.add(kb[2])
    keyboard.add(kb[3])
    keyboard.add(kb[4])
    keyboard.add(kb[5])
    keyboard.add(kb[6])
    keyboard.add(kb[7])

    return keyboard

def find_back():
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(back, callback_data="find:back"))

    return keyboard


def profile_adm_inl(user_id):
    keyboard = InlineKeyboardMarkup()
    kb = []

    user = get_user(id=user_id)

    kb.append(InlineKeyboardButton("💰 Выдать баланс", callback_data=f"user:balance_add:{user_id}"))
    kb.append(InlineKeyboardButton("💰 Изменить баланс", callback_data=f"user:balance_edit:{user_id}"))
    if user['is_ban'] == "True":
        kb.append(InlineKeyboardButton("⛔ Разблокировать", callback_data=f"user:is_ban_unban:{user_id}"))
    elif user['is_ban'] == "False":
        kb.append(InlineKeyboardButton("⛔ Заблокировать", callback_data=f"user:is_ban_ban:{user_id}"))
    kb.append(InlineKeyboardButton("⭐ Отправить уведомление", callback_data=f"user:sms:{user_id}"))

    keyboard.add(kb[0], kb[1])
    keyboard.add(kb[2])
    keyboard.add(kb[3])


    return keyboard


def find_settings():
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton("👤 Профиль", callback_data="find:profile"))
    kb.append(InlineKeyboardButton("🧾 Чек", callback_data="find:receipt"))
    kb.append(InlineKeyboardButton(back, callback_data="settings_back"))

    keyboard.add(kb[0])
    keyboard.add(kb[1])
    keyboard.add(kb[2])

    return keyboard

def payments_settings():
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(qiwi_text, callback_data="payments:qiwi"))
    kb.append(InlineKeyboardButton(yoomoney_text, callback_data="payments:yoomoney"))
    kb.append(InlineKeyboardButton(lava_text, callback_data="payments:lava"))
    kb.append(InlineKeyboardButton(lzt_text, callback_data="payments:lzt"))
    kb.append(InlineKeyboardButton(crystalPay_text, callback_data="payments:crystalPay"))
    kb.append(InlineKeyboardButton(back, callback_data="settings_back"))

    keyboard.add(kb[0])
    keyboard.add(kb[1])
    keyboard.add(kb[2])
    keyboard.add(kb[3])
    keyboard.add(kb[4])
    keyboard.add(kb[5])

    return keyboard

def payments_settings_info(way, status):
    keyboard = InlineKeyboardMarkup()
    kb = []

    if status == "True":
        kb.append(InlineKeyboardButton("❌ Выключить", callback_data=f"payments_on_off:{way}:off"))
    else:
        kb.append(InlineKeyboardButton("✅ Включить", callback_data=f"payments_on_off:{way}:on"))
    kb.append(InlineKeyboardButton("💰 Узнать баланс", callback_data=f"payments_balance:{way}"))
    kb.append(InlineKeyboardButton("📌 Показать информацию", callback_data=f"payments_info:{way}"))
    kb.append(InlineKeyboardButton(back, callback_data="payments"))

    keyboard.add(kb[0])
    keyboard.add(kb[1], kb[2])
    keyboard.add(kb[3])

    return keyboard

def set_back():
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(back, callback_data="settings"))

    keyboard.add(kb[0])

    return keyboard

def payments_back():
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(back, callback_data="payments"))

    keyboard.add(kb[0])

    return keyboard

def mail_types():
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton("💎 Просто текст", callback_data=f"mail:text"))
    kb.append(InlineKeyboardButton("📌 Текст с картинкой", callback_data=f"mail:photo"))
    kb.append(InlineKeyboardButton(back, callback_data="settings_back"))

    keyboard.add(kb[0], kb[1])
    keyboard.add(kb[2])

    return keyboard

def opr_mail_text():
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton("✅ Да, хочу", callback_data=f"mail_start_text:yes"))
    kb.append(InlineKeyboardButton("❌ Нет, не хочу", callback_data=f"mail_start_text:no"))

    keyboard.add(kb[0], kb[1])

    return keyboard

def opr_mail_photo():
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton("✅ Да, хочу", callback_data=f"mail_start_photo:yes"))
    kb.append(InlineKeyboardButton("❌ Нет, не хочу", callback_data=f"mail_start_photo:no"))

    keyboard.add(kb[0], kb[1])

    return keyboard

def products_edits():
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton("➕ | Категорию", callback_data=f"add_cat"))
    kb.append(InlineKeyboardButton("⚙️ | Категорию", callback_data=f"edit_cat"))
    kb.append(InlineKeyboardButton("🗑️ | ВСЕ Категории", callback_data=f"del_all_cats"))

    kb.append(InlineKeyboardButton("➕ | Под-Категорию", callback_data=f"add_pod_cat"))
    kb.append(InlineKeyboardButton("⚙️ | Под-Категорию", callback_data=f"edit_pod_cat"))
    kb.append(InlineKeyboardButton("🗑️ | ВСЕ Под-Категории", callback_data=f"del_all_pod_cats"))

    kb.append(InlineKeyboardButton("➕ | Позицию", callback_data=f"add_pos"))
    kb.append(InlineKeyboardButton("⚙️ | Позицию", callback_data=f"edit_pos"))
    kb.append(InlineKeyboardButton("🗑️ | ВСЕ Позиции", callback_data=f"del_all_poss"))

    kb.append(InlineKeyboardButton("➕ | Товары", callback_data=f"add_items"))
    kb.append(InlineKeyboardButton("🗑️ | ВСЕ Товары", callback_data=f"del_all_items"))

    kb.append(InlineKeyboardButton(back, callback_data="settings_back"))

    keyboard.add(kb[0], kb[1], kb[2])
    keyboard.add(kb[3], kb[4], kb[5])
    keyboard.add(kb[6], kb[7], kb[8])
    keyboard.add(kb[9], kb[10])
    keyboard.add(kb[11])

    return keyboard

def back_pr_edits():
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(back, callback_data="pr_edit"))

    keyboard.add(kb[0])

    return keyboard

def open_cats_for_edit():
    keyboard = InlineKeyboardMarkup()

    for category in get_all_categories():
        name = category['name']
        cat_id = category['id']
        keyboard.add(InlineKeyboardButton(name, callback_data=f"cat_edit:{cat_id}"))

    return keyboard

def open_cats_for_edit_pod_cat():
    keyboard = InlineKeyboardMarkup()

    for category in get_all_categories():
        name = category['name']
        cat_id = category['id']
        keyboard.add(InlineKeyboardButton(name, callback_data=f"pods_cat_edit:{cat_id}"))

    keyboard.add(InlineKeyboardButton(back, callback_data=f"pr_edit"))

    return keyboard

def open_pod_cats_for_edit(cat_id):
    keyboard = InlineKeyboardMarkup()

    for pod_category in get_pod_categories(cat_id):
        name = pod_category['name']
        pod_cat_id = pod_category['id']
        keyboard.add(InlineKeyboardButton(name, callback_data=f"podss_cat_edit:{pod_cat_id}"))

    return keyboard

def open_cats_for_add_pod_cat():
    keyboard = InlineKeyboardMarkup()

    for category in get_all_categories():
        name = category['name']
        cat_id = category['id']
        keyboard.add(InlineKeyboardButton(name, callback_data=f"add_pod_cat_cat:{cat_id}"))

    keyboard.add(InlineKeyboardButton(back, callback_data=f"pr_edit"))

    return keyboard

def edit_cat_inl(cat_id):
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(f"Изменить название", callback_data=f"edit_cat_name:{cat_id}"))
    kb.append(InlineKeyboardButton(f"Удалить", callback_data=f"del_cat:{cat_id}"))
    kb.append(InlineKeyboardButton(back, callback_data=f"edit_cat"))

    keyboard.add(kb[0], kb[1])
    keyboard.add(kb[2])

    return keyboard

def choose_del_cat(cat_id):
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(f"✅ Да, хочу", callback_data=f"dels_cat:yes:{cat_id}"))
    kb.append(InlineKeyboardButton(f"❌ Нет, не хочу", callback_data=f"dels_cat:no:{cat_id}"))

    keyboard.add(kb[0], kb[1])

    return keyboard

def choose_del_all_cats():
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(f"✅ Да, хочу", callback_data=f"dels_all_cat:yes"))
    kb.append(InlineKeyboardButton(f"❌ Нет, не хочу", callback_data=f"dels_all_cat:no"))

    keyboard.add(kb[0], kb[1])

    return keyboard

def update_pod_cat_inl(pod_cat_id):
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(f"Изменить название", callback_data=f"edit_pod_cat_name:{pod_cat_id}"))
    kb.append(InlineKeyboardButton(f"Удалить", callback_data=f"del_pod_cat:{pod_cat_id}"))
    kb.append(InlineKeyboardButton(back, callback_data=f"edit_pod_cat"))

    keyboard.add(kb[0], kb[1])
    keyboard.add(kb[2])

    return keyboard

def choose_del_pod_cat(pod_cat_id):
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(f"✅ Да, хочу", callback_data=f"dels_pod_cat:yes:{pod_cat_id}"))
    kb.append(InlineKeyboardButton(f"❌ Нет, не хочу", callback_data=f"dels_pod_cat:no:{pod_cat_id}"))

    keyboard.add(kb[0], kb[1])

    return keyboard

def choose_del_all_pod_cats():
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(f"✅ Да, хочу", callback_data=f"dels_all_pod_cats:yes"))
    kb.append(InlineKeyboardButton(f"❌ Нет, не хочу", callback_data=f"dels_all_pod_cats:no"))

    keyboard.add(kb[0], kb[1])

    return keyboard

def open_cats_for_add_pos():
    keyboard = InlineKeyboardMarkup()

    for category in get_all_categories():
        name = category['name']
        cat_id = category['id']
        keyboard.add(InlineKeyboardButton(name, callback_data=f"add_pos_cat:{cat_id}"))

    keyboard.add(InlineKeyboardButton(back, callback_data=f"pr_edit"))

    return keyboard

def open_pod_cats_for_add_pos(cat_id):
    keyboard = InlineKeyboardMarkup()

    for pod_category in get_pod_categories(cat_id):
        name = pod_category['name']
        pod_cat_id = pod_category['id']
        keyboard.add(InlineKeyboardButton(name, callback_data=f"pod_cat_add_pos:{pod_cat_id}:{cat_id}"))

    keyboard.add(InlineKeyboardButton(f"💎 Выбрать эту категорию", callback_data=f"add_poss_cat:{cat_id}"))
    keyboard.add(InlineKeyboardButton(back, callback_data=f"add_pos"))

    return keyboard


def open_cats_for_edit_pos():
    keyboard = InlineKeyboardMarkup()

    for category in get_all_categories():
        name = category['name']
        cat_id = category['id']
        keyboard.add(InlineKeyboardButton(name, callback_data=f"edit_pos_cat:{cat_id}"))

    keyboard.add(InlineKeyboardButton(back, callback_data=f"pr_edit"))

    return keyboard

def open_pod_cats_for_edit_pos(cat_id):
    keyboard = InlineKeyboardMarkup()

    for pod_category in get_pod_categories(cat_id):
        name = pod_category['name']
        pod_cat_id = pod_category['id']
        keyboard.add(InlineKeyboardButton(name, callback_data=f"pod_cat_edit_pos:{pod_cat_id}:{cat_id}"))
    for position in get_positions(cat_id):
        name = position['name']
        pos_id = position['id']
        price = position['price']
        items = f"{len(get_items(position_id=pos_id))}шт"
        if position['infinity'] == "+":
            items = "[Безлимит]"
        if position['pod_category_id'] is not None:
            continue
        keyboard.add(InlineKeyboardButton(f"{name} | {price}₽ | {items}", callback_data=f"edit_pos:{pos_id}"))

    keyboard.add(InlineKeyboardButton(back, callback_data=f"edit_pos"))

    return keyboard

def open_positions_for_edit(cat_id, pod_cat_id = None):
    keyboard = InlineKeyboardMarkup()

    if pod_cat_id is None:
        for position in get_positions(cat_id):
            name = position['name']
            pos_id = position['id']
            price = position['price']
            items = get_items(position_id=pos_id)
            keyboard.add(InlineKeyboardButton(f"{name} | {price}₽ | {len(items)}шт.", callback_data=f"edit_pos:{pos_id}"))
    else:
        for position in get_positions(cat_id, pod_cat_id):
            name = position['name']
            pos_id = position['id']
            price = position['price']
            items = get_items(position_id=pos_id)
            keyboard.add(InlineKeyboardButton(f"{name} | {price}₽ | {len(items)}шт.", callback_data=f"edit_pos:{pos_id}"))

    keyboard.add(InlineKeyboardButton(back, callback_data=f"edit_pos"))

    return keyboard

def edit_pos_inl(pos_id):
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(f"Цена", callback_data=f"edit_price_pos:{pos_id}"))
    kb.append(InlineKeyboardButton(f"Название", callback_data=f"edit_name_pos:{pos_id}"))
    kb.append(InlineKeyboardButton(f"Описание", callback_data=f"edit_desc_pos:{pos_id}"))
    kb.append(InlineKeyboardButton(f"Фото", callback_data=f"edit_photo_pos:{pos_id}"))
    kb.append(InlineKeyboardButton(f"Тип товара", callback_data=f"edit_infinity_pos:{pos_id}"))
    kb.append(InlineKeyboardButton(f"Удалить", callback_data=f"edit_del_pos:{pos_id}"))
    kb.append(InlineKeyboardButton(f"Очистить товары", callback_data=f"edit_clear_items_pos:{pos_id}"))
    kb.append(InlineKeyboardButton(f"Загрузить товары", callback_data=f"edit_upload_items_pos:{pos_id}"))


    keyboard.add(kb[0], kb[1])
    keyboard.add(kb[2], kb[3], kb[4])
    keyboard.add(kb[5])
    keyboard.add(kb[7], kb[6])
    keyboard.add(InlineKeyboardButton(back, callback_data=f"edit_pos"))

    return keyboard

def choose_del_pos(pos_id):
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(f"✅ Да, хочу", callback_data=f"dels_pos:yes:{pos_id}"))
    kb.append(InlineKeyboardButton(f"❌ Нет, не хочу", callback_data=f"dels_pos:no:{pos_id}"))

    keyboard.add(kb[0], kb[1])

    return keyboard

def choose_del_all_pos():
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(f"✅ Да, хочу", callback_data=f"dels_all_poss:yes"))
    kb.append(InlineKeyboardButton(f"❌ Нет, не хочу", callback_data=f"dels_all_poss:no"))

    keyboard.add(kb[0], kb[1])

    return keyboard

def open_cats_for_add_items():
    keyboard = InlineKeyboardMarkup()

    for category in get_all_categories():
        name = category['name']
        cat_id = category['id']
        keyboard.add(InlineKeyboardButton(name, callback_data=f"add_items_cat:{cat_id}"))

    keyboard.add(InlineKeyboardButton(back, callback_data=f"pr_edit"))

    return keyboard

def open_pod_cats_for_add_items(cat_id):
    keyboard = InlineKeyboardMarkup()

    for pod_category in get_pod_categories(cat_id):
        name = pod_category['name']
        pod_cat_id = pod_category['id']
        keyboard.add(InlineKeyboardButton(name, callback_data=f"pod_cat_add_items:{pod_cat_id}:{cat_id}"))
    for position in get_positions(cat_id):
        name = position['name']
        pos_id = position['id']
        price = position['price']
        items = f"{len(get_items(position_id=pos_id))}шт"
        if position['infinity'] == "+":
            items = "[Безлимит]"
        if position['pod_category_id'] is not None:
            continue
        keyboard.add(InlineKeyboardButton(f"{name} | {price}₽ | {items}", callback_data=f"pos_add_items:{pos_id}"))

    keyboard.add(InlineKeyboardButton(back, callback_data=f"edit_pos"))

    return keyboard

def open_positions_for_add_items(cat_id, pod_cat_id = None):
    keyboard = InlineKeyboardMarkup()

    if pod_cat_id is None:
        for position in get_positions(cat_id):
            name = position['name']
            pos_id = position['id']
            price = position['price']
            items = get_items(position_id=pos_id)
            keyboard.add(InlineKeyboardButton(f"{name} | {price}₽ | {len(items)}шт.", callback_data=f"spos_add_items:{pos_id}"))
    else:
        for position in get_positions(cat_id, pod_cat_id):
            name = position['name']
            pos_id = position['id']
            price = position['price']
            items = get_items(position_id=pos_id)
            keyboard.add(InlineKeyboardButton(f"{name} | {price}₽ | {len(items)}шт.", callback_data=f"spos_add_items:{pos_id}"))

    keyboard.add(InlineKeyboardButton(back, callback_data=f"edit_pos"))

    return keyboard

def stop_add_items():
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(f"❌ Закончить загрузку", callback_data=f"stop_add_items"))

    return keyboard

def choose_del_all_items():
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(f"✅ Да, хочу", callback_data=f"dels_all_items:yes"))
    kb.append(InlineKeyboardButton(f"❌ Нет, не хочу", callback_data=f"dels_all_items:no"))

    keyboard.add(kb[0], kb[1])

    return keyboard

def choose_clear_items_pos(pos_id):
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(f"✅ Да, хочу", callback_data=f"clear_items:yes:{pos_id}"))
    kb.append(InlineKeyboardButton(f"❌ Нет, не хочу", callback_data=f"clear_items:no:{pos_id}"))

    keyboard.add(kb[0], kb[1])

    return keyboard