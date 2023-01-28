from aiogram import Dispatcher
from .echo import setup as setup_echo
from .start import setup as setup_start


def setup(dp: Dispatcher):
    setup_start(dp)
    setup_echo(dp)
