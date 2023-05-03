from aiogram import Bot, Dispatcher, types, executor
from keybord import kb, ikb
from main import TOKEN_API
from random import choice, randrange
bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

HELP_COMMAND ='''
/start - Запуск бота
/help - Опис команд
/description - Опис можливостей бота
 /photo - Генерує рандомне фото 
 /stickers - Відправляє стікер
 /emoji - відправляє емоджі
 /random_place - відправляє рандомне місце на карті '''

photos = ['https://img.freepik.com/free-photo/lavender-field-at-sunset-near-valensole_268835-3910.jpg',
          'https://static-cse.canva.com/blob/847064/29.jpg',
          'https://img.freepik.com/free-photo/landscape-of-morning-fog-and-mountains-with-hot-air-balloons-at-sunrise_335224-794.jpg',
          'https://prophotos.ru/data/articles/0002/2622/image-rectangle_600_x.jpg']

like = False
dislike = False


async def on_startup(_):
    print('Я запустився')


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text='Вітаю в моєму боті',
                           reply_markup=kb)


@dp.message_handler(commands=['emoji'])
async def emoji_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text='💋')


@dp.message_handler(commands=['random_place'])
async def command_random_place(message: types.Message):
    await bot.send_location(chat_id=message.chat.id,
                            latitude=randrange(-90, 90),
                            longitude=randrange(-180, 180))


@dp.message_handler(commands=['stickers'])
async def stickers_command(message: types.Message):
    await bot.send_sticker(chat_id=message.chat.id,
                           sticker='CAACAgIAAxkBAAEIC5ZkB7DIjiROAV5OCvNE_VmBmPVTFgACsQwAAsgCUEjyCmjnV5lUti4E')


@dp.message_handler(commands=['description'])
async def description_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text='Бот покаже все чого я навчився')


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text=HELP_COMMAND)


@dp.message_handler(commands=['photo'])
async def photo_command(message: types.Message):
    await bot.send_photo(chat_id=message.chat.id,
                         photo=choice(photos),
                         caption='Твоє рандомне фото',
                         reply_markup=ikb)


@dp.callback_query_handler()
async def callback_vote(callback: types.CallbackQuery):
    global like
    global dislike
    if callback.data == 'like':
        dislike = False
        if like:
            return await callback.answer(text='Ви вже відправляли даний текст')
        like = True
        return await callback.answer(text='Тобі сподобалось',)
    elif callback.data == 'dislike':
        like = False
        if dislike:
            return await callback.answer(text='Ви вже відправляли даний текст')
        dislike = True
        return await callback.answer(text='Тобі не сподобалось')
    await bot.send_photo(chat_id=callback.message.chat.id,
                         photo=choice(photos),
                         caption='Твоє рандомне фото',
                         reply_markup=ikb)
    await callback.answer()


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)