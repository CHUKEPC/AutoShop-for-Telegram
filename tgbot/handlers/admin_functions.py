# - *- coding: utf- 8 - *-
import nest_asyncio
import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from tgbot.keyboards.inline_admin import admin_menu, mail_types, opr_mail_photo, opr_mail_text, settings_inl, on_off_inl, find_settings, \
find_back, profile_adm_inl, set_back, back_sett, extra_back, extra_settings_inl
from tgbot.services.sqlite import all_users, get_user, get_refill, get_purchase, get_settings, update_settings, \
all_purchases, all_refills, create_coupon, delete_coupon, update_user
from tgbot.keyboards.inline_user import close_inl
from tgbot.filters.is_admin import IsAdmin
from tgbot.data.loader import dp, bot
from tgbot.utils.utils_functions import send_admins, get_admins, ots

nest_asyncio.apply()

async def mail_start_text(call: CallbackQuery, msg):
    await send_admins(f"<b>❗ Администратор @{call.from_user.username} запустил рассылку!</b>", True)
    users = all_users()
    yes_users, no_users = 0, 0
    for user in users:
        try:
            user_id = user['id']
            await bot.send_message(chat_id=user_id, text=msg, reply_markup=close_inl())
            yes_users += 1
        except:
            no_users += 1

    new_msg = f"""
<b>💎 Всего пользователей: <code>{len(all_users())}</code>
✅ Отправлено: <code>{yes_users}</code>
❌ Не отправлено (Бот заблокирован): <code>{no_users}</code></b>
    """

    await call.message.answer(new_msg)

async def mail_start_photo(call: CallbackQuery, msg, file_id):
    await send_admins(f"<b>❗ Администратор @{call.from_user.username} запустил рассылку!</b>", True)
    users = all_users()
    yes_users, no_users = 0, 0
    for user in users:
        try:
            user_id = user['id']
            await bot.send_photo(chat_id=user_id, photo=file_id, caption=msg, reply_markup=close_inl())
            yes_users += 1
        except:
            no_users += 1

    new_msg = f"""
<b>💎 Всего пользователей: <code>{len(all_users())}</code>
✅ Отправлено: <code>{yes_users}</code>
❌ Не отправлено (Бот заблокирован): <code>{no_users}</code></b>
    """

    await call.message.answer(new_msg)

@dp.message_handler(IsAdmin(), commands=['admin', 'adm', 'a'], state="*")
async def admin_menu_send(message: Message, state: FSMContext):
    await state.finish()

    await message.answer("Добро пожаловать в меню Администратора", reply_markup=admin_menu())

@dp.callback_query_handler(IsAdmin(), text="admin_menu", state="*")
async def admin_menu_send(call: CallbackQuery, state: FSMContext):
    await state.finish()

    await call.message.delete()
    await call.message.answer("Добро пожаловать в меню Администратора", reply_markup=admin_menu())

@dp.callback_query_handler(IsAdmin(), text="settings_back", state="*")
async def admin_menu_send(call: CallbackQuery, state: FSMContext):
    await state.finish()

    await call.message.edit_text("Добро пожаловать в меню Администратора", reply_markup=admin_menu())


@dp.callback_query_handler(IsAdmin(), text = "mail_start", state="*")
async def adm_mail_start(call: CallbackQuery, state: FSMContext):
    await state.finish()

    await call.message.edit_text("<b>❗ Выберите тип рассылки</b>", reply_markup=mail_types())

@dp.callback_query_handler(text_startswith = "mail:", state="*")
async def mail_types_chosen(call: CallbackQuery, state: FSMContext):
    await state.finish()
    

    tip = call.data.split(":")[1]
    if tip == "text":
        await call.message.edit_text("<b>❗ Введите текст для рассылки \n📌 Можно использовать HTML-Разметку.</b>")
        await state.set_state("here_text_mail_text")
    elif tip == "photo":
        await call.message.edit_text("<b>❗ Введите текст для рассылки \n📌 Можно использовать HTML-Разметку.</b>")
        await state.set_state("here_text_mail_photo")

@dp.message_handler(IsAdmin(), state="here_text_mail_text")
async def mail_text_start(message: Message, state: FSMContext):

    msg = message.text
    await message.answer(f"<b>❗ Вы точно хотите запустить рассылку с таким текстом?</b>")
    await message.answer(msg, reply_markup=opr_mail_text())
    await state.update_data(here_text_mail_text=msg)

