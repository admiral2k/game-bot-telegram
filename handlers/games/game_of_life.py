from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import random as r
import time


from bot_config import FSM
from handlers import client
from handlers.games import game_manager
from keyboards.client_kb import back_or_play_kb, end_game_kb

short_description = """*Game of Life 🦠*
Create your own world right in your phone\!"""

long_description = "The Game of Life, also known simply as Life, is a simulation firstly created by the " \
                   "British mathematician John Horton Conway in 1970. It is a zero-player game, meaning " \
                   "that its evolution is determined by its initial state, requiring no further input. So," \
                   "the only thing is needed to see the simulation - start cells. All the cells evolving by their" \
                   "own following next rules:\n If alive cell has 2 or 3 neighbors (alive cells), it keeps alive" \
                   " for next step.\n If dead cell has 3 heighbors, it becomes alive for next step.\n Any other cells" \
                   "die or stay dead for next step."


async def show_info(callback: types.CallbackQuery):
    await FSM.game_of_life_game_info.set()
    await callback.message.edit_text(long_description, reply_markup=back_or_play_kb, parse_mode="HTML")


async def go_back(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(callback.message.text, reply_markup=None)
    if await state.get_state() == FSM.game_of_life_game_info.state:
        await game_manager.show_menu("game_of_life", callback, state)
    elif await state.get_state() == FSM.game_of_life_game_menu.state:
        await FSM.main_menu.set()
        await client.send_list_of_games(callback.message, state)
    elif await state.get_state() == FSM.game_of_life_active_game.state:
        await FSM.game_of_life_game_menu.set()
        callback.data = "returned_from_game"
        await game_manager.show_menu("game_of_life", callback, state)


async def show_leaderboard(callback: types.CallbackQuery):
    await callback.answer("Oops. This function is still in development")


async def start_game(callback: types.CallbackQuery, state: FSMContext):
    await FSM.game_of_life_active_game.set()
    game = GameOfLife(30, 20)
    async with state.proxy() as data:
        data["game"] = game
    await game_cycle(callback, state)


async def game_cycle(callback: types.CallbackQuery, state: FSMContext):
    time.sleep(0.5)
    if callback != "game_button_back" and await state.get_state() == FSM.game_of_life_active_game.state:
        async with state.proxy() as data:
            game = data["game"]
        await callback.message.edit_text(str(game), reply_markup=end_game_kb)
        game.tick()
        async with state.proxy() as data:
            data["game"] = game
        await game_cycle(callback, state)

def registrate_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(show_info, lambda callback: callback.data == "game_button_about",
                                       state=FSM.game_of_life_game_menu)
    dp.register_callback_query_handler(go_back,
                                       lambda callback: callback.data == "game_button_back",
                                       state=[FSM.game_of_life_game_info.state, FSM.game_of_life_game_menu.state,
                                              FSM.game_of_life_active_game.state, FSM.game_of_life_game_leaderboard.state])
    dp.register_callback_query_handler(show_leaderboard,
                                       lambda callback: callback.data == "game_button_leaderboard",
                                       state=FSM.game_of_life_game_menu)
    dp.register_callback_query_handler(start_game,
                                       lambda callback: callback.data == "game_button_start",
                                       state=[FSM.game_of_life_game_menu, FSM.game_of_life_game_info])
    dp.register_callback_query_handler(game_cycle,
                                       lambda callback: callback.data == "game_button_back",
                                       state=FSM.game_of_life_active_game)
    # dp.register_message_handler(send_game_reply, state=FSM.bagels_active_game)


class GameOfLife:
    ALIVE = '0'
    DEAD = '_'

    def __init__(self, width, length):
        if length > 0 and width > 0:
            self._width = width
            self._length = length
            self._currentCells = {}
            self.randomly_fill()
        else:
            raise ValueError("Wrong size input.")

    def __str__(self):
        output = ""
        for y in range(self._length):
            for x in range(self._width):
                output += self._currentCells[(x, y)]
            output += "\n"
        return output

    def get_field(self):
        output = ""
        for y in range(self._length):
            for x in range(self._width):
                output += self._currentCells[(x, y)]
            output += "\n"
        return output

    def randomly_fill(self):
        for x in range(self._width):
            for y in range(self._length):
                if r.randint(0, 1):
                    self._currentCells[(x, y)] = self.ALIVE
                else:
                    self._currentCells[(x, y)] = self.DEAD

    def tick(self):
        next_cells={}
        for x in range(self._width):
            for y in range(self._length):
                right = (x - 1) % self._width
                left = (x + 1) % self._width
                up = (y - 1) % self._length
                down = (y + 1) % self._length

                num_of_neighbors = 0
                if self._currentCells[(left, y)] == self.ALIVE:
                    num_of_neighbors += 1

                if self._currentCells[(left, up)] == self.ALIVE:
                    num_of_neighbors += 1

                if self._currentCells[(x, up)] == self.ALIVE:
                    num_of_neighbors += 1

                if self._currentCells[(right, up)] == self.ALIVE:
                    num_of_neighbors += 1

                if self._currentCells[(right, y)] == self.ALIVE:
                    num_of_neighbors += 1

                if self._currentCells[(right, down)] == self.ALIVE:
                    num_of_neighbors += 1

                if self._currentCells[(x, down)] == self.ALIVE:
                    num_of_neighbors += 1

                if self._currentCells[(left, down)] == self.ALIVE:
                    num_of_neighbors += 1

                if num_of_neighbors in [2, 3] and self._currentCells[(x, y)] == self.ALIVE:
                    next_cells[(x, y)] = self.ALIVE
                elif num_of_neighbors == 3 and self._currentCells[(x, y)] == self.DEAD:
                    next_cells[(x, y)] = self.ALIVE
                else:
                    next_cells[(x, y)] = self.DEAD
        self._currentCells = next_cells