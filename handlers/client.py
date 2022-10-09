from aiogram.dispatcher import FSMContext

from bot_config import bot, FSM
from aiogram import types, Dispatcher
from keyboards.client_kb import games_list
from handlers.games import game_manager


async def send_start_message(message: types.Message, state: FSMContext):
    if await state.get_state() is not None:
        await state.finish()
    await FSM.main_menu.set()
    msg_id = await message.answer("*Hey*\! 😀\nI am a game bot\!\nTo see available games, please, use */games* command \:\)\n"
                         "Created by @admiral2k", parse_mode="MarkDownV2")
    async with state.proxy() as data:
        data["msg_id"] = msg_id


async def send_list_of_games(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        msg_id = data["msg_id"]
    if not message.from_user.is_bot:
        await message.delete()
    await msg_id.edit_text("Here is the list of available games\. *More games soon\!* 🔽", parse_mode="MarkDownV2",
                         reply_markup=games_list)


async def start_game(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await FSM.next()
    game_name = callback.data.split("game_chosen_")[1]
    await game_manager.show_menu(game_name, callback, state)


def registrate_handlers(dp: Dispatcher):
    dp.register_message_handler(send_start_message, commands=["start", "help"], state="*")
    dp.register_message_handler(send_list_of_games, commands="games", state=FSM.main_menu)
    dp.register_callback_query_handler(start_game, lambda callback: callback.data.startswith("game_chosen"),
                                       state=FSM.main_menu)
