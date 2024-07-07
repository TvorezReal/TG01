import asyncio
import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from googletrans import Translator

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()


@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Привет! Отправь мне дату в формате ММ/ДД, и я расскажу тебе интересный факт о ней. Например: 10/25")


@dp.message()
async def get_date_fact(message: Message):
    try:
        # Разбиваем дату на месяц и день
        month, day = message.text.split('/')
        # Формируем URL для запроса к API
        url = f"http://numbersapi.com/{month}/{day}/date"
        # Делаем запрос к API
        response = requests.get(url)
        # Если запрос успешный, переводим факт на русский и отправляем пользователю
        if response.status_code == 200:
            fact_in_english = response.text
            fact_in_russian = translator.translate(fact_in_english, src='en', dest='ru').text
            await message.answer(fact_in_russian)
        else:
            await message.answer("Не удалось получить факт. Пожалуйста, убедитесь, что вы ввели дату в правильном формате ММ/ДД.")
    except Exception as e:
        await message.answer("Произошла ошибка. Пожалуйста, убедитесь, что вы ввели дату в правильном формате ММ/ДД.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())