from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bot_config import FSM
from handlers import client
from handlers.games import game_manager
from keyboards.client_kb import game_menu, back_or_play_kb


short_description = """*Bagels 💀*
Try to save the world using your deductive skills\!"""

long_description = "I thought up a 3-digit number. You have 10 guesses to get the number. Otherwise, " \
                   "i'll kill the whole world. So, please, pull yourself together :)" \
                   "I know about your silly mind so i'll give you some clues during our pretty game:" \
                   "\n\nWhen i say:         That means:" \
                   "\n<b>Pico</b>   -   One digit is correct but in the wrong position." \
                   "\n<b>Fermi</b>   -   One digit is correct and in the right position." \
                   "\n<b>Bagels</b>   -   No correct digits in your guess >:c." \
                   "\n\nThe clues will be represented in the alphabet order, so the position of a clue means nothing." \
                   "\n<b>So, lets start the game!</b>"


async def show_info(callback: types.CallbackQuery):
    await callback.message.edit_text(long_description, reply_markup=back_or_play_kb, parse_mode="HTML")
    await FSM.bagels_game_info.set()


async def go_back(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    if await state.get_state() == FSM.bagels_game_info.state:
        await game_manager.show_menu("bagels", callback)
    elif await state.get_state() == FSM.bagels_game_menu.state:
        await FSM.main_menu.set()
        await client.send_list_of_games(callback.message, state)


async def show_leaderboard(callback: types.CallbackQuery):
    await callback.answer("Oops. This function is still in development")


async def start_game(callback: types.CallbackQuery, state: FSMContext):
    pass

def registrate_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(show_info, lambda callback: callback.data == "game_button_about",
                                       state=FSM.bagels_game_menu)
    dp.register_callback_query_handler(go_back,
                                       lambda callback: callback.data == "game_button_back", state="*")
    dp.register_callback_query_handler(show_leaderboard,
                                       lambda callback: callback.data == "game_button_leaderboard",
                                       state=FSM.bagels_game_menu)




