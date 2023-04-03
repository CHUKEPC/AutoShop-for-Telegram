from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter
from tgbot.services.sqlite import get_user
from tgbot.utils.utils_functions import get_admins
class IsBan(BoundFilter):
    async def check(self, message: Message) -> bool:
        user = get_user(id=message.from_user.id)
        if user['is_ban'] == "True" and not user['id'] in get_admins():
            return True
        else:
            return False
            
