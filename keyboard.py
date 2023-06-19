from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def generate(buttons):
    keyboard = InlineKeyboardMarkup()
    for button in buttons:
        keyboard.add(InlineKeyboardButton(text=button[0],callback_data=button[1]))
    return keyboard