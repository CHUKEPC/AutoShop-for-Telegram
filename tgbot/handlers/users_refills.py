# - *- coding: utf- 8 - *-
import random

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from tgbot.services.crystal import CrystalPay
from tgbot.services.lolz import Lolz
from tgbot.services.lava import Lava
from tgbot.services.yoomoney_api import YooMoney
from tgbot.services.qiwi import Qiwi
from tgbot.utils.utils_functions import send_admins, get_unix
from tgbot.services.sqlite import get_user, update_user, add_refill, get_settings
from design import refill_success_text, yes_refill_ref, refill_text, refill_amount_text, min_amount, max_amount, \
refill_gen_text, min_max_amount, no_int_amount, refill_check_no
from tgbot.keyboards.inline_user import refill_inl, refill_open_inl
from tgbot.data.loader import dp, bot
from tgbot.data import config

async def success_refill(call: CallbackQuery, way, amount, id, user_id):
    user = get_user(id=user_id)
    msg = f"💰 Произошло пополнение баланса! \n" \
          f"👤 Пользователь: <b>@{user['user_name']}</b> | <a href='tg://user?id={user['id']}'>{user['first_name']}</a> | <code>{user['id']}</code>\n" \
          f"💵 Сумма пополнения: <code>{amount} RUB</code>\n" \
          f"🧾 Чек: <code>{id}</code> \n" \
          f"⚙️ Способ: <code>{way}</code>"
    await send_admins(msg, True)
    update_user(id=user_id, balance=int(user['balance']) + int(amount), total_refill=int(user['total_refill']) + int(amount), count_refills=int(user['count_refills']) + 1)
    add_refill(amount, way, user_id, user['user_name'], user['first_name'], comment=id)
    await call.message.edit_text(refill_success_text(way, amount, id))

    if get_settings()['is_ref'] == "False":
        pass
    elif get_settings()['is_ref'] == "True":
        if user['ref_id'] is None:
            pass
        else:
            reffer = get_user(id=user['ref_id'])

            if reffer['ref_lvl'] == 1:
                ref_percent = get_settings()['ref_percent_1']
            elif reffer['ref_lvl'] == 2:
                ref_percent = get_settings()['ref_percent_2']
            elif reffer['ref_lvl'] == 3:
                ref_percent = get_settings()['ref_percent_3']

            ref_amount = int(amount) / 100 * int(ref_percent)
            reffer_id = user['ref_id']
            reffer_balance = get_user(id=reffer_id)['balance']
            ref_earn = reffer_balance = get_user(id=reffer_id)['ref_earn']
            add_balance = round(reffer_balance + round(ref_amount, 1), 2)
            name = f"<a href='tg://user?id={user['id']}'>{user['user_name']}</a>"
            update_user(reffer_id, balance=add_balance, ref_earn=ref_earn + round(ref_amount, 1))
            await bot.send_message(reffer_id, yes_refill_ref.format(name=name, amount=amount, ref_amount=round(ref_amount, 1)))


@dp.callback_query_handler(text="refill", state="*")
async def refill_open(call: CallbackQuery, state: FSMContext):
    await state.finish()

    await call.message.delete()
    await call.message.answer(refill_text, reply_markup=refill_inl())

@dp.callback_query_handler(text_startswith="refill:", state="*")
async def refill_(call: CallbackQuery, state: FSMContext):
    await state.finish()

    way = call.data.split(":")[1]
    await state.update_data(here_way=way)
    await state.set_state("here_amount_refill")
    await call.message.answer(refill_amount_text)