@dp.callback_query_handler(text_startswith="mail_start_text:", state="*")
async def mail_opr(call: CallbackQuery, state: FSMContext):

    way = call.data.split(":")[1]

    async with state.proxy() as data:
        msg = data['here_text_mail_text']

    if way == "no":
        await call.message.edit_text("<b>❗ Введите новый текст для рассылки \n📌 Можно использовать HTML-Разметку.</b>")
        await state.set_state("here_text_mail_text")
    elif way == "yes":
        loop = asyncio.get_event_loop()
        a1 = loop.create_task(mail_start_text(call, msg))
        loop.run_until_complete(a1)

###################################################################################

@dp.message_handler(IsAdmin(), state="here_text_mail_photo")
async def mail_photo_start(message: Message, state: FSMContext):

    msg = message.text
    await message.answer(f"<b>❗ Отправьте фото для рассылки</b>")
    await state.update_data(here_text_mail_photo=msg)
    await state.set_state("here_photo_mail_photo")

@dp.message_handler(IsAdmin(), content_types=['photo'], state="here_photo_mail_photo")
async def mail_photo_starts(message: Message, state: FSMContext):
    photo = message.photo[-1].file_id
    msg = (await state.get_data())['here_text_mail_photo']
    await state.update_data(here_photo_mail_photo=photo)

    await message.answer(f"<b>❗ Вы точно хотите запустить рассылку с таким текстом?</b>")
    await bot.send_photo(chat_id=message.from_user.id, photo=photo, caption=msg, reply_markup=opr_mail_photo())

@dp.callback_query_handler(text_startswith="mail_start_photo:", state="*")
async def mail_opr(call: CallbackQuery, state: FSMContext):

    way = call.data.split(":")[1]

    msg = (await state.get_data())['here_text_mail_photo']
    file_id = (await state.get_data())['here_photo_mail_photo']

    if way == "no":
        await call.message.edit_text("<b>❗ Введите новый текст для рассылки \n📌 Можно использовать HTML-Разметку.</b>")
        await state.set_state("here_text_mail_photo")
    elif way == "yes":
        loop = asyncio.get_event_loop()
        a1 = loop.create_task(mail_start_photo(call, msg, file_id))
        loop.run_until_complete(a1)


@dp.callback_query_handler(IsAdmin(), text_startswith="settings", state="*")
async def settings_open(call: CallbackQuery, state: FSMContext):
    await state.finish()

    await call.message.edit_text("<b>⚙️ Основные настройки бота.</b>", reply_markup=settings_inl())

@dp.callback_query_handler(IsAdmin(), text_startswith="on_off", state="*")
async def on_off_open(call: CallbackQuery, state: FSMContext):
    await state.finish()

    await call.message.edit_text("<b>⚙️ Выберите что хотите выключить/включить \n❌ - Выкл. | ✅ - Вкл.</b>", reply_markup=on_off_inl())

@dp.callback_query_handler(IsAdmin(), text="find:", state='*')
async def find_open(call: CallbackQuery, state: FSMContext):
    await state.finish()

    await call.message.edit_text("<b>⚙️ Выберите что хотите найти</b>", reply_markup=find_settings())

@dp.callback_query_handler(IsAdmin(), text="find:profile", state="*")
async def find_profile_open(call: CallbackQuery, state: FSMContext):
    await state.finish()


    await call.message.edit_text("<b>❗ Введите ID, имя или @username пользователя</b>", reply_markup=find_back())
    await state.set_state("here_user")

@dp.message_handler(state="here_user")
async def find_profile_op(message: Message, state: FSMContext):
    if message.text.isdigit():
        user = get_user(id=message.text)
    elif message.text.startswith("@"):
        user = get_user(user_name=message.text.split("@")[1])
    else:
        user = get_user(first_name=message.text)

    if user is None:
        await message.reply("<b>❗ Такого пользователя нет! Перепроверьте данные!</b>")
    else:
        await state.finish()

        user_name = user['user_name']
        user_id = user['id']
        balance = user['balance']
        total_refill = user['total_refill']
        reg_date = user['reg_date']
        ref_count = user['ref_count']

        msg = f"""
<b>👤 Профиль:
💎 Юзер: @{user_name}
🆔 ID: <code>{user_id}</code>
💰 Баланс: <code>{balance} RUB</code>
💵 Всего пополнено: <code>{total_refill} RUB</code>
📌 Дата регистрации: <code>{reg_date}</code>
👥 Рефералов: <code>{ref_count} чел</code></b>
"""
        await message.answer(ots(msg), reply_markup=profile_adm_inl(user_id))


