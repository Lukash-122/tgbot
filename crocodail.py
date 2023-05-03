from aiogram import Dispatcher, Bot, types, executor
from main import TOKEN_API
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import random

user_name = ''

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

s = [i for i in range(0, 1000)]


def croc_keyboard():
    ikb = InlineKeyboardMarkup()
    ikb.add(InlineKeyboardButton('Слово', callback_data='1'), InlineKeyboardButton('інше слово', callback_data='2'))
    return ikb


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    global user_name
    user_name = message["from"]["username"]
    await message.answer(f'Загадує {user_name} ',
                         reply_markup=croc_keyboard())


@dp.callback_query_handler()
async def callback_crock(callback: types.CallbackQuery):
    if callback.from_user.username == user_name:
        if callback.data == '1':
            with open('file.txt', 'r') as file:
                await callback.answer(file.read())
        if callback.data == '2':
            with open('file.txt', 'w') as file:
                file.write(str(random.choice(s)))
            with open('file.txt', 'r') as file:
                await callback.answer(file.read())


@dp.message_handler()
async def correct_word(message: types.Message):
    global user_name
    with open('file.txt', 'r') as file:
        if file.read() == message.text:
            with open('file.txt', 'w') as files:
                files.write(str(random.choice(s)))
            user_name = message.from_user.username
            await message.answer(f'Загадує {message["from"]["username"]}',
                                 reply_markup=croc_keyboard())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)