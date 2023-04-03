# - *- coding: utf- 8 - *-
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from design import is_ban_text, is_buy_text, is_ref_text, is_refill_text, is_work_text, no_sub, start_photo, start_text, \
yes_reffer, invite_yourself, new_ref_lvl, new_refferal, max_ref_lvl, cur_max_lvl, next_lvl_remain, ref_text, \
last_10_purc, last_purc_text, no_purcs, promo_act, no_coupon, no_uses_coupon, yes_coupon, yes_uses_coupon, no_faq_text, \
yes_support, no_support
from tgbot.keyboards.inline_user import sub, user_menu, back_to_profile, profile_inl, back_to_user_menu, chat_inl, news_inl, faq_inl, support_inll
from tgbot.services.sqlite import get_user, get_settings, update_user, last_purchases, get_activate_coupon, get_coupon_search, \
delete_coupon, update_coupon, add_activ_coupon, activate_coupon
from tgbot.data.loader import dp, bot
from tgbot.utils.other_functions import open_profile, convert_ref
from contextlib import suppress
from tgbot.filters.is_buy import IsBuy
from tgbot.filters.is_ban import IsBan
from tgbot.filters.is_work import IsWork
from tgbot.filters.is_refill import IsRefill
from tgbot.filters.is_sub import IsSub
from aiogram.utils.exceptions import MessageCantBeDeleted

@dp.callback_query_handler(IsBuy(), text="products:open", state="*")
async def is_buy(call: CallbackQuery, state: FSMContext):
    await state.finish()

    await call.answer(is_buy_text, True)

@dp.message_handler(IsBan(), state="*")
async def is_ban(message: Message, state: FSMContext):
    await state.finish()

    await message.answer(is_ban_text)

@dp.callback_query_handler(IsBan(), state="*")
async def is_ban(call: CallbackQuery, state: FSMContext):
    await state.finish()

    await call.answer(is_ban_text)

