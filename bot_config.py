from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State


with open("token.txt") as file:
    TOKEN = file.readline()

storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=storage)


class FSM(StatesGroup):
    main_menu = State()
    bagels_game_menu = State()
    bagels_game_info = State()
    bagels_game_leaderboard = State()
    bagels_active_game = State()
