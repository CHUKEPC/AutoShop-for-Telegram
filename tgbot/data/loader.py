# - *- coding: utf- 8 - *-
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tgbot.data.config import bot_token

bot = Bot(token=bot_token, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
scheduler = AsyncIOScheduler()