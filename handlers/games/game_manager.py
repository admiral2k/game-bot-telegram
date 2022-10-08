from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from keyboards.client_kb import game_menu
from bot_config import FSM
from handlers.games import bagels

async def show_menu(game_name: str, callback: types.CallbackQuery, state: FSMContext):
    if game_name == "bagels":
        await FSM.bagels_game_menu.set()
        short_description = bagels.short_description
        if callback.data == "returned_from_game":
            async with state.proxy() as data:
                msg_id = data["msg_id"]
            await msg_id.edit_text(short_description, reply_markup=game_menu, parse_mode="MarkDownV2")
        else:
            await callback.message.edit_text(short_description, reply_markup=game_menu, parse_mode="MarkDownV2")



