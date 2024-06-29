import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import TOKEN
from googletrans import Translator
import requests
import random

from gtts import gTTS
import os

WEATHER_API_KEY = "97aba1c9708dbacff0648ede33aedbb7"
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'

bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()

@dp.message()
async def translate_text(message: Message):
    original_text = message.text.lower()
    translated = translator.translate(text=original_text, src='auto', dest='en')
    await message.reply(f"Перевод: {translated.text}")

@dp.message(Command('audio'))
async def audio(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_audio')
    audio = FSInputFile('audio.mp3')
    await bot.send_audio(message.from_user.id, audio=audio)

@dp.message(Command('video'))
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')
    video = FSInputFile('video.mp4')
    await bot.send_video(message.from_user.id, video=video)

@dp.message(Command('training'))
async def training(message: Message):
   training_list = [
       "Тренировка 1:\\n1. Скручивания: 3 подхода по 15 повторений\\n2. Велосипед: 3 подхода по 20 повторений (каждая сторона)\\n3. Планка: 3 подхода по 30 секунд",
       "Тренировка 2:\\n1. Подъемы ног: 3 подхода по 15 повторений\\n2. Русский твист: 3 подхода по 20 повторений (каждая сторона)\\n3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
       "Тренировка 3:\\n1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений\\n2. Горизонтальные ножницы: 3 подхода по 20 повторений\\n3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
   ]
   rand_tr = random.choice(training_list)
   await message.answer(f"Это ваша мини-тренировка на сегодня {rand_tr}")

   tts = gTTS(text=rand_tr, lang='ru')
   tts.save("training.ogg")
   await bot.send_voice(message.from_user.id, FSInputFile("training.ogg"))
   os.remove("training.ogg")

@dp.message(Command('voice'))
async def voice(message: Message):
    voice = FSInputFile("sample.ogg")
    await message.answer_voice(voice)

@dp.message(Command('doc'))
async def doc(message: Message):
    doc = FSInputFile("TG02.pdf")
    await bot.send_document(message.chat.id, doc)

@dp.message(F.photo)
async def react_photo(message: Message):
    lst = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(lst)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1], destination=f'tmp/{message.photo[-1].file_id}.jpg')

# def get_weather(city: str) -> str:
#     url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru'
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         temperature = data['main']['temp']
#         weather_description = data['weather'][0]['description']
#         return f"Температура в городе {city}: {temperature}°C\nПогодные условия: {weather_description}"
#     else:
#         return "Не удалось получить данные о погоде. Проверьте название города."

@dp.message(Command('weather'))
async def send_weather(message: Message):
    params = {
        'q': 'Moscow',
        'appid': WEATHER_API_KEY,
        'units': 'metric'
    }
    response = requests.get(WEATHER_URL, params=params)
    data = response.json()

    if response.status_code == 200:
        temp = data['main']['temp']
        await message.reply(f"Сейчас в Москве {temp}°C.")
    else:
        await message.reply("Не удалось получить данные о погоде. Попробуйте позже.")

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды: \n /start \n /help \n /weather")

@dp.message(CommandStart())
async def start(message: Message):
    await message.reply(f"Привет,{message.from_user.full_name}. \n Я бот, который может предоставить тебе прогноз погоды.")



# @dp.message()
# async def send_weather(message: Message):
#     city = message.text
#     weather_info = get_weather(city)
#     await message.reply(weather_info)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())