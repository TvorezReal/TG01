from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
   [KeyboardButton(text="Привет"), KeyboardButton(text="Пока")]
], resize_keyboard=True)

inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text="Новости", url='https://www.youtube.com/watch?v=HfaIcB4Ogxk')],
   [InlineKeyboardButton(text="Музыка", url='https://www.youtube.com/watch?v=HfaIcB4Ogxk')],
   [InlineKeyboardButton(text="Видео", url='https://www.youtube.com/watch?v=HfaIcB4Ogxk')]
])

dynamic_keyboard = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text="Показать больше", callback_data='view_more')],
])

change_keyboard = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text="опция 1", callback_data='option_1'), InlineKeyboardButton(text="опция 2", callback_data='option_2')]
])

test = ["опция 1", "опция 2"]

async def test_keyboard():
   keyboard = InlineKeyboardBuilder()
   for key in test:
       keyboard.add(InlineKeyboardButton(text=key, url='https://www.youtube.com/watch?v=HfaIcB4Ogxk'))
   return keyboard.adjust(2).as_markup()