@dp.message_handler(IsWork(), state="*")
async def is_work(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(is_work_text)

@dp.callback_query_handler(IsWork(), state="*")
async def is_work(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer(is_work_text)

@dp.callback_query_handler(IsRefill(), text="refill", state="*")
async def is_refill(call: CallbackQuery, state: FSMContext):
    await state.finish()

    await call.answer(is_refill_text, True)

@dp.callback_query_handler(IsSub(), state="*")
async def is_subs(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer(no_sub, reply_markup=sub())

@dp.message_handler(IsSub(), state="*")
async def is_subs(msg: Message, state: FSMContext):
    await state.finish()
    await msg.answer(no_sub, reply_markup=sub())

@dp.callback_query_handler(text=['subprov'])
async def sub_prov(call: CallbackQuery, state: FSMContext):
    await state.finish()
    if call.message.chat.type == 'private':
        user = get_user(id=call.from_user.id)
        kb = user_menu(call.from_user.id)
        if start_photo == "":
            await call.message.answer(start_text.format(user_name=user['user_name']), reply_markup=kb)
        else:
            await bot.send_photo(chat_id=call.from_user.id, photo=start_photo,
                                caption=start_text.format(user_name=user['user_name']), reply_markup=kb)

#####################################################################################
#####################################################################################
#####################################################################################
    
@dp.message_handler(commands=['start'], state="*")
async def main_start(message: Message, state: FSMContext):
    await state.finish()
    user = get_user(id=message.from_user.id)
    kb = user_menu(message.from_user.id)

    if get_settings()['is_ref'] == 'True':

        if message.get_args() == "":
            if start_photo == "":
                await message.answer(start_text.format(user_name=user['user_name']), reply_markup=kb)
            else:
                await bot.send_photo(chat_id=message.from_user.id, photo=start_photo,
                                    caption=start_text.format(user_name=user['user_name']), reply_markup=kb)
        else:
            if get_user(id=int(message.get_args())) is None:
                if start_photo == "":
                    await message.answer(start_text.format(user_name=user['user_name']), reply_markup=kb)
                else:
                    await bot.send_photo(chat_id=message.from_user.id, photo=start_photo,
                                        caption=start_text.format(user_name=user['user_name']), reply_markup=kb)
            else:
                if user['ref_id'] is not None:
                    await message.answer(yes_reffer)
                else:
                    reffer = get_user(id=int(message.get_args()))
                    if reffer['id'] == message.from_user.id:
                        await message.answer(invite_yourself)
                    else:
                        user_ref_count = reffer['ref_count']
                        msg = new_refferal.format(user_name=user['user_name'], user_ref_count=user_ref_count + 1, convert_ref=convert_ref(user_ref_count + 1))

                        update_user(message.from_user.id, ref_id=reffer['id'], ref_user_name=reffer['user_name'], ref_first_name=reffer['first_name'])
                        update_user(reffer['id'], ref_count = user_ref_count + 1)

                        await bot.send_message(chat_id=reffer['id'], text=msg)

                        if reffer['ref_count'] + 1 == get_settings()['ref_lvl_1']:
                            remain_refs = get_settings()['ref_lvl_2'] - (reffer['ref_count'] + 1)
                            text = new_ref_lvl.format(new_lvl=1, next_lvl=2, remain_refs=remain_refs, convert_ref=convert_ref(remain_refs))
                            await bot.send_message(chat_id=reffer['id'], text=text)
                            update_user(reffer['id'], ref_lvl=1)
                        elif reffer['ref_count'] + 1 == get_settings()['ref_lvl_2']:
                            remain_refs = get_settings()['ref_lvl_3'] - (reffer['ref_count'] + 1)
                            text = new_ref_lvl.format(new_lvl=2, next_lvl=3, remain_refs=remain_refs, convert_ref=convert_ref(remain_refs))
                            await bot.send_message(chat_id=reffer['id'],
                            text=text)
                            update_user(reffer['id'], ref_lvl=2)
                        elif reffer['ref_count'] + 1 == get_settings()['ref_lvl_3']:
                            await bot.send_message(chat_id=reffer['id'],
                            text=max_ref_lvl)
                            update_user(reffer['id'], ref_lvl=3)

                        if start_photo == "":
                            await message.answer(start_text.format(user_name=user['user_name']), reply_markup=kb)
                        else:
                            await bot.send_photo(chat_id=message.from_user.id, photo=start_photo,
                                                caption=start_text.format(user_name=user['user_name']), reply_markup=kb)
    else:
        if start_photo == "":
            await message.answer(start_text.format(user_name=user['user_name']), reply_markup=kb)
        else:
            await bot.send_photo(chat_id=message.from_user.id, photo=start_photo,
                                 caption=start_text.format(user_name=user['user_name']), reply_markup=kb)

@dp.callback_query_handler(text="ref_system", state='*')
async def ref_systemm(call: CallbackQuery, state: FSMContext):
    await state.finish()
    status = get_settings()['is_ref']
    bott = await bot.get_me()
    bot_name = bott.username
    ref_link = f"<code>https://t.me/{bot_name}?start={call.from_user.id}</code>"
    user = get_user(id=call.from_user.id)
    ref_earn = user['ref_earn']
    ref_count = user['ref_count']
    ref_lvl = user['ref_lvl']
    if ref_lvl == 0:
        lvl = 1
        ref_percent = get_settings()['ref_percent_1']
    if ref_lvl == 1:
        lvl = 2
        ref_percent = get_settings()['ref_percent_1']
    elif ref_lvl == 2:
        lvl = 3
        ref_percent = get_settings()['ref_percent_2']
    elif ref_lvl == 3:
        lvl = 3
        ref_percent = get_settings()['ref_percent_3']

    remain_refs = get_settings()[f'ref_lvl_{lvl}'] - user['ref_count']

    if ref_lvl == 3:
        mss = cur_max_lvl
    else:
        mss = next_lvl_remain.format(remain_refs=remain_refs)

    reffer_name = user['ref_first_name']
    if reffer_name is None:
        reffer = '<code>Никто</code>'
    else:
        reffer = f"<a href='tg://user?id={user['ref_id']}'>{reffer_name}</a>"


    msg = ref_text.format(ref_link=ref_link, ref_percent=ref_percent, reffer=reffer, ref_earn=ref_earn, convert_ref=convert_ref(ref_count), ref_count=ref_count, ref_lvl=ref_lvl, mss=mss)

    if status == "True":
        await call.message.edit_text(msg, reply_markup=back_to_profile())
    else:
        await call.answer(is_ref_text, True)


# Просмотр истории покупок
@dp.callback_query_handler(text="last_purchases", state="*")
async def user_history(call: CallbackQuery, state: FSMContext):
    purchasess = last_purchases(call.from_user.id, 10)

    if len(purchasess) >= 1:
        await call.answer(last_10_purc)
        with suppress(MessageCantBeDeleted):
            await call.message.delete()
            for purchases in purchasess:
                link_items = purchases['item']
            msg = last_purc_text.format(receipt=purchases['receipt'], name=purchases['position_name'], count=purchases['count'], price=purchases['price'], date=purchases['date'], link_items=link_items)

            await call.message.answer(msg)

        msg = open_profile(call)
        await call.message.answer(msg, reply_markup=profile_inl())
    else:
        await call.answer(no_purcs, True)


@dp.callback_query_handler(text_startswith="promo_act", state="*")
async def user_history(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await state.set_state(f"set_coupon")
    await call.message.edit_text(promo_act, reply_markup=back_to_profile())

@dp.message_handler(state="set_coupon")
async def functions_profile_get(message: Message, state: FSMContext):
    await state.finish()
    coupon = message.text


    if get_coupon_search(coupon=coupon) is None:
        await message.answer(no_coupon.format(coupon=coupon))
    else:
        cop = get_coupon_search(coupon=coupon)["coupon"]
        uses = get_coupon_search(coupon=coupon)["uses"]
        discount = get_coupon_search(coupon=coupon)["discount"]
        user_id = message.from_user.id
        user = get_user(id=user_id)
        if uses == 0:
            await message.answer(no_uses_coupon)
            delete_coupon(coupon=coupon)
        elif get_activate_coupon(user_id=user_id) is None:
            update_user(user_id, balance=user['balance'] + discount)
            update_coupon(coupon, uses=int(uses) - 1)
            add_activ_coupon(user_id)
            activate_coupon(user_id=user_id, coupon=coupon)
            await message.answer(yes_coupon.format(discount=discount))
        elif get_activate_coupon(user_id=user_id)["coupon_name"] == cop:
            await message.answer(yes_uses_coupon)


@dp.callback_query_handler(text="back_to_user_menu", state="*")
async def again_start(call: CallbackQuery, state: FSMContext):
    await state.finish()

    user = get_user(id=call.from_user.id)
    kb = user_menu(call.from_user.id)
    if start_photo == "":
        await call.message.edit_text(start_text.format(user_name=user['user_name']), reply_markup=kb)
    else:
        await call.message.delete()
        await bot.send_photo(chat_id=call.from_user.id, photo=start_photo, caption=start_text.format(user_name=user['user_name']), reply_markup=kb)

@dp.callback_query_handler(text="close_text_mail", state='*')
async def close_text_mails(call: CallbackQuery, state: FSMContext):
    await state.finish()

    await call.message.delete()

@dp.callback_query_handler(text="profile", state="*")
async def profile_open(call: CallbackQuery, state: FSMContext):
    await state.finish()

    msg = open_profile(call)

    await call.message.delete()
    await call.message.answer(msg, reply_markup=profile_inl())

@dp.callback_query_handler(text="faq:open", state="*")
async def faq_open(call: CallbackQuery, state: FSMContext):
    await state.finish()

    faq = get_settings()['faq']
    if faq == "None" or faq == "-":
        faq = no_faq_text
    news = get_settings()['news']
    chat = get_settings()['chat']

    if get_settings()['chat'] == "-":
        chat = None

    if get_settings()['news'] == "-":
        news = None

    if news is None and chat is None:
        kb = back_to_user_menu()
    if news is None and chat is not None:
        kb = chat_inl()
    if news is not None and chat is None:
        kb = news_inl()
    if news is not None and chat is not None:
        kb = faq_inl()

    await call.message.delete()
    await call.message.answer(faq, reply_markup=kb)

@dp.callback_query_handler(text="support:open", state="*")
async def faq_open(call: CallbackQuery, state: FSMContext):
    await state.finish()

    get_support = get_settings()['support']
    if get_support == "None" or get_support == "-":
        msg = no_support
    else:
        msg = yes_support

    if get_support == "None" or get_support == "-":
        kb = back_to_user_menu()
    else: 
        kb = support_inll()

    await call.message.delete()
    await call.message.answer(msg, reply_markup=kb)