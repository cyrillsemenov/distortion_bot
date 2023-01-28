"""
This is an explicit echo bot.
It echoes any incoming text messages in distorted way.
"""

import logging
import os
import random

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import ChatTypeFilter

from text_distort import TextDistort
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
distort = TextDistort(db_path='explicit_words_list.txt')


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply('💦Привет!🍆\n'
                        '🔞Этот бот заменяет слова на 🙈всякую похабщину🙊, '
                        'поэтому уберите детей👶 от экранов📺.\n'
                        'В качестве 📘словаря использован файл <code>pornlist_some_famous_company_data.txt</code>\n'
                        'Просто пришли мне свой текст📄, а я отправлю его отредактированную✏️ версию!',
                        parse_mode="HTML")


@dp.message_handler(chat_type=types.ChatType.PRIVATE, content_types=types.ContentTypes.TEXT)
async def echo(message: types.Message):
    answer = "\n".join([
        distort(line) if line else ""
        for line in message.text.splitlines()
    ])
    await message.answer(answer)


@dp.message_handler(chat_type=types.ChatType.SUPER_GROUP, content_types=types.ContentTypes.TEXT)
async def echo(message: types.Message):
    if random.random() < 0.05:
        answer = "\n".join([
            distort(line) if line else ""
            for line in message.text.splitlines()
        ])
        await message.answer(answer)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
