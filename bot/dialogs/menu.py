from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.text import Const

from .states import Menu


MENU = Dialog(
    Window(
        Const("Добро пожаловать!"),
        state=Menu.start
    )
)
