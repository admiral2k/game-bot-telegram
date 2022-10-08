from aiogram import types, Dispatcher
from keyboards.client_kb import game_menu

short_description = """*Bagels 💀*
Try to save the world using your deductive skills\!"""

long_description = """I thought up a 3-digit number. You have 10 guesses to get the number. Otherwise, 
i'll kill the whole world. So, please, pull yourself together :)
I know about your silly mind so i'll give you some clues during our pretty game:
When i say:         That means:
*Pico*          One digit is correct but in the wrong position.
*Fermi*         One digit is correct and in the right position.
*Bagels*        No correct digits in your guess >:c.

The clues will be represented in the alphabet order, so the position of a clue means nothing.
So, lets start the game!"""


async def show_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(short_description, reply_markup=game_menu, parse_mode="MarkDownV2")


def registrate_handlers(dp: Dispatcher):
    pass

