from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bot_config import FSM
from handlers import client
from handlers.games import game_manager
from keyboards.client_kb import game_menu, back_or_play_kb, end_game_kb
from utils.exceptions import AccessError, ActionError
import random as r


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
    await callback.message.edit_text(callback.message.text ,reply_markup=None)
    if await state.get_state() == FSM.bagels_game_info.state:
        await game_manager.show_menu("bagels", callback, state)
    elif await state.get_state() == FSM.bagels_game_menu.state:
        await FSM.main_menu.set()
        await client.send_list_of_games(callback.message, state)
    elif await state.get_state() == FSM.bagels_active_game.state:
        await FSM.bagels_game_menu.set()
        callback.data = "returned_from_game"
        await game_manager.show_menu("bagels", callback, state)


async def show_leaderboard(callback: types.CallbackQuery):
    await callback.answer("Oops. This function is still in development")


async def start_game(callback: types.CallbackQuery, state: FSMContext):
    await FSM.bagels_active_game.set()
    game = BagelsGame(3, 10)
    game.start_game()
    async with state.proxy() as data:
        data["game"] = game

    await callback.message.edit_text(long_description, reply_markup=end_game_kb, parse_mode="HTML")
    msg_id = await callback.message.answer("Guess #1")

    async with state.proxy() as data:
        data["msg_id"] = msg_id
    # while game.get_game_state():
    #     print(game.user_guess(input(f"Guess #{game.get_current_guess()}\n>")))


async def send_game_reply(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        game = data["game"]
    text = game.user_guess(message.text)
    if text.startswith("Congrats") or text.startswith("Oops"):
        await FSM.bagels_game_info.set()
        text += "\nDo you want to play again?"
        msg_id = await message.answer(text, reply_markup=back_or_play_kb)
    elif game.get_game_state():
        text += f"\nGuess#{game.get_current_guess()}"
        msg_id = await message.answer(text)

    async with state.proxy() as data:
        data["game"] = game
        data["msg_id"] = msg_id



def registrate_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(show_info, lambda callback: callback.data == "game_button_about",
                                       state=FSM.bagels_game_menu)
    dp.register_callback_query_handler(go_back,
                                       lambda callback: callback.data == "game_button_back", state="*")
    dp.register_callback_query_handler(show_leaderboard,
                                       lambda callback: callback.data == "game_button_leaderboard",
                                       state=FSM.bagels_game_menu)
    dp.register_callback_query_handler(start_game,
                                       lambda callback: callback.data == "game_button_start",
                                       state=[FSM.bagels_game_menu, FSM.bagels_game_info])
    dp.register_message_handler(send_game_reply, state=FSM.bagels_active_game)



class BagelsGame:
    _alphabet = "1234567890"
    _current_guess = None
    _answer = None
    _active_game = False

    def __init__(self, number_of_digits: int, number_of_guesses: int):
        self.set_number_of_digits(number_of_digits)
        self.set_number_of_guesses(number_of_guesses)

    def start_game(self):
        """Start of the game"""
        if not self._active_game:
            self._active_game = True
            self._current_guess = 1
            self._answer = self._create_word()
        else:
            raise ActionError("Game already started.")

    def end_game(self):
        """End of the game"""
        if self._active_game:
            self._active_game = False
        else:
            raise ActionError("Game already ended.")

    def user_guess(self, guess: str):
        # checking whether the input is valid
        if len(guess) == self._number_of_digits and guess.isdecimal():

            # case of the user win
            if guess == self._answer:
                self.end_game()
                return f"Congrats! You guessed the number \"{self._answer}\" within {self._current_guess} guesses!"

            # case of the user lose
            elif guess != self._answer and self._current_guess == self._number_of_guesses:
                self.end_game()
                return f"Oops. Seems like you failed the world. The right number was \"{self._answer}\"."

            self._current_guess += 1
            clues = []

            # filling up the clues array
            for i in range(self._number_of_digits):
                if guess[i] == self._answer[i]:
                    clues.append("Fermi")
                elif guess[i] in self._answer:
                    clues.append("Pico")

            # case of no clues (no correct digits in the guess)
            if len(clues) == 0:
                clues.append("Bagels")
            else:
                # sorting clues to disable the user to detect the position of the correct letter
                clues.sort()

            clue = " ".join(clues)

        # formatting the wrong input message
        else:
            clue = "Wrong input!\n"

            # case of the wrong length
            if len(guess) != self._number_of_digits:
                clue += f'You need to write {self._number_of_digits} digits!\n'

            # case of the wrong letters usage
            if not guess.isdecimal():
                clue += "You should use only digits.\n"

        return clue

    def get_current_guess(self) -> int:
        if self._active_game:
            return self._current_guess
        else:
            raise AccessError("Can't access because game not started.")

    def get_game_state(self) -> int:
        return self._active_game

    def set_number_of_digits(self, number_of_digits: int) -> None:
        if (10 >= number_of_digits >= 1) and not self._active_game:
            self._number_of_digits = number_of_digits
        elif not (10 >= number_of_digits >= 1):
            raise ValueError('Wrong number of digits is given. '
                             'Following number should be more than 0 and less than 11.')
        elif self._active_game:
            raise AccessError("Can't change number of digits while game is started.")

    def set_number_of_guesses(self, number_of_guesses: int) -> None:
        if number_of_guesses > 0 and not self._active_game:
            self._number_of_guesses = number_of_guesses
        elif number_of_guesses < 0:
            raise ValueError(('Wrong number of guesses is given. '
                             'Following number should be more than 0.'))
        elif self._active_game:
            raise AccessError("Can't change number of guesses while game is started.")

    def _create_word(self) -> str:
        """creation of the secret word"""
        # randomizing the alphabet
        temp_shuffled_alphabet = list(self._alphabet)
        r.shuffle(temp_shuffled_alphabet)

        # taking first N letters from shuffled alphabet, so repetitive letters  are avoided
        word = "".join(temp_shuffled_alphabet[:self._number_of_digits])
        return word