# - *- coding: utf- 8 - *-
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Update
from tgbot.services.sqlite import *
from tgbot.utils.utils_functions import send_admins
from tgbot.data.loader import bot

class ExistsUserMiddleware(BaseMiddleware):

    def __init__(self):
        super(ExistsUserMiddleware, self).__init__()

    async def on_process_update(self, update: Update, data: dict):
        user = update

        if "message" in update:
            user = update.message.from_user
        elif "callback_query" in update:
            user = update.callback_query.from_user

        if user is not None:
            if not user.is_bot:
                self.id = user.id
                self.user_name = user.username
                self.first_name = user.first_name
                self.bot = await bot.get_me()

                if self.user_name is None:
                    self.user_name = ""

                if get_user(id=self.id) is None:
                    register_user(id=self.id, user_name=self.user_name, first_name=self.first_name)
                    if get_settings()['is_notify'] == "True":
                        await send_admins(f"<b>💎 Зарегистрирован новый пользователь @{self.user_name}</b>", False)
                else:
                    if get_user(id=self.id)['is_ban'] == "" or get_user(id=self.id)['is_ban'] is None:
                        update_user(id=self.id, is_ban="False")
                    if get_user(id=self.id)['user_name'] != self.user_name:
                        update_user(self.id, user_name=self.user_name)
                    if get_user(id=self.id)['first_name'] != self.first_name:
                        update_user(self.id, first_name=self.first_name)
            
                    if len(self.user_name) >= 1:
                        if self.user_name != get_user(id=self.id)['user_name']:
                            update_user(id=self.id, user_name=self.user_name)
                    else:
                        update_user(id=self.id, user_name="")