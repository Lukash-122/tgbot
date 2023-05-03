from aiogram import Dispatcher, types, Bot, executor
from main import TOKEN_API
import random
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

kb = ReplyKeyboardMarkup(resize_keyboard=True,#робить норм розмір клави
                         one_time_keyboard=True)#скриває клаву
button1 = KeyboardButton('так')
button2 = KeyboardButton('ні')
kb.add(button1).add(button2)


deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
random.shuffle(deck)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(text='Будемо грати?',
                         reply_markup=kb)
    await message.delete()

    @dp.message_handler(text="ні")
    async def finish_command(message: types.Message):
        await message.answer(text='Ну як хочеш')
        await message.delete()

    @dp.message_handler(text="так")
    async def starts_command(message: types.Message):
        global player
        global dealer
        player = deck.pop(0)
        await message.answer(text=f"Ваші очки:{player}")
        dealer = deck.pop(0)
        await message.answer(text=f"Очки диллра:{dealer}")
        await message.answer(text='Ще карту??',
                             reply_markup=kb)

        @dp.message_handler(text="так")
        async def card_command(message: types.Message):
            player += deck.pop(0)
            await message.answer(text=f"Ваші :{player}")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)