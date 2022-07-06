from aiogram import Bot, executor, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from db import Database
from openpyxl import load_workbook

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
    wb = load_workbook(filename='для бота.xlsx')  # сюда указывается имя файла
    sheet_ranges = wb['Лист1']  # сюда указывается имя листа из экселя
    table_numbers = [table_number.value for table_number in sheet_ranges["B"]][1:]

    for table_number in table_numbers:
        tg_id = "".join(db.tgIdSelector(table_number)[0])
        print(tg_id)
        await bot.send_message(tg_id, "Отметьтесь, пожалуйста")




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)