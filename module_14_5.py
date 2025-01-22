from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from crud_functions import *

bot = Bot(token='7680362534:AAFxREcENIpGw2eLIBR25rgd7xjTql0mjyQ')
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_registration = KeyboardButton(text='Зарегистриваться')
button_calc = KeyboardButton(text='Рассчитать')
button_buy = KeyboardButton(text='Купить')
button_info = KeyboardButton(text='Информация')
kb.add(button_registration)
kb.add(button_calc)
kb.row(button_buy, button_info)

inline_kb = InlineKeyboardMarkup(resize_keyboard=True)
inline_button_calc = InlineKeyboardButton(text='Рассчитать калории: ', callback_data='calories')
inline_button_formula = InlineKeyboardButton(text='Формула рассчета калорий', callback_data='formulas')
inline_kb.add(inline_button_calc)
inline_kb.add(inline_button_formula)

inline_kb_product = InlineKeyboardMarkup(resize_keyboard=True)
inline_button_product1 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
inline_button_product2 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
inline_button_product3 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
inline_button_product4 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
inline_kb_product.add(inline_button_product1)
inline_kb_product.add(inline_button_product2)
inline_kb_product.add(inline_button_product3)
inline_kb_product.add(inline_button_product4)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()

@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer(f'Привет, {message.from_user.username}! Я бот, который поможет тебе', reply_markup=kb)

@dp.message_handler(text='Зарегистриваться')
async def sing_up(message):
    await message.answer('Введите имя пользователя, спользуя латинский алфавит:')
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text):
        await message.answer('Пользователь с таким именем сущуствует!')
        await RegistrationState.username.set()
    else:
        await state.update_data(username=message.text)
        await message.answer('Введите ваш email: ')
        await RegistrationState.email.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите ваш возраст: ')
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    add_user(data['username'], data['age'], data['email'])
    await message.answer('Зегистрация прошла успешно')
    await state.finish()

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберете опцию: ', reply_markup=inline_kb)

@dp.message_handler(text='Купить')
async def get_catalog(message):
    data = get_all_products()
    for i in range(1, 5):
        with open(f'Product{i}.jpg', 'rb') as img:
            await message.answer_photo(img)
        await message.answer(f'Наименование: {data[i-1][1]}| Описание: {data[i-1][2]}| Цена: {data[i-1][3]}')
    await message.answer('Выберете продукт покупки:', reply_markup=inline_kb_product)

@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Вы можете зарегистрироваться, рассчитать вашу норму калорий. А так же приобрести необходимые витамины',
                         reply_markup=inline_kb)

@dp.callback_query_handler(text='product_buying')
async def send_confim(call):
    await call.message.answer('Спасибо за покупку')
    await call.answer()

@dp.callback_query_handler(text='formulas')
async def get_formula(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5 \n ДЛЯ МУЖЧИН.')
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) -161 \n ДЛЯ ЖЕНЩИН.')
    await call.answer()

@dp.callback_query_handler(text='calories')
async def get_age(call):
    await call.message.answer('Введите ваш возраст: ')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def get_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите ваш рост: ')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def get_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите ваш вес: ')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    men = 10 * int(data['weight']) + 6.25 * int(data['growth']) + 5 * int(data['age']) + 5
    women = 10 * int(data['weight']) + 6.25 * int(data['growth']) + 5 * int(data['age']) - 161
    await message.answer(f'Если вы мужчина, то ваша норма {men}')
    await message.answer(f'Если вы женщина, то ваша норма {women}')
    await state.finish()

@dp.message_handler()
async def all_message(message):
    await message.answer('Для начала общения введите команду /start')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)