@dp.callback_query_handler(IsAdmin(), text="find:receipt", state="*")
async def find_receipt(call: CallbackQuery, state: FSMContext):
    await state.finish()


    await call.message.edit_text("<b>❗ Введите чек</b>", reply_markup=find_back())
    await state.set_state("here_receipt")

@dp.message_handler(state="here_receipt")
async def find_receipt_op(message: Message, state: FSMContext):
    if get_refill(receipt=message.text) is not None and get_purchase(receipt=message.text) is None:
        await state.finish()

        refill = get_refill(receipt=message.text)
        msg = f"""
<b>⭐ Чек <code>{message.text}</code>:

⚙️ Тип: <code>Пополнение</code>
💎 Юзер: @{refill['user_name']} | <a href='tg://user?id={refill['user_id']}'>{refill['user_full_name']}</a> | <code>{refill['user_id']}</code>
📌 Способ: <code>{refill['way']}</code>
💰 Сумма: <code>{refill['amount']} RUB</code>
🎲 Дата: <code>{refill['date']}</code></b>
        """

        await message.answer(ots(msg))

    elif get_refill(receipt=message.text) is None and get_purchase(receipt=message.text) is not None:
        await state.finish()

        purchase = get_purchase(receipt=message.text)
        msg = f"""
        <b>⭐ Чек <code>{message.text}</code>:

        ⚙️ Тип: <code>Покупка</code>
        💎 Юзер: @{purchase['user_name']} | <a href='tg://user?id={purchase['user_id']}'>{purchase['user_full_name']}</a> | <code>{purchase['user_id']}</code>
        📌 Позиция: <code>{purchase['position_name']}</code>
        💰 Цена: <code>{purchase['price']} RUB</code>
        💚 Кол-во: <code>{purchase['count']} Шт.</code>
        🎲 Дата: <code>{purchase['date']}</code>
        🛍️ Сам товар:</b>
        
        {purchase['item']}
                """

        await message.answer(ots(msg))
    elif get_refill(receipt=message.text) is None and get_purchase(receipt=message.text) is None:
        await message.answer("<b>❗ Такого чека нет! Перепроверьте данные!</b>")

@dp.callback_query_handler(IsAdmin(), text_startswith="faq:edit", state="*")
async def settings_set_faq(call: CallbackQuery, state: FSMContext):

    await state.set_state("here_faq")
    await call.message.edit_text("<b>⚙️ Введите новый текст для FAQ \n"
                           "❕ Вы можете использовать HTML разметку:</b> \n"
                           "❕ Отправьте <code>-</code> чтобы оставить пустым.", reply_markup=set_back())

@dp.callback_query_handler(IsAdmin(), text_startswith="ref_percent:edit:", state="*")
async def settings_set_faq(call: CallbackQuery, state: FSMContext):
    await state.update_data(cache_ref_lvl_to_edit_percent=call.data.split(":")[2])
    await state.set_state("here_ref_percent")
    await call.message.edit_text(f"<b>⚙️ Введите новый процент для {call.data.split(':')[2]} реферального уровня:</b>", reply_markup=set_back())

@dp.callback_query_handler(IsAdmin(), text_startswith="sup:edit", state="*")
async def settings_set_sup(call: CallbackQuery, state: FSMContext):
    await state.set_state("here_support")
    await call.message.edit_text("<b>⚙️ Введите ссылку на пользователя (https://t.me/юзернейм)</b>"
                              "❕ Отправьте <code>-</code> чтобы оставить пустым.", reply_markup=set_back())

@dp.callback_query_handler(IsAdmin(), text_startswith="chat:edit", state="*")
async def settings_set_chat(call: CallbackQuery, state: FSMContext):
    await state.set_state("here_chat")
    await call.message.edit_text("<b>⚙️ Отправьте ссылку на чат:</b>"
                              "❕ Отправьте <code>-</code> чтобы оставить пустым.", reply_markup=set_back())

