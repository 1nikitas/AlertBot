from aiogram import Bot, executor, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from db import Database


bot = Bot(token="5394783980:AAFmlnp_lWi3wzkFTNUhp1fKbv9btLB4-Bk")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database('db.db')

keyboard_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Пройти регистрацию🤝")
        ]
    ], resize_keyboard=True
)


class register(StatesGroup):
    table_number = State()


@dp.message_handler(Command("start"))
async def getUsers(message: types.Message):
        await message.answer("Тебя привествует бот😃\n"
                                 "Тебе доступна регистрация 🙌", reply_markup=keyboard_menu)

@dp.message_handler(text="Пройти регистрацию🤝")
async def register_(message: types.Message):
    if not db.userExists(message.from_user.id):
        await message.answer("Ты перешел в меню регистрации.\n"
                             "Введи свой табельный номер ⚠")
        await register.table_number.set()
    else:
        await message.answer("Ты уже прошел регистрацию!")

@dp.message_handler(state = register.table_number)
async def table(message: types.Message, state: FSMContext):
    answer = message.text

    await state.update_data(table_number=answer)
    data = await state.get_data()

    table_number = data.get('table_number')
    db.addUser(message.from_user.id, table_number)
    await state.finish()
    await message.answer("Данные успешно получены!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)