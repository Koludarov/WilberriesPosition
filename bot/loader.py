import asyncio
import logging.config
import os

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

logging.config.fileConfig('etc/logging.conf')
logger = logging.getLogger(__name__)

load_dotenv()

token = os.getenv("BOT_TOKEN")
bot = Bot(token=token)
loop = asyncio.get_event_loop()
storage = MemoryStorage()
dp = Dispatcher(bot, loop=loop, storage=storage)
