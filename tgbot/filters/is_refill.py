from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter
from tgbot.services.sqlite import get_settings

class IsRefill(BoundFilter):
    async def check(self, message: Message) -> bool:
        if get_settings()['is_refill'] == "True":
            return False
        else:
            return True