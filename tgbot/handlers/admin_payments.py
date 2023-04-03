# - *- coding: utf- 8 - *-
import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from tgbot.services.sqlite import get_payments, update_payments
from tgbot.services.crystal import CrystalPay
from tgbot.services.lolz import Lolz
from tgbot.services.lava import Lava
from tgbot.services.yoomoney_api import YooMoney
from tgbot.services.qiwi import Qiwi
from design import qiwi_text, yoomoney_text, lava_text, lzt_text, crystalPay_text
from tgbot.utils.utils_functions import ots
from tgbot.keyboards.inline_admin import payments_settings_info, payments_settings, payments_back
from tgbot.filters.is_admin import IsAdmin
from tgbot.data.loader import dp
from tgbot.data import config

@dp.callback_query_handler(IsAdmin(), text='payments', state="*")
async def payments_settings_choose(call: CallbackQuery, state: FSMContext):
    await state.finish()

    await call.message.edit_text("<b>⚙️ Выберите способ оплаты</b>", reply_markup=payments_settings())

@dp.callback_query_handler(IsAdmin(), text_startswith="payments:", state="*")
async def payments_info(call: CallbackQuery, state: FSMContext):
    await state.finish()
    way = call.data.split(":")[1]

    def pay_info(way, status):
        if status == "True":
            status = "✅ Включен"
        elif status == "False":
            status = "❌ Выключен"

        msg = f"""
<b>{way}

Статус: <code>{status}</code></b>        
"""
        return ots(msg)

    if way == "qiwi":
        ways = qiwi_text
        status = get_payments()['pay_qiwi']

        await call.message.edit_text(pay_info(ways, status), reply_markup=payments_settings_info(way, status))
    elif way == "yoomoney":
        ways = yoomoney_text
        status = get_payments()['pay_yoomoney']

        await call.message.edit_text(pay_info(ways, status), reply_markup=payments_settings_info(way, status))
    elif way == "lava":
        ways = lava_text
        status = get_payments()['pay_lava']

        await call.message.edit_text(pay_info(ways, status), reply_markup=payments_settings_info(way, status))
    elif way == "lzt":
        ways = lzt_text
        status = get_payments()['pay_lolz']

        await call.message.edit_text(pay_info(ways, status), reply_markup=payments_settings_info(way, status))
    elif way == "crystalPay":
        ways = crystalPay_text
        status = get_payments()['pay_crystal']

        await call.message.edit_text(pay_info(ways, status), reply_markup=payments_settings_info(way, status))

@dp.callback_query_handler(IsAdmin(), text_startswith="payments_on_off:", state="*")
async def off_payments(call: CallbackQuery, state: FSMContext):

    way = call.data.split(":")[1]
    action = call.data.split(":")[2]

    def pay_info(way, status):
        if status == "True":
            status = "✅ Включен"
        elif status == "False":
            status = "❌ Выключен"

        msg = f"""
    <b>{way}

    Статус: <code>{status}</code></b>        
    """
        return ots(msg)

    if way == "qiwi":
        ways = qiwi_text

        if action == "off":
            update_payments(pay_qiwi="False")
        else:
            update_payments(pay_qiwi="True")

        status = get_payments()['pay_qiwi']

        await call.message.edit_text(pay_info(ways, status), reply_markup=payments_settings_info(way, status))
    elif way == "yoomoney":
        ways = yoomoney_text

        if action == "off":
            update_payments(pay_yoomoney="False")
        else:
            update_payments(pay_yoomoney="True")

        status = get_payments()['pay_yoomoney']

        await call.message.edit_text(pay_info(ways, status), reply_markup=payments_settings_info(way, status))
    elif way == "lava":
        ways = lava_text

        if action == "off":
            update_payments(pay_lava="False")
        else:
            update_payments(pay_lava="True")

        status = get_payments()['pay_lava']

        await call.message.edit_text(pay_info(ways, status), reply_markup=payments_settings_info(way, status))
    elif way == "lzt":
        ways = lzt_text

        if action == "off":
            update_payments(pay_lolz="False")
        else:
            update_payments(pay_lolz="True")

        status = get_payments()['pay_lolz']

        await call.message.edit_text(pay_info(ways, status), reply_markup=payments_settings_info(way, status))
    elif way == "crystalPay":
        ways = crystalPay_text

        if action == "off":
            update_payments(pay_crystal="False")
        else:
            update_payments(pay_crystal="True")

        status = get_payments()['pay_crystal']

        await call.message.edit_text(pay_info(ways, status), reply_markup=payments_settings_info(way, status))

