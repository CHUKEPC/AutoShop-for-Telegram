# - *- coding: utf- 8 - *-
import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from tgbot.services.sqlite import get_user
from design import no_cats, available_cats, no_products, current_cat, current_pod_cat, open_pos_text, here_count_products, \
choose_buy_product, no_balance, no_product, no_num_count, choose_buy_products, gen_products, yes_buy_items, otmena_buy, edit_prod
from tgbot.keyboards.inline_user import back_to_user_menu, open_products, open_positions, open_pod_cat_positions, \
pos_buy_inl, choose_buy_items
from tgbot.services.sqlite import get_all_categories, get_positions, get_category, get_pod_category, get_position, \
get_items, buy_item, update_user, add_purchase
from tgbot.data.loader import dp, bot
from tgbot.utils.utils_functions import split_messages, get_date, get_unix, send_admins
from contextlib import suppress
from aiogram.utils.exceptions import MessageCantBeDeleted

@dp.callback_query_handler(text="products:open", state="*")
async def open_products_users(call: CallbackQuery, state: FSMContext):
    await state.finish()

    if len(get_all_categories()) < 1:
        await call.message.delete()
        await call.message.answer(no_cats, reply_markup=back_to_user_menu())
    else:
        await call.message.delete()
        await call.message.answer(available_cats, reply_markup=open_products())

@dp.callback_query_handler(text_startswith="open_category:", state="*")
async def open_cat_for_buy(call: CallbackQuery, state: FSMContext):
    await state.finish()

    cat_id = call.data.split(":")[1]

    if len(get_positions(cat_id)) < 1:
        await call.message.delete()
        await call.message.answer(no_products, reply_markup=back_to_user_menu())
    else:
        await call.message.delete()
        await call.message.answer(current_cat.format(name=get_category(cat_id)['name']), reply_markup=open_positions(cat_id))

@dp.callback_query_handler(text_startswith="open_pod_cat:", state="*")
async def open_pod_cat(call: CallbackQuery, state: FSMContext):
    await state.finish()

    pod_cat_id = call.data.split(":")[1]

    if len(get_positions(pod_cat_id=pod_cat_id)) < 1:
        await call.message.delete()
        await call.message.answer(no_products)
    else:
        await call.message.delete()
        await call.message.answer(current_pod_cat.format(name=get_pod_category(pod_cat_id)['name']), reply_markup=open_pod_cat_positions(pod_cat_id))

@dp.callback_query_handler(text_startswith="open_pos:", state="*")
async def open_pos(call: CallbackQuery, state: FSMContext):
    await state.finish()

    pos_id = call.data.split(":")[1]
    pos = get_position(pos_id)
    cat_id = pos['category_id']
    cat = get_category(cat_id)
    items = f"{len(get_items(position_id=pos_id))}шт."
    if pos['infinity'] == "+":
        items = "Безлимит"

    msg = open_pos_text.format(cat_name=cat['name'], pos_name=pos['name'], price=pos['price'], items=items, desc=pos['description'])

    if pos['photo'] is None or pos['photo'] == "-":
        await call.message.edit_text(msg, reply_markup=pos_buy_inl(pos_id))
    else:
        await call.message.delete()
        await bot.send_photo(chat_id=call.from_user.id, photo=pos['photo'], caption=msg, reply_markup=pos_buy_inl(pos_id))


@dp.callback_query_handler(text_startswith='buy_pos:', state="*")
async def pos_buy(call: CallbackQuery, state: FSMContext):
    await state.finish()

    pos_id = call.data.split(":")[1]
    pos = get_position(pos_id)
    items = get_items(position_id=pos_id)
    user = get_user(id=call.from_user.id)

    await state.update_data(cache_pos_id_for_buy=pos_id)

    if len(items) > 1:
            await call.message.delete()
            await call.message.answer(here_count_products)
            await state.set_state("here_amount_to_buy")

    elif len(items) == 1:
        if user['balance'] >= pos['price']:
            await call.message.delete()
            await call.message.answer(choose_buy_product.format(name=pos['name']), reply_markup=choose_buy_items(pos_id, 1))
        else:
            await call.answer(no_balance)
    else:
        await call.answer(no_product, True)

@dp.message_handler(state="here_amount_to_buy")
async def here_amount_to_buy(msg: Message, state: FSMContext):

    amount = msg.text
    user = get_user(id=msg.from_user.id)
    async with state.proxy() as data:
        pos_id = data['cache_pos_id_for_buy']

    pos = get_position(pos_id)

    if not amount.isdigit():
        await msg.delete()
        await msg.answer(no_num_count)
    else:
        if user['balance'] >= pos['price']:
            await state.finish()
            await msg.delete()
            await msg.answer(choose_buy_products.format(name=pos['name'], amount=amount), reply_markup=choose_buy_items(pos_id, amount))
        else:
            await msg.reply(no_balance)

# Подтверждение покупки товара
@dp.callback_query_handler(text_startswith="buy_items:", state="*")
async def user_purchase_confirm(call: CallbackQuery, state: FSMContext):
    action = call.data.split(":")[1]
    pos_id = call.data.split(":")[2]
    amount = call.data.split(":")[3]
    amount = int(amount)

    if action == "yes":
        await call.message.edit_text(gen_products)

        pos = get_position(pos_id)
        items = get_items(position_id=pos_id)
        user = get_user(id=call.from_user.id)

        amount_pay = (int(pos['price'] * amount))

        if 1 <= int(amount) <= len(items):
            if int(user['balance']) >= amount_pay:
                infinity = pos['infinity']
                save_items, send_count, split_len = buy_item(items, amount, infinity)

                if amount != send_count:
                    amount_pay = (int(pos['price'] * send_count))
                    amount = send_count

                receipt = get_unix()
                buy_time = get_date()

                with suppress(MessageCantBeDeleted):
                    await call.message.delete()
                if split_len == 0:
                    await call.message.answer("\n\n".join(save_items), parse_mode="None")
                else:
                    for item in split_messages(save_items, split_len):
                        await call.message.answer("\n\n".join(item), parse_mode="None")
                        await asyncio.sleep(0.3)
                tovs = "\n".join(save_items)
                msg = f"""
💰 Новая покупка!
👤 Пользователь: <b>@{user['user_name']}</b> | <a href='tg://user?id={user['id']}'>{user['first_name']}</a> | <code>{user['id']}</code>
💵 Сумма: <code>{amount_pay} RUB</code>
🧾 Чек: <code>{receipt}</code>
⚙️ Товар: <code>{pos['name']}</code>
🎲 Содержимое товара:
{tovs}"""

                await send_admins(msg, True)
                update_user(user['id'], balance=user['balance'] - amount_pay)
                add_purchase(user['id'], user['first_name'], user['user_name'], receipt, amount, amount_pay, pos['id'], pos['name'], "\n".join(save_items), buy_time, receipt)
                msg = yes_buy_items.format(receipt=receipt, name=pos['name'], amount=amount, amount_pay=amount_pay, buy_time=buy_time)
                await call.message.answer(msg)
            else:
                await call.answer(no_balance)
        else:
            await call.message.answer(edit_prod)
    else:
        await call.message.edit_text(otmena_buy)