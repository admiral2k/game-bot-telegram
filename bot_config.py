from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State

TOKEN = '1838250326:AAGVUGJM9o8P9KzaCcTW2EM-yZFUjpKpfJ0'

storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=storage)


class FSM(StatesGroup):
    main_menu = State()

    bagels_game_menu = State()
    bagels_game_info = State()
    bagels_game_leaderboard = State()
    bagels_active_game = State()

    game_of_life_game_menu = State()
    game_of_life_game_info = State()
    game_of_life_game_leaderboard = State()
    game_of_life_active_game = State()