@dp.callback_query_handler(IsAdmin(), text_startswith="payments_balance:", state="*")
async def payments_balance_call(call: CallbackQuery, state: FSMContext):
    await state.finish()

    way = call.data.split(":")[1]

    if way == "qiwi":
        ways = qiwi_text
        qiwi = Qiwi(config.qiwi_token, config.qiwi_login, config.qiwi_secret)
        balance = await qiwi.get_balance(config.qiwi_login)

        await call.message.edit_text(f"{ways} \n\n{balance}", reply_markup=payments_back())

    elif way == "yoomoney":
        ways = yoomoney_text
        yoo = YooMoney(config.yoomoney_token, config.yoomoney_number)
        balance = yoo.get_balance()

        await call.message.edit_text(f"{ways} \n\n<code>{balance} RUB</code>", reply_markup=payments_back())

    elif way == "crystalPay":
        ways = crystalPay_text
        crystal = CrystalPay(config.crystal_Cassa, config.crystal_Token)
        balance = await crystal.get_balance()

        await call.message.edit_text(f"{ways} \n\n{balance}", reply_markup=payments_back())

    elif way == "lzt":
        ways = lzt_text
        lzt = Lolz(config.lolz_token)
        await asyncio.sleep(3)
        data = await lzt.get_user()
        balance = data['balance']
        hold = data['hold']

        await call.message.edit_text(f'{ways} \n\nВаш баланс: <code>{balance+hold} RUB</code> (<code>{hold} RUB</code> в холде)', reply_markup=payments_back())

    elif way == "lava":
        ways = lava_text
        lava = Lava(config.lava_project_id, config.lava_secret_key)
        balance = await lava.get_balance()

        await call.message.edit_text(f"{ways} \n\nВаш баланс: <code>{balance['data']['balance']+balance['data']['freeze_balance']} RUB</code> (<code>{balance['data']['freeze_balance']} RUB</code> заморожено)", reply_markup=payments_back())


@dp.callback_query_handler(IsAdmin(), text_startswith="payments_info:", state="*")
async def payments_info_open(call: CallbackQuery, state: FSMContext):
    await state.finish()

    way = call.data.split(":")[1]

    if way == "qiwi":
        ways = qiwi_text

        await call.message.edit_text(f"{ways} \n\nНомер: <code>{config.qiwi_login}</code> \nТокен: <code>{config.qiwi_token}</code> \nСекретный p2p-ключ: <code>{config.qiwi_secret}</code>", reply_markup=payments_back())

    elif way == "crystalPay":
        ways = crystalPay_text

        await call.message.edit_text(f"{ways} \n\nЛогин кассы: <code>{config.crystal_Cassa}</code> \nСекретный токен 1: <code>{config.crystal_Token}</code>", reply_markup=payments_back())

    elif way == "yoomoney":
        ways = yoomoney_text

        await call.message.edit_text(f"{ways} \n\nТокен: <code>{config.yoomoney_token}</code> \nНомер: <code>{config.yoomoney_number}</code>", reply_markup=payments_back())
    elif way == "lzt":
        ways = lzt_text

        await call.message.edit_text(f"{ways} \n\nТокен: <code>{config.lolz_token}</code> \nНик: <code>{config.lolz_nick}</code> \nID: <code>{config.lolz_id}</code>", reply_markup=payments_back())
    elif way == "lava":
        ways = lava_text

        await call.message.edit_text(f"{ways} \n\nID Проекта: <code>{config.lava_project_id}</code> \nСекретный ключ: <code>{config.lava_secret_key}</code>", reply_markup=payments_back())