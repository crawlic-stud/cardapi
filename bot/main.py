import os
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram_dialog import DialogManager, StartMode, DialogRegistry
from dotenv import load_dotenv

from .dialogs.states import Menu


load_dotenv()

bot = Bot(os.getenv("TG_TOKEN"), parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)
registry = DialogRegistry(dp)


@dp.message_handler(commands=["start"])
async def start(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(Menu.start, mode=StartMode.RESET_STACK)


def start_bot():
    from .dialogs import MENU

    registry.register(MENU)

    executor.start_polling(
        dp, skip_updates=True
    )
