from aiogram import types, Dispatcher
from keyboards.client_kb import game_menu
from bot_config import FSM
from handlers.games import bagels

async def show_menu(game_name: str, callback: types.CallbackQuery):
    if game_name == "bagels":
        await FSM.bagels_game_menu.set()
        await bagels.show_menu()