@dp.callback_query_handler(IsAdmin(), text_startswith="news:edit", state="*")
async def settings_set_news(call: CallbackQuery, state: FSMContext):
    await state.set_state("here_news")
    await call.message.edit_text("<b>⚙️ Отправьте ссылку на канал:</b>"
                              "❕ Отправьте <code>-</code> чтобы оставить пустым.", reply_markup=set_back())

@dp.callback_query_handler(IsAdmin(), text_startswith="refills:on_off", state="*")
async def settings_vkl_refill(call: CallbackQuery, state: FSMContext):
    await state.finish()
    status_refill = get_settings()['is_refill']

    if status_refill == "True":
        update_settings(is_refill="False")
    if status_refill == "False":
        update_settings(is_refill="True")

    msg = "<b>⚙️ Выберите что хотите выключить/включить \n❌ - Выкл. | ✅ - Вкл.</b>"
    kb = on_off_inl()

    await call.message.edit_text(msg, reply_markup=kb)

@dp.callback_query_handler(IsAdmin(), text_startswith="work:on_off", state="*")
async def settings_vkl_work(call: CallbackQuery, state: FSMContext):
    await state.finish()
    status_work = get_settings()['is_work']

    if status_work == "True":
        update_settings(is_work="False")
    if status_work == "False":
        update_settings(is_work="True")

    msg = "<b>⚙️ Выберите что хотите выключить/включить \n❌ - Выкл. | ✅ - Вкл.</b>"
    kb = on_off_inl()

    await call.message.edit_text(msg, reply_markup=kb)

@dp.callback_query_handler(IsAdmin(), text_startswith="ref:on_off", state="*")
async def settings_vkl_work(call: CallbackQuery, state: FSMContext):
    await state.finish()
    status_ref = get_settings()['is_ref']

    if status_ref == "True":
        update_settings(is_ref="False")
    if status_ref == "False":
        update_settings(is_ref="True")

    msg = "<b>⚙️ Выберите что хотите выключить/включить \n❌ - Выкл. | ✅ - Вкл.</b>"
    kb = on_off_inl()

    await call.message.edit_text(msg, reply_markup=kb)

@dp.callback_query_handler(IsAdmin(), text_startswith="notify:on_off", state="*")
async def settings_vkl_work(call: CallbackQuery, state: FSMContext):
    await state.finish()
    is_notify = get_settings()['is_notify']

    if is_notify == "True":
        update_settings(is_notify="False")
    if is_notify == "False":
        update_settings(is_notify="True")

    msg = "<b>⚙️ Выберите что хотите выключить/включить \n❌ - Выкл. | ✅ - Вкл.</b>"
    kb = on_off_inl()

    await call.message.edit_text(msg, reply_markup=kb)

@dp.callback_query_handler(IsAdmin(), text_startswith="sub:on_off", state="*")
async def settings_vkl_work(call: CallbackQuery, state: FSMContext):
    await state.finish()

    is_sub = get_settings()['is_sub']

    if is_sub == "True":
        update_settings(is_sub="False")
    if is_sub == "False":
        update_settings(is_sub="True")

    msg = "<b>⚙️ Выберите что хотите выключить/включить \n❌ - Выкл. | ✅ - Вкл.</b>"
    kb = on_off_inl()

    await call.message.edit_text(msg, reply_markup=kb)

@dp.callback_query_handler(IsAdmin(), text_startswith="buys:on_off", state="*")
async def settings_vkl_buys(call: CallbackQuery, state: FSMContext):
    await state.finish()

    status_buy = get_settings()['is_buy']

    if status_buy == "True":
        update_settings(is_buy="False")
    if status_buy == "False":
        update_settings(is_buy="True")

    msg = "<b>⚙️ Выберите что хотите выключить/включить \n❌ - Выкл. | ✅ - Вкл.</b>"
    kb = on_off_inl()

    await call.message.edit_text(msg, reply_markup=kb)


@dp.message_handler(IsAdmin(), state="here_faq")
@dp.message_handler(IsAdmin(), text="-", state="here_faq")
async def settings_faq_set(message: Message, state: FSMContext):
    await state.finish()

    update_settings(faq=message.text)
    await send_admins(f"<b>❗ Администратор  @{message.from_user.username} Изменил FAQ на: \n{message.text}</b>", True)
    await message.answer("<b>✅ Готово! FAQ Было изменено!</b>")


