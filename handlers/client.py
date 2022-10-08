from bot_config import bot, FSM
from aiogram import types, Dispatcher
from keyboards.client_kb import games_list
from handlers.games import game_manager


async def send_start_message(message: types.Message):
    await FSM.main_menu.set()
    await message.delete()
    await message.answer("*Hey*\! 😀\nI am a game bot\!\nTo see available games, please, use */games* command \:\)\n"
                         "Created by @admiral2k", parse_mode="MarkDownV2")


async def send_list_of_games(message: types.Message):
    await message.answer("Here is the list of available games\. *More games soon\!* 🔽", parse_mode="MarkDownV2",
                         reply_markup=games_list)


async def start_game(callback: types.CallbackQuery):
    await callback.answer()
    await FSM.next()
    game_name = callback.data.split("_")[2]
    await game_manager.show_menu(game_name, callback)


def registrate_handlers(dp: Dispatcher):
    dp.register_message_handler(send_start_message, commands=["start", "help"], state=None)
    dp.register_message_handler(send_list_of_games, commands="games", state=FSM.main_menu)
    dp.register_callback_query_handler(start_game, lambda callback: callback.data.startswith("game_chosen"),
                                       state=FSM.main_menu)
