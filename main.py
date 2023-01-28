"""
This is an explicit echo bot.
It echoes any incoming text messages in distorted way.
"""

import logging
import os

from aiogram import Bot, Dispatcher, executor
from handlers import setup as setup_handlers
from middlewares import setup as setup_middlewares

from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

bot_config = {
    'token': os.environ['BOT_TOKEN']
}

if os.environ.get('PYTHONANYWHERE_SITE'):
    bot_config['proxy'] = 'http://proxy.server:3128'


# Initialize bot and dispatcher
bot = Bot(**bot_config)
dp = Dispatcher(bot)


async def on_startup(dispatcher: Dispatcher):
    setup_middlewares(dispatcher)
    setup_handlers(dispatcher)


async def on_shutdown(dispatcher):
    logging.info('Shutdown.')


if __name__ == '__main__':
    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown
    )