@dp.message_handler(state="here_amount_refill")
async def refill_pay(message: Message, state: FSMContext):
    amount = message.text
    way = (await state.get_data())['here_way']
    bota = await bot.get_me()
    bot_name = bota.username
    user_name = get_user(id=message.from_user.id)['user_name']

    if amount.isdigit():
        pay_amount = int(amount)
        if min_amount <= pay_amount <= max_amount:
            if way == "crystal":
                way = "CrystalPay"
                crystal = CrystalPay(config.crystal_Cassa, config.crystal_Token)
                crys = await crystal.generate_pay_link(amount=pay_amount)
                link = crys['url']
                id = crys['id']
            elif way == "qiwi":
                way = "Qiwi"
                qiwi = Qiwi(config.qiwi_token, config.qiwi_login, config.qiwi_secret)
                bill_id = get_unix(True)
                bill = await qiwi.create_bill(amount=pay_amount, comment=bill_id)
                id = bill['billId']
                link = bill['payUrl']
            elif way == "lolz":
                way = "Lolz"
                lzt = Lolz(access_token=config.lolz_token)
                comment = lzt.get_random_string()
                link = lzt.get_link(amount=pay_amount, comment=comment)
                id = comment
            elif way == "lava":
                way = "Lava"
                lava = Lava(shop_id=config.lava_project_id, secret_token=config.lava_secret_key)
                invoice = await lava.create_invoice(amount=float(pay_amount), comment=f"Пополнение аккаунта {user_name} на сумму {pay_amount}₽ в боте {bot_name}", success_url=f"https://t.me/{bot_name}")
                link = invoice['data']['url']
                id = invoice['data']['id']
            elif way == "yoomoney":
                way = "ЮMoney"
                order = random.randint(1111111,9999999)
                yoo = YooMoney(token=config.yoomoney_token, number=config.yoomoney_number)
                form = yoo.create_yoomoney_link(amount=pay_amount, comment=order)
                link = form['link']
                id = form['comment']
            await message.answer(refill_gen_text(way=way, amount=pay_amount, id=id), reply_markup=refill_open_inl(way=way, amount=pay_amount, link=link, id=id))
            await state.finish()
        else:
            await message.answer(min_max_amount)
    else:
        await message.answer(no_int_amount)

@dp.callback_query_handler(text_startswith="check_opl:", state='*')
async def check_refill(call: CallbackQuery, state: FSMContext):
    
    data = call.data.split(':')
    amount = data[2]
    way = data[1]
    id = data[3]
    bota = await bot.get_me()
    bot_name = bota.username
    user_name = get_user(id=call.from_user.id)['user_name']

    if way == "CrystalPay":
        crystal = CrystalPay(config.crystal_Cassa, config.crystal_Token)
        status = await crystal.get_pay_status(invoice_id=id)
        if status:
            await success_refill(call, way, int(amount), id, call.from_user.id)
        else:
            await call.answer(refill_check_no, True)
    elif way == "Qiwi":
        qiwi = Qiwi(config.qiwi_token, config.qiwi_login, config.qiwi_secret)
        status = await qiwi.check_bill(bill_id=id)
        print(status)
        if status:
            await success_refill(call, way, amount, id, call.from_user.id)
        else:
            await call.answer(refill_check_no, True)
    elif way == "Lava":
        lava = Lava(shop_id=config.lava_project_id, secret_token=config.lava_secret_key)
        status = await lava.status_invoice(invoice_id=id)
        if status:
            await success_refill(call, way, amount, id, call.from_user.id)
        else:
            await call.answer(refill_check_no, True)
    elif way == "Lolz":
        lzt = Lolz(config.lolz_token)
        status = await lzt.check_payment(amount=int(amount), comment=id)
        if status == True:
            await success_refill(call, way, amount, id, call.from_user.id)
        else:
            if status == False:
                await call.answer(refill_check_no, True)
            else:
                await call.answer(status, True)
    elif way == "ЮMoney":
        yoo = YooMoney(token=config.yoomoney_token, number=config.yoomoney_number)
        status = yoo.check_yoomoney_payment(comment=id)
        if status:
            await success_refill(call, way, amount, id, call.from_user.id)
        else:
            await call.answer(refill_check_no, True)