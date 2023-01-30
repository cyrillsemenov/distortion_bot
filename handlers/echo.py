import random

from aiogram import Dispatcher
from aiogram.types import Message, ChatType, ContentTypes

from text_distort import TextDistort

distort = TextDistort(db_path='explicit_words_list.txt')


async def echo_private(message: Message):
    answer = "\n".join([
        distort(line) if line else ""
        for line in message.text.splitlines()
    ])
    await message.answer(answer)


async def echo_group(message: Message):
    if random.random() < 0.05:
        answer = "\n".join([
            distort(line) if line else ""
            for line in message.text.splitlines()
        ])
        await message.answer(answer)


def setup(dp: Dispatcher):
    dp.register_message_handler(
        echo_private,
        chat_type=ChatType.PRIVATE, content_types=ContentTypes.TEXT
    )
    dp.register_message_handler(
        echo_private,
        chat_type=[ChatType.SUPERGROUP, ChatType.GROUP], content_types=ContentTypes.TEXT
    )
