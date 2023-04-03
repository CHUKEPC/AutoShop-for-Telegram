from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter
from tgbot.services.sqlite import get_settings
from tgbot.data.loader import bot, dp
from tgbot.data import config
from design import no_sub
from tgbot.keyboards.inline_user import sub

# проверка на подписку канала
class IsSub(BoundFilter):
    async def check(self, message: Message):
        issub = get_settings()['is_sub']
        channel_id = config.channel_id
        if channel_id == "":
            return False
        else:
            user_status = await bot.get_chat_member(chat_id=channel_id, user_id=message.from_user.id)
            if issub == "True":
                if user_status["status"] == 'left':
                    return True
                else:
                    return False
            else:
                return False