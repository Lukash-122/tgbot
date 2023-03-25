from aiogram import Bot, Dispatcher, executor, types
from main import TOKEN_API
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

help_commands = '''
/help = інструкія до бота
/review = показ всіх даних
'''

HELP = ''' 
Щоб додати дані до файлу потрібно перед повідомленням дописати wr. Приклад:
wr ООП - 17.04.
Щоб видалити дані з файлу потрібно перед повідомленням дописати de. Приклад:
de ООП - 17.04.
'''

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(KeyboardButton('/help'), KeyboardButton('/commands'), KeyboardButton('/review'))


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer('hello', reply_markup=kb)


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer(HELP)


@dp.message_handler(commands=['commands'])
async def commands_command(message: types.Message):
    await message.answer(help_commands)


@dp.message_handler(commands=['review'])
async def review_command(message: types.Message):
    with open('file.txt', 'r') as file:
        await message.answer(file.read())


@dp.message_handler(lambda message: message.text.startswith('wr'))
async def write_file(message: types.Message):
    with open('file.txt', 'a', encoding='utf-8') as file:
        dat = message.text.lstrip('wr ')
        file.write(dat + '\n')


@dp.message_handler(lambda message: message.text.startswith('de'))
async def delete_file(message: types.Message):
    with open('file.txt', 'r', encoding='utf-8') as file:
        content = file.readlines()
        new_content = ''
        for i in content:
            if 'de ' + i != message.text + '\n':
                new_content += i
    with open('file.txt', 'w', encoding='utf-8') as file:
        file.write(new_content)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)