@dp.message_handler(IsAdmin(), state="here_ref_percent")
async def settings_ref_per_set(message: Message, state: FSMContext):
    user_id = message.from_user.id

    async with state.proxy() as data:
        lvl = data['cache_ref_lvl_to_edit_percent']

    await state.finish()

    if not message.text.isdigit():
        return await message.answer("<b>❌ Введите число!</b>")

    if lvl == "1":
        update_settings(ref_percent_1=int(message.text))
    elif lvl == "2":
        update_settings(ref_percent_2=int(message.text))
    elif lvl == "3":
        update_settings(ref_percent_3=int(message.text))

    await send_admins(f"<b>❗ Администратор  @{message.from_user.username} изменил процент для {lvl} реферального уровня на: \n{message.text}</b>", True)
    await message.answer(f"<b>✅ Готово! Процент для {lvl} реферального уровня изменен!</b>")


@dp.message_handler(IsAdmin(), state="here_support")
@dp.message_handler(IsAdmin(), text="-", state="here_support")
async def settings_sup_set(message: Message, state: FSMContext):
    await state.finish()

    if message.text.startswith("https://t.me/") or message.text == "-":
        update_settings(support=message.text)
        await send_admins(
            f"<b>❗ Администратор  @{message.from_user.username} изменил Тех. Поддержку на: \n{message.text}</b>", True)
        await message.answer("<b>✅ Готово! Тех. Поддержка была изменена!</b>")
    else:
        await message.answer("<b>❌ Введите ссылку! (https://t.me/юзернейм)</b> ")



@dp.message_handler(IsAdmin(), state="here_chat")
@dp.message_handler(IsAdmin(), text="-", state="here_chat")
async def settings_chat_set(message: Message, state: FSMContext):
    await state.finish()

    if message.text.startswith("https://t.me/") or message.text == "-":
        update_settings(chat=message.text)
        await send_admins(
            f"<b>❗ Администратор  @{message.from_user.username} изменил Чат на: \n{message.text}</b>", True
        )
        await message.answer("<b>✅ Готово! Чат был изменен!</b>")
    else:
        await message.answer("<b>❌ Введите ссылку! (https://t.me/название_чата)</b>")




