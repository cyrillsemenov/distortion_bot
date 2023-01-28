from aiogram import Dispatcher
from aiogram.types import Message


async def send_welcome(message: Message):
    await message.reply('💦Привет!🍆\n'
                        '🔞Этот бот заменяет слова на 🙈всякую похабщину🙊, '
                        'поэтому уберите детей👶 от экранов📺.\n'
                        'В качестве 📘словаря использован файл <code>pornlist_some_famous_company_data.txt</code>\n'
                        'Просто пришли мне свой текст📄, а я отправлю его отредактированную✏️ версию!',
                        parse_mode="HTML")


def setup(dp: Dispatcher):
    dp.register_message_handler(
        send_welcome,
        commands=['start', 'help']
    )