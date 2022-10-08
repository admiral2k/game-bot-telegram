from aiogram.utils import executor
from bot_config import dp, bot, FSM
from handlers import client


async def on_startup(_):
    print("Bot successfully started.")
    await bot.send_message(1267043297, "Bot started")

client.registrate_handlers(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)