@dp.message_handler(IsAdmin(), state="here_news")
@dp.message_handler(IsAdmin(), text="-", state="here_news")
async def settings_news_set(message: Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id

    if message.text.startswith("https://t.me/") or message.text == "-":
        update_settings(news=message.text)
        await send_admins(
            f"<b>❗ Администратор  @{message.from_user.username} изменил Новостной канал на: \n{message.text}</b>", True
        )
        await message.answer("<b>✅ Готово! Новостной канал был изменен!</b>")
    else:
        await message.answer("<b>❌ Введите ссылку! (https://t.me/название_канала)</b>")



@dp.callback_query_handler(IsAdmin(), text="stats")
async def stats_open(call: CallbackQuery, state: FSMContext):
    await state.finish()

    show_refill_amount_all, show_refill_amount_day, show_refill_amount_week = 0, 0, 0
    show_refill_count_all, show_refill_count_day, show_refill_count_week = 0, 0, 0
    show_profit_amount_all, show_profit_amount_day, show_profit_amount_week = 0, 0, 0
    show_profit_count_all, show_profit_count_day, show_profit_count_week = 0, 0, 0
    show_users_all, show_users_day, show_users_week, show_users_money = 0, 0, 0, 0

    get_purchases = all_purchases()
    get_refill = all_refills()
    get_users = all_users()

    for purchase in get_purchases:
        show_profit_amount_all += purchase['price']
        show_profit_count_all += purchase['count']

        if purchase['unix'] - get_settings()['profit_day'] >= 0:
            show_profit_amount_day += purchase['price']
            show_profit_count_day += purchase['count']
        if purchase['unix'] - get_settings()['profit_week'] >= 0:
            show_profit_amount_week += purchase['price']
            show_profit_count_week += purchase['count']

    for refill in get_refill:
        show_refill_amount_all += refill['amount']
        show_refill_count_all += 1

        if refill['date_unix'] - get_settings()['profit_day'] >= 0:
            show_refill_amount_day += refill['amount']
            show_refill_count_day += 1
        if refill['date_unix'] - get_settings()['profit_week'] >= 0:
            show_refill_amount_week += refill['amount']
            show_refill_count_week += 1

    for user in get_users:
        show_users_money += user['balance']
        show_users_all += 1

        if user['reg_date_unix'] - get_settings()['profit_day'] >= 0:
            show_users_day += 1
        if user['reg_date_unix'] - get_settings()['profit_week'] >= 0:
            show_users_week += 1

    msg = f"""
<b>📊 Статистика:</b>


<b>👤 Юзеры:</b>

👤 За День: <code>{show_users_day}</code>
👤 За Неделю: <code>{show_users_week}</code>
👤 За Всё время: <code>{show_users_all}</code>

<b>💸 Продажи:</b>

💸 За День: <code>{show_profit_count_day}шт</code> (<code>{show_profit_amount_day} RUB</code>)
💸 За Неделю: <code>{show_profit_count_week}шт</code> (<code>{show_profit_amount_week} RUB</code>)
💸 За Всё время: <code>{show_profit_count_all}шт</code> (<code>{show_profit_amount_all} RUB</code>)

<b>💰 Пополнения:</b>

💰 Пополнений за День: <code>{show_refill_count_day}шт</code> (<code>{show_refill_amount_day}₽</code>)
💰 Пополнений за Неделю: <code>{show_refill_count_week}шт</code> (<code>{show_refill_amount_week}₽</code>)
💰 Пополнений за Всё время: <code>{show_refill_count_all}шт</code> (<code>{show_refill_amount_all}₽</code>)

<b>⚙️ Админы: </b>

⚙️ Всего админов: <code>{len(get_admins())} чел</code>
⚙️ Админы: \n
"""
    for admin in get_admins():
        user = get_user(id=admin)
        msg += f"@{user['user_name']}\n "

    await call.message.edit_text(ots(msg), reply_markup=back_sett())


@dp.callback_query_handler(text='extra_settings', state="*")
async def extra_settings(call: CallbackQuery, state: FSMContext):
    await state.finish()

    await call.message.edit_text(f"<b>❗ Выберите действие:</b>", reply_markup=extra_settings_inl())

@dp.callback_query_handler(text="promo_create", state="*")
async def promo_create(call: CallbackQuery, state: FSMContext):
    await state.finish()

    await call.message.edit_text(f"<b>❗ Введите название промокода</b>", reply_markup=extra_back())
    await state.set_state(f"here_name_promo")

@dp.message_handler(state='here_name_promo')
async def here_name_promo(msg: Message, state: FSMContext):
    
    name = msg.text

    await msg.answer(f"<b>❗ Введите кол-во использований</b>")
    await state.update_data(cache_name_for_add_promo=name)
    await state.set_state(f"here_uses_promo")

@dp.message_handler(state="here_uses_promo")
async def here_uses_promo(msg: Message, state: FSMContext):
    if msg.text.isdigit():
        await msg.answer("<b>❗ Введите скидку в рублях (Они зачисляться после ввода промокода)</b>")
        await state.update_data(cache_uses_for_add_promo=int(msg.text))
        await state.set_state("here_discount_promo")
    else:
        await msg.answer("<b>❗ Кол-во использований должно быть числом!</b>")

@dp.message_handler(state="here_discount_promo")
async def here_discount_promo(msg: Message, state: FSMContext):
    if msg.text.isdigit():
        async with state.proxy() as data:
            name = data['cache_name_for_add_promo']
            uses = data['cache_uses_for_add_promo']
        await state.finish()
        discount = int(msg.text)

        create_coupon(name, uses, discount)
        await msg.answer(f"<b>✅ Промокод <code>{name}</code> с кол-вом использований <code>{uses}</code> и скидкой <code>{discount} RUB</code> был создан!</b>")
        await send_admins(
            f"<b>❗ Администратор  @{msg.from_user.username} создал Промокод <code>{name}</code> с кол-вом использований <code>{uses}</code> и скидкой <code>{discount} RUB</code></b>", True
        )
    else:
        await msg.answer("<b>❗ Скидка должна быть числом!</b>")

@dp.callback_query_handler(text="promo_delete", state="*")
async def promo_create(call: CallbackQuery, state: FSMContext):
    await state.finish()

    await call.message.edit_text(f"<b>❗ Введите название промокода</b>", reply_markup=extra_back())
    await state.set_state(f"here_name_for_delete_promo")

@dp.message_handler(state="here_name_for_delete_promo")
async def promo_delete(msg: Message, state: FSMContext):

    try:
        delete_coupon(msg.text)
        await state.finish()
        await msg.answer(f"<b>✅ Промокод <code>{msg.text}</code> был удален</b>")
        await send_admins(
            f"<b>❗ Администратор  @{msg.from_user.username} удалил Промокод <code>{msg.text}</code></b>", True
        )
    except:
        await msg.answer(f"<b>❌ Промокода <code>{msg.text}</code> не существует!</b>")


@dp.callback_query_handler(text_startswith="ref_lvl_edit:", state="*")
async def ref_lvl_edit(call: CallbackQuery, state: FSMContext):
    await state.finish()

    lvl = call.data.split(":")[1]

    await call.message.edit_text(f"<b>❗ Введите кол-во рефералов для {lvl} уровня</b>", reply_markup=extra_back())
    await state.update_data(cache_lvl_for_edit_lvls=lvl)
    await state.set_state("here_count_lvl_ref")

@dp.message_handler(state="here_count_lvl_ref")
async def here_count_lvl_ref(msg: Message, state: FSMContext):
    if msg.text.isdigit():
        async with state.proxy() as data:
            lvl = data['cache_lvl_for_edit_lvls']
        count = int(msg.text)

        if lvl == "1":
            update_settings(ref_lvl_1=count)
        elif lvl == "2":
            update_settings(ref_lvl_2=count)
        else:
            update_settings(ref_lvl_3=count)

        await msg.answer(f"<b>✅ Вы изменили кол-во рефералов для <code>{lvl}</code> уровня на <code>{count} чел</code></b>")
        await send_admins(
            f"<b>❗ Администратор  @{msg.from_user.username} изменил кол-во рефералов для <code>{lvl}</code> уровня на <code>{count} чел</code></b>", True
        )

@dp.callback_query_handler(text_startswith="user:", state="*")
async def user_balance_add(call: CallbackQuery, state: FSMContext):
    await state.finish()
    
    action = call.data.split(":")[1]
    user_id = call.data.split(":")[2]
    user = get_user(id=user_id)

    if action == "balance_add":
        await call.message.edit_text(f"<b>💰 Введите сумму, которую хотите выдать:</b>")
        await state.update_data(cache_user_id_for_bal_add=user_id)
        await state.set_state("here_amount_to_add")
    elif action == "balance_edit":
        await call.message.edit_text(f"<b>💰 Введите сумму, на которую хотите изменить:</b>")
        await state.set_state("here_amount_to_edit")
        await state.update_data(cache_user_id_for_bal_edit=user_id)
    elif action == "is_ban_ban":
        update_user(id=user_id, is_ban="True")
        await call.message.edit_text(f"<b>✅ Вы забанили пользователя @{user['user_name']}</b>")
        user_name = user['user_name']
        user_id = user['id']
        balance = user['balance']
        total_refill = user['total_refill']
        reg_date = user['reg_date']
        ref_count = user['ref_count']

        msgg = f"""
        <b>👤 Профиль:
        💎 Юзер: @{user_name}
        🆔 ID: <code>{user_id}</code>
        💰 Баланс: <code>{balance} RUB</code>
        💵 Всего пополнено: <code>{total_refill} RUB</code>
        📌 Дата регистрации: <code>{reg_date}</code>
        👥 Рефералов: <code>{ref_count} чел</code></b>"""

        await call.message.answer(msgg, reply_markup=profile_adm_inl(user_id))
    elif action == "is_ban_unban":
        update_user(id=user_id, is_ban="False")
        await call.message.edit_text(f"<b>✅ Вы разбанили пользователя @{user['user_name']}</b>")
        user_name = user['user_name']
        user_id = user['id']
        balance = user['balance']
        total_refill = user['total_refill']
        reg_date = user['reg_date']
        ref_count = user['ref_count']

        msgg = f"""
                <b>👤 Профиль:
                💎 Юзер: @{user_name}
                🆔 ID: <code>{user_id}</code>
                💰 Баланс: <code>{balance} RUB</code>
                💵 Всего пополнено: <code>{total_refill} RUB</code>
                📌 Дата регистрации: <code>{reg_date}</code>
                👥 Рефералов: <code>{ref_count} чел</code></b>"""

        await call.message.answer(msgg, reply_markup=profile_adm_inl(user_id))
    elif action == "sms":
        await call.message.edit_text(f"<b>❗ Введите сообщение, которое хотите отправить пользователю</b>")
        await state.update_data(cache_user_id_for_send_msg=user_id)
        await state.set_state("here_msg_to_send")

@dp.message_handler(state="here_amount_to_add")
async def here_amount_to_add(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = data['cache_user_id_for_bal_add']

    if msg.text.isdigit() or msg.text.replace(".", "", 1).isdigit():
        await state.finish()
        user = get_user(id=user_id)
        update_user(id=user_id, balance=float(user['balance']) + float(msg.text))
        await bot.send_message(chat_id=user_id, text=f"<b>💰 Администратор выдал вам <code>{msg.text} RUB</code></b>")
        user_name = user['user_name']
        user_id = user['id']
        balance = user['balance']
        total_refill = user['total_refill']
        reg_date = user['reg_date']
        ref_count = user['ref_count']

        msgg = f"""
<b>👤 Профиль:
💎 Юзер: @{user_name}
🆔 ID: <code>{user_id}</code>
💰 Баланс: <code>{float(balance) + float(msg.text)} RUB</code>
💵 Всего пополнено: <code>{total_refill} RUB</code>
📌 Дата регистрации: <code>{reg_date}</code>
👥 Рефералов: <code>{ref_count} чел</code></b>"""

        await msg.answer(msgg, reply_markup=profile_adm_inl(user_id))
    else:
        await msg.answer("<b>❗ Сумма должна быть числом!</b>")

@dp.message_handler(state="here_amount_to_edit")
async def here_amount_to_add(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = data['cache_user_id_for_bal_edit']

    if msg.text.isdigit() or msg.text.replace(".", "", 1).isdigit():
        await state.finish()
        user = get_user(id=user_id)
        update_user(id=user_id, balance=round(float(msg.text), 2))
        await bot.send_message(chat_id=user_id, text=f"<b>💰 Администратор изменил вам баланс на <code>{msg.text} RUB</code></b>")
        user_name = user['user_name']
        user_id = user['id']
        balance = user['balance']
        total_refill = user['total_refill']
        reg_date = user['reg_date']
        ref_count = user['ref_count']

        msgg = f"""
<b>👤 Профиль:
💎 Юзер: @{user_name}
🆔 ID: <code>{user_id}</code>
💰 Баланс: <code>{float(msg.text)} RUB</code>
💵 Всего пополнено: <code>{total_refill} RUB</code>
📌 Дата регистрации: <code>{reg_date}</code>
👥 Рефералов: <code>{ref_count} чел</code></b>"""

        await msg.answer(msgg, reply_markup=profile_adm_inl(user_id))
    else:
        await msg.answer("<b>❗ Сумма должна быть числом!</b>")


@dp.message_handler(state="here_msg_to_send")
async def here_msg_to_send(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = data['cache_user_id_for_send_msg']

    await state.finish()

    await bot.send_message(chat_id=user_id, text=f"<b>⭐ Вам пришло сообщение от администратора: \n{msg.text}</b>")
    await msg.answer(f"<b>⭐ Вы отправили сообщение пользователю @{get_user(id=user_id)['user_name']}</b>")
    user = get_user(id=user_id)
    user_name = user['user_name']
    user_id = user['id']
    balance = user['balance']
    total_refill = user['total_refill']
    reg_date = user['reg_date']
    ref_count = user['ref_count']

    msgg = f"""
<b>👤 Профиль:
💎 Юзер: @{user_name}
🆔 ID: <code>{user_id}</code>
💰 Баланс: <code>{balance} RUB</code>
💵 Всего пополнено: <code>{total_refill} RUB</code>
📌 Дата регистрации: <code>{reg_date}</code>
👥 Рефералов: <code>{ref_count} чел</code></b>"""

    await msg.answer(msgg, reply_markup=profile_adm_inl(user_id))
