from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter
from tgbot.utils.utils_functions import get_admins

class IsAdmin(BoundFilter):
    async def check(self, message: Message) -> bool:
        user_id = message.from_user.id
        return user_id in get_admins()