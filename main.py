import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN
import requests

WEATHER_API_KEY = "97aba1c9708dbacff0648ede33aedbb7"
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_weather(city: str) -> str:
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        weather_description = data['weather'][0]['description']
        return f"Температура в городе {city}: {temperature}°C\nПогодные условия: {weather_description}"
    else:
        return "Не удалось получить данные о погоде. Проверьте название города."

# @dp.message(Command('weather'))
# async def send_weather(message: Message):
#     params = {
#         'q': 'Moscow',
#         'appid': WEATHER_API_KEY,
#         'units': 'metric'
#     }
#     response = requests.get(WEATHER_URL, params=params)
#     data = response.json()
#
#     if response.status_code == 200:
#         temp = data['main']['temp']
#         await message.reply(f"Сейчас в Москве {temp}°C.")
#     else:
#         await message.reply("Не удалось получить данные о погоде. Попробуйте позже.")

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды: \n /start \n /help")

@dp.message(CommandStart())
async def start(message: Message):
    await message.reply("Привет! Я бот, который может предоставить тебе прогноз погоды. Отправь мне название города.")

@dp.message()
async def send_weather(message: Message):
    city = message.text
    weather_info = get_weather(city)
    await message.reply(weather_info)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())