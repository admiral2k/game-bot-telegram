from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

games_list = InlineKeyboardMarkup(row_width=1)
bagels = InlineKeyboardButton("Bagels 💀", callback_data="game_chosen_bagels")
game_of_life = InlineKeyboardButton("Game of Life 🦠", callback_data="game_chosen_game_of_life")
games_list.add(bagels, game_of_life)


game_menu = InlineKeyboardMarkup(row_width=2)
show_about = InlineKeyboardButton("📍 About Game", callback_data="game_button_about")
show_records_table = InlineKeyboardButton("Leaderboard 🏆", callback_data="game_button_leaderboard")
go_back = InlineKeyboardButton("◀️ Back", callback_data="game_button_back")
start_game = InlineKeyboardButton("START 🎮", callback_data="game_button_start")
game_menu.row(show_about, show_records_table).row(go_back, start_game)

back_or_play_kb = InlineKeyboardMarkup(row_width=2).row(go_back, start_game)

end_game_kb = InlineKeyboardMarkup().add(go